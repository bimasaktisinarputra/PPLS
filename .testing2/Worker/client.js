const request = require('request');

//Connect to outside

// var option = {
//     url: 'http://ppls-cbs.herokuapp.com/mobil?loc=Bandung&date=15%2F09%2F2019+00%3A00%3A00',
//     proxy: 'http://gaudensiusdps:44429223@cache.itb.ac.id:8080',
//     json: true
// }

// request(option, (err, res, body) => {
//   if (err) { return console.log(err); }
//   console.log(body);
// });

//Connect to camunda via localhost

var message = {
  "messageName" : "query-search",
  "processVariables" : {
    "FormLoc": {"value":"Bandung", "type":"String"}, 
    "FormDate": {"value":"15%2F09%2F2019+00%3A00%3A00", "type":"String"}
  },
  "resultEnabled" : true
}

request({
    url: "http://localhost:8080/engine-rest/message",
    method: "POST",
    json: true,   // <--Very important!!!
    body: message
}, function (error, response, body){
    console.log(body);
});