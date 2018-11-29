import requests
import json
import urllib
import logging
from flask import Flask
from flask_spyne import Spyne
from spyne.protocol.soap import Soap11
from spyne.protocol.json import JsonDocument
from spyne.model.primitive import Unicode, Integer, AnyDict, String
from spyne.model.complex import Iterable
from suds.client import Client as SudsClient

camunda_rest_url = "http://127.0.0.1:8080/engine-rest"
camunda_message_url = camunda_rest_url + "/message"
camunda_process_url = camunda_rest_url + "/process-instance/"
camunda_proxy_url = "http://127.0.0.1:3000"
payment_url = 'http://167.205.35.211:8080/easypay/PaymentService?wsdl'

def create_variable(value, vtype):
    variable = {}
    variable["value"] = urllib.quote(value, safe='')
    variable["type"] = vtype
    return variable

def create_camunda_message(msg_name, process_variables):
    message = {}
    message["messageName"] = msg_name
    message["processVariables"] = process_variables
    message["resultEnabled"] = True
    return message

def create_camunda_message_pid(msg_name, process_variables, p_id):
    message = create_camunda_message(msg_name, process_variables)
    message["processInstanceId"] = p_id
    return message
    
def create_proxy_msg(url, jsondict):
    message = {}
    message["json"] = jsondict
    message["url"] = url
    return json.dumps(message)

def clean_json_string(jsonstr):
    jsonstr.replace("\\", "")
    jsonstr.replace("\"{", "")
    jsonstr.replace("}\"", "")
    jsonstr.replace("\"[", "")
    jsonstr.replace("]\"", "")
    return jsonstr

def send_camunda_msg(msg_name, variables):
    jsonmessage = create_camunda_message(msg_name, variables)
    message = create_proxy_msg(camunda_message_url, jsonmessage)
    print ("Sending message to Camunda at " + camunda_message_url)
    print ("Message: ")
    print (message)
    r = requests.post(camunda_proxy_url, data=message)
    response = json.loads(r.text)[0]
    print ("Sent to Camunda at " + camunda_message_url)
    print ("Response from Camunda: ")
    print (response)
    return response

def send_camunda_msg_pid(msg_name, variables, p_id):
    jsonmessage = create_camunda_message_pid(msg_name, variables, p_id)
    message = create_proxy_msg(camunda_message_url, jsonmessage)
    print ("Sending message to Camunda at " + camunda_message_url)
    print ("Message: ")
    print (message)
    r = requests.post(camunda_proxy_url, data=message)
    response = json.loads(r.text)[0]
    print ("Sent to Camunda at " + camunda_message_url)
    print ("Response from Camunda: ")
    print (response)
    return response

def get_camunda_variable(p_id, vname):
    p_var_url = camunda_process_url + p_id + "/variables/" + vname
    print ("Getting output variable from Camunda at " + p_var_url)
    r = requests.get(p_var_url)
    response = json.loads(clean_json_string(r.text))
    output = json.loads(response["value"])
    print ("Output variable:")
    print (output)
    return output

app = Flask(__name__)
spyne = Spyne(app)
class CarAvailability(spyne.Service):
    __service_url_path__ = '/request_available_cars'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()

    @spyne.srpc(Unicode, Unicode, _returns=AnyDict)
    def car_availability(pick_loc, pick_date):
        vloc = create_variable(pick_loc, "String")
        vdate = create_variable(pick_date, "String")
        variables = {}
        variables["pickLoc"] = vloc
        variables["pickDate"] = vdate
        response = send_camunda_msg("query-search", variables)
        p_id = response["processInstance"]["id"]
        output = {}
        output ["carList"] = get_camunda_variable(p_id, "carList")
        output ["processId"] = p_id
        return output

class BookCar(spyne.Service):
    __service_url_path__ = '/book_car'
    __in_protocol__ = Soap11(validator='lxml')
    __out_protocol__ = Soap11()

    @spyne.srpc(Unicode, Unicode, Unicode, Unicode, Unicode, _returns=AnyDict)
    def book_car(id_mobil, id_penumpang, drop_loc, drop_date, process_code):
        car_list = get_camunda_variable(process_code, "carList")
        v_idm = create_variable(id_mobil, "String")
        v_idp = create_variable(id_penumpang, "String")
        v_loc = create_variable(drop_loc, "String")
        v_date = create_variable(drop_date, "String")
        variables = {}
        variables["idMobil"] = v_idm
        variables["idPenumpang"] = v_idp
        variables["dropLoc"] = v_loc
        variables["dropDate"] = v_date
        response = send_camunda_msg_pid("car-detail", variables, process_code)
        invoice = get_camunda_variable(process_code, "invoice")
        invoice["price"] = 10000 # Rp 10.000,- is charged to the user for booking

        # Calling SOAP method from Payment service (EasyPay)
        client = SudsClient(url=payment_url)
        payId = client.service.beginPayment("bank_va", 10000) 
        r = client.service.getPaymentEvents(payId, 0)
        events = SudsClient.dict(r)["events"]

        # Get the VA account number from the response
        i = 0
        found = False
        va_account = None
        while i < len(events) and found is False :
            if events[i]["_type"] == "ACCOUNT_NUMBER_AVAILABLE" :
                va_account = events[i]["_accountNumber"]
                found = True
            else :
                i += 1

        # Returns the VA number designation and the price the user have to pay
        output = {}
        output["va_account"] = va_account
        output["price"] = invoice["price"]
        return output

if __name__ == '__main__':
    app.run(host = '167.205.35.227', port = 5000)
