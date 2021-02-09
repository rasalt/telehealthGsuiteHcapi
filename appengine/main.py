# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_storage_app]
import logging
import os

import google.auth
from google.auth import app_engine
from google.auth.transport import requests
from google.oauth2 import service_account

from model import HomeForm
from flask import Flask, render_template, request, url_for, redirect, session
from flask_session import Session

import sys
import json
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
# [START healthcare_get_session]
def get_session():
    """Creates an authorized Requests Session."""

    # Pass in the credentials and project ID. If none supplied, get them
    # from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )

    # Create a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    return session
# [END healthcare_get_session]

def get_resource(
    base_url,
    project_id,
    cloud_region,
    dataset_id,
    fhir_store_id,
    resource_type,
    resource_id,
):
    """Gets a FHIR resource."""
    url = "{}/projects/{}/locations/{}".format(base_url, project_id, cloud_region)

    resource_path = "{}/datasets/{}/fhirStores/{}/fhir/{}/{}".format(
        url, dataset_id, fhir_store_id, resource_type, resource_id
    )

    # Make an authenticated API request
    session = get_session()

    headers = {"Content-Type": "application/fhir+json;charset=utf-8"}
    app.logger.info("url is :{}".format(resource_path))
    response = session.get(resource_path, headers=headers)
    response.raise_for_status()

    resource = response.json()

    app.logger.info("Got {} resource:".format(resource["resourceType"]))
    app.logger.info(json.dumps(resource, indent=2))

    return resource

base_url = os.environ['BASE_URL']
project_id = os.environ['PROJECT_ID']
cloud_region = os.environ['REGION']
dataset_id = os.environ['DATASET_ID']
fhir_store_id = os.environ['FHIR_STORE_ID']


def queryHCapi(resource_id, resource_type):
    app.logger.info("PatientId {}".format( resource_id ))
    app.logger.info("ResourceType {}".format(resource_type))
    resource  = get_resource(
      base_url,
      project_id,
      cloud_region,
      dataset_id,
      fhir_store_id,
      resource_type,
      resource_id)
    return resource


#Query fhir store
def existingPatientLookup(
    base_url, project_id, cloud_region, dataset_id, fhir_store_id, query
):
    """
    Searches resources in the given FHIR store.

    It uses the
    _search POST method and a query string containing the
    information to search for. In this sample, the search criteria is
    'family:exact=Smith' on a Patient resource.
    """
    url = "{}/projects/{}/locations/{}".format(base_url, project_id, cloud_region)

    fhir_store_path = "{}/datasets/{}/fhirStores/{}/fhir".format(
        url, dataset_id, fhir_store_id
    )

    resource_path = "{}/Patient/_search{}".format(fhir_store_path, query)

    # Make an authenticated API request
    session = get_session()

    headers = {"Content-Type": "application/fhir+json;charset=utf-8"}

    response = session.post(resource_path, headers=headers)
    response.raise_for_status()

    resources = response.json()
    print(
        "Using POST request, found a total of {} Patient resources:".format(
            resources["total"]
        )
    )

    print(json.dumps(resources, indent=2))
    id = resources["entry"][0]["resource"]["id"]
    app.logger.info("Got patient id {}".format(id))
    return id, resources

@app.route('/', methods=['GET', 'POST'])
def index():
    template_name = 'homeform'
    form = HomeForm(request.form)
    result = None
    app.logger.info("Request method is {}".format(request.method))
    if request.method == 'POST': # and form.validate():
        app.logger.info("Input Data")
        app.logger.info("email: {}".format(form.email.data))    
        app.logger.info("lastname: {}".format(form.lastname.data))    
        app.logger.info("dob: {}".format(form.dob.data))    
        app.logger.info("new patient:  {}".format(form.newpatient.data))
        lastname = form.lastname.data    
        dob = form.dob.data    
        email = form.email.data    
        newpatient = form.newpatient.data
        if (newpatient == 'yes'):
           app.logger.info("new patient")
           redirect(url_for("newPatient"))
        else:
           app.logger.info("existing patient")
           query="?birthDate={}&family={}".format(dob,lastname) 
           patientid,patientResource = existingPatientLookup(base_url, project_id, cloud_region, dataset_id, fhir_store_id, query)
           return redirect(url_for('existingPatient',id=patientid, email=email))
          
    app.logger.info("rendering template")    
    return render_template(template_name + '.html',
                           form=form, result=result)

@app.route('/newPatient', methods=['GET', 'POST'])
def newPatient():
    print('Hello new patient')
    return 0

def createformurl(message):
    base_url = "https://docs.google.com/forms/d/e/1FAIpQLSc302VjEc7Rdl1omwDB0NfAR6z8SPx1r_sNn-jxXTpe_hi8Ng/viewform?"
    url = base_url + "entry.128528274=" + message['name'][0]['given'][0]
    url = url + "&" + "entry.1097928041=" + message['name'][0]['family']
    url = url + "&" + "entry.1420404417=" + message['gender'].capitalize()
    url = url + "&" + "entry.1158965125=" + message['birthDate']
    return url

@app.route('/existingPatient')
def existingPatient():
    id = request.args.get('id')
    email = request.args.get('email')
    template_name = 'existingPatient'
    patientResource = queryHCapi(id, "Patient")
    app.logger.info("existint P {}".format(patientResource['birthDate']))
    app.logger.info("existint P {}".format(patientResource['name'][0]['family']))
    url = createformurl(patientResource)
    message = "Geat to see you back, click on the form link below. It is populated with the data we have in file for you. Please update it wherever necessary and add what brings you in today" 
    return render_template(template_name + '.html',data = url, msg = message)
#
#{'birthDate': '2010-01-01', 'gender': 'male', 'id': '3017a631-d4cf-4c64-9417-a39300ecb651', 'meta': {'lastUpdated': '2020-07-30T22:16:01.866247+00:00', 'versionId': 'MTU5NjE0NzM2MTg2NjI0NzAwMA'}, 'name': [{'family': 'Baker', 'given': ['John'], 'use': 'official'}], 'resourceType': 'Patient'}
#

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
