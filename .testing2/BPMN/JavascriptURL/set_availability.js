var outUrl= "http://ppls-cbs.herokuapp.com/setmobil";
var idm = execution.getVariable("idMobil");
var dropLoc = execution.getVariable("dropLoc");
var dropDate = execution.getVariable("dropDate");
var stat = "booked";
var url = "http://127.0.0.1:3001/?url=" + outUrl + "?idm=" + idm + "&loc=" + dropLoc + "&date=" + dropDate + "&stat=" + stat; 
url;