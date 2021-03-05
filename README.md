# Telehealth with Google Workspace and the Healthcare API

This repository contains the following artifactse that can help you setup your solution
It assumes you have familiarity with GCP pub/sub etc and have created a pubsub topic etc.
It assumes you know how to deploy code to appengine.

## ./appscript:
This folder has an image GoogleformScreenshot.png that has a snapshot of an example Google Form and 
how you can start to add AppScript Code.
The 2 .gs files are example AppScript Code I used for my solution


## ./appengine:
This folder contains example code used to query a FHIR store using Google's healthcare API.
The example is in the form of a webpage that looks up existing patient info and creates a custom link 
to a google form pre-populated with information. The webapp could easily be modified to offer a rest endpoint 
via which queries to the FHIR repository could be done.

## ./whistle
This folder has a whistle mapping file that specifies the transformation required from the Google form to 
a FHIR Patient resource ready for writing to a FHIR store.
This needs to be used in conjunction with this whistle library referenced here 
https://github.com/GoogleCloudPlatform/healthcare-data-harmonization

## ./examples
This folder has samples of what the submitted form data and a patient resource might look like.

