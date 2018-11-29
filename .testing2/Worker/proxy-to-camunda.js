//for POST and GET to Camunda via localhost only
function sendRequest(message, requrl, reqmethod, callback){
    const request = require('request');
    if (reqmethod == "POST"){
        request({
            url: requrl,
            method: "POST",
            json: true,    //<--Very important!!!
            body: message
        }, function (error, response, body){
            callback(body);
        }); 
    } else if (reqmethod == "GET"){
        var option = {
            url: requrl,
            //proxy: 'http://gaudensiusdps:44429223@cache.itb.ac.id:8080',
            json: true
        }
        request(option, (err, res, body) => {
        if (err) { return console.log(err); }
            callback(body);
        });
    }
}

var http = require('http');
var server = http.createServer( function (req, res) {
    var reqmethod = req.method;
    console.log("Received " + reqmethod);
    var body = "";
    req.on('data', function (data) {
        body += data;
    });
    req.on('end', function () {
        var jsonbody = JSON.parse(body);
        var message = JSON.stringify(jsonbody.json);
        var url = jsonbody.url;
        console.log("Message: " + message);
        console.log("Forwarding to " + jsonbody.url);
        sendRequest(jsonbody.json, url, reqmethod, function (response){
            console.log("Forwarded to " + url);
            console.log("Response : " + JSON.stringify(response));
            res.writeHead(200, {'Content-Type': 'application/json'});
            res.write(JSON.stringify(response));
            res.end();
        });
    });
});

var port = 3000;
var host = '127.0.0.1';
server.listen(port, host);
console.log('Listening at http://' + host + ':' + port);
