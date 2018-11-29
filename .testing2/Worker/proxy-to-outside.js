//for GET through proxy only
function sendRequest(requrl, callback){
    const request = require('request');
    var option = {
        url: requrl,
        proxy: 'http://gaudensiusdps:44429223@cache.itb.ac.id:8080'
    }
    request(option, (err, res, body) => {
    if (err) { return console.log(err); }
        callback(body);
    });
}

var http = require('http');
var server = http.createServer( function (req, res) {
    var reqmethod = req.method;
    console.log("Received " + reqmethod);
    console.log("Parameters: " + req.url);
    var body = "";
    req.on('data', function (data) {
        body += data;
    });
    req.on('end', function () {
        var url = req.url.substring(6, req.url.length);
        console.log("Forwarding to " + url);
        sendRequest(url, function (response){
            var jsonres = JSON.parse(response);
            console.log("Forwarded to " + url);
            console.log("Response : " + response);
            res.writeHead(200, {'Content-Type': 'application/json'});
            res.write(JSON.stringify(jsonres));
            res.end();
        });
    });
});

var port = 3001;
var host = '127.0.0.1';
server.listen(port, host);
console.log('Listening at http://' + host + ':' + port);
