var outUrl= "http://ppls-cbs.herokuapp.com/mobil"
var loc = execution.getVariable("pickLoc");
var date = execution.getVariable("pickDate");
var url= "http://127.0.0.1:3001/?url=" + outUrl + "?loc=" + loc + "&date=" + date; 
url;
