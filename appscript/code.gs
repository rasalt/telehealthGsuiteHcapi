var PROJECT = '<Your project name>';
var PUBSUB_TOPIC = '<Your created Pub/Sub topic in GCP that this Appscript will be publishing to>';
var API_KEY = '<Your API Key>';
var CLIENT_ID = '<Client ID>';
var CLIENT_SECRET = '<Client Secret>';

function datefix(inpDate) {
  function pad(s) { return (s < 10) ? '0' + s : s; }
  var d = new Date(inpDate);
  dateString = [d.getFullYear(), pad(d.getMonth()+1), pad(d.getDate())].join('-')
  console.log(dateString)
  return dateString
}

function myFunction(e) {

  var data = e.namedValues;
  var patientData= {
     fname: e.namedValues['First Name'][0],
     mname: e.namedValues['Middle Name'][0],
     lname: e.namedValues['Last Name'][0],
     sex: e.namedValues['Sex'][0],
     dob: datefix(e.namedValues['Date of Birth (MM/DD/YYYY)'][0]),
     ht: e.namedValues['Height (inches)'][0],
     wt: e.namedValues['Weight (pounds)'][0],
     cn: e.namedValues['Contact Number (Area Code - Phone Number)'][0],
     ms: e.namedValues['Marital Status'][0],
     addrstreet: e.namedValues['Address - Street'][0],
     addrcity: e.namedValues['Address - City'][0],
     addrstate: e.namedValues['Address - State'][0],
     addrzip: e.namedValues['Address - ZipCode'][0],
     addrstart: e.namedValues['Address - Living since'][0],
     addruse: e.namedValues['Address - Use'][0],
     email: e.namedValues['Email Address'][0]
  };

  console.log('PATIENT DATA');
  console.log(patientData);
  var payload = JSON.stringify(patientData);
  console.log('PAYLOAD');
  console.log(payload);
  var attr = null;

  pubsubmsg(PROJECT, PUBSUB_TOPIC,attr, payload)
}

function getService() {
  return OAuth2.createService('MyPubSub')
  .setAuthorizationBaseUrl('https://accounts.google.com/o/oauth2/auth')
  .setTokenUrl('https://accounts.google.com/o/oauth2/token')
  .setClientId(CLIENT_ID)
  .setClientSecret(CLIENT_SECRET)
  .setCallbackFunction('authCallback')
  .setPropertyStore(PropertiesService.getUserProperties())
  .setScope(['https://www.googleapis.com/auth/cloud-platform','https://www.googleapis.com/auth/pubsub','https://www.googleapis.com/auth/script.external_request'])
  .setParam('access_type', 'offline')
  .setParam('approval_prompt', 'auto') // force
  .setParam('login_hint', Session.getActiveUser().getEmail());
}
function authCallback(request) {
  var service = getService();
  var isAuthorized = service.handleCallback(request);
  if (isAuthorized) {
    return HtmlService.createHtmlOutput('Success! You can close this tab.');
  } else {
    return HtmlService.createHtmlOutput('Denied. You can close this tab');
  }
}
// Reset the service
function reset() {
  var service = getService();
  service.reset();
}

/**
* Logs the redirect URI to register.
*/
function logRedirectUri() {
  var service = getService();
  Logger.log(service.getRedirectUri());
}
