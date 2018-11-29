var request = require('request');
// const admin = require('firebase-admin');
const Client = require('camunda-external-task-client-js');
const logger = require('camunda-external-task-client-js');
// const settings = {timestampsInSnapshots: true};

// const serviceAccount = require('C:\\Users\\IRS37\\Desktop\\Camunda\\PPLS\\PPLS\\kunci.json');

// admin.initializeApp({
//     credential: admin.credential.cert(serviceAccount)
// });
// admin.firestore().settings(settings);

// var db = admin.firestore();

// configuration for the Client:
//  - 'baseUrl': url to the Process Engine
//  - 'logger': utility to automatically log important events
const config = {baseUrl: 'http://localhost:8080/engine-rest', use: logger};

// create a Client instance with custom configuration
const client = new Client(config);

client.subscribe('send-car-data', async function ({task, taskService}) {
    // Put your business logic here

    // Get a process variable
    const ploc = task.variables.get('pickLocation');
    const ptime = task.variables.get('pickDateTime');

    request('http://ppls-cbs.herokuapp.com/mobil?loc=' + ploc + '&date=' + ptime, function (error, response, body) {
        var jsonbody = JSON.parse(body);
        console.log('Cars Available :')
        console.log(jsonbody);
        taskService.complete(task);
    });
});

client.subscribe('send-car-availability', async function ({task, taskService}) {
    // Put your business logic here

    // Get a process variable
    const id = task.variables.get('id');
    const ploc = task.variables.get('dropLocation');
    const ptime = task.variables.get('droDateTime');

    // const mobilRef = db.collection("koleksimobil");

    // // Complete the task
    // mobilRef
    //     .get().then(col => {
    //     col.forEach((docs) => {
    //         let cars = docs.ref.collection("mobil");
    //         // implementasi
    //     });
    // }).catch(err => {
    //     console.log('Error', err);
    // });

    console.log(``);

    //implementasi send message

    await taskService.complete(task);
});

client.subscribe('generate-bill', async function ({task, taskService}) {
    // Put your business logic here

    // Get a process variable

    //implementasi send message

    await taskService.complete(task);
});