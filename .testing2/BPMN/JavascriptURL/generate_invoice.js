var outUrl= "http://ppls-cbs.herokuapp.com/geninv";
var idm = execution.getVariable("idMobil");
var idp = execution.getVariable("idPenumpang");
var dropDate = execution.getVariable("dropDate");
var url = "http://127.0.0.1:3001/?url=" + outUrl + "?idm=" + idm + "&idp=" + idp + "&date=" + dropDate; 
url;