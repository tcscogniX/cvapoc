from flask import Flask,request,jsonify
import configparser
import logging
from datetime import datetime
import requests
import json

config = configparser.ConfigParser()
config.read("D:\\Application\\CEM\\Orchestrator\\Code\\config.ini")

date_str = datetime.now().strftime(format="%d_%m_%Y")
logging.basicConfig(filename=f"./Code/Logs/orchestrator_log_{date_str}.log", filemode="a", format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger("orchestrator")

app = Flask(__name__)



@app.route('/', methods=['GET'])
def index():
    return "Welcome to Orchestrator"


#for testing of CVA team
@app.route('/get_chat_response', methods=['GET'])
def get_chat_response():
    logger.info("In method get_automatic_response_from_premap().")
    return_dict = {
        "ConvId": "",
        "CustomerId": "",
        "Response": ""
    }
    try:
        input_json_body = request.get_json(force=True)
        json_key_list = list(input_json_body.keys())
        if ("ConvId" in json_key_list) and ("CustomerId" in json_key_list) and ("Message" in json_key_list):  # check if required keys are present in request json

            # fetching conv_id, customer_id & message from request json body
            conv_id = input_json_body["ConvId"]
            customer_id = input_json_body["CustomerId"]
            message = input_json_body["Message"]

            #updating caller and customer info for return dict
            return_dict["ConvId"] = conv_id
            return_dict["CustomerId"] = customer_id
            return_dict["Response"] = "Hi caller: " + conv_id + ", your message was: " + message  # static data for testing

        else:
            raise Exception("Required keys are not present in request json")

        return jsonify(return_dict)
    except Exception as ex:
        error_message = "Some error occured. Error: " + ex.__str__()
        logger.error(error_message)
        return error_message
		
@app.route('/test_for_premap', methods=['GET'])
def test_for_premap():
    logger.info("In method test_for_premap().")
    return_dict = {
        "ConvId": "",
        "CustomerId": "",
		"MessageId": "",
        "Message": ""
    }
    try:
        input_json_body = request.get_json(force=True)
        json_key_list = list(input_json_body.keys())
        if ("ConvId" in json_key_list) and ("CustomerId" in json_key_list) and ("Message" in json_key_list):  # check if required keys are present in request json

            # fetching conv_id, customer_id & message from request json body
            conv_id = input_json_body["ConvId"]
            customer_id = input_json_body["CustomerId"]
            message = input_json_body["Message"]
            message_id = input_json_body["MessageId"]

            #updating caller and customer info for return dict
            return_dict["ConvId"] = conv_id
            return_dict["CustomerId"] = customer_id
            return_dict["MessageId"] = message_id
            return_dict["Message"] = "This is another query."

        else:
            raise Exception("Required keys are not present in request json")

        return jsonify(return_dict)
    except Exception as ex:
        error_message = "Some error occured. Error: " + ex.__str__()
        logger.error(error_message)
        return error_message


@app.route('/get_chat_response', methods=['GET'])
def get_automatic_response_from_premap():
    logger.info("In method get_automatic_response_from_premap().")
    return_dict = {
        "ConvId": "",
        "CustomerId": "",
        "Response": ""
    }
    try:
        input_json_body = request.get_json(force=True)
        json_key_list = list(input_json_body.keys())

        if ("ConvId" in json_key_list) and ("CustomerId" in json_key_list) and ("Message" in json_key_list):  # check if required keys are present in request json
            


            # fetching conv_id, customer_id & message from request json body
            conv_id = input_json_body["ConvId"]
            customer_id = input_json_body["CustomerId"]
            message = input_json_body["Message"]

            #updating caller and customer info for return dict
            return_dict["ConvId"] = conv_id
            return_dict["CustomerId"] = customer_id



            # get customer data from CRM by API call
            crm_url =  str(config["CRM"]["url"]).strip()
            try:
                payload = {
                    "customer_id": str(customer_id)
                }
                response = requests.request("GET", crm_url, data=json.dumps(payload))
                crm_response = response.json()

                if crm_response["status"] == "fail":
                    raise requests.exceptions.RequestException(crm_response["exception"])

                customer_data = crm_response["data"]

            except requests.exceptions.RequestException as ex:
                logger.error("Exception in fetching customer data from CRM API:" + ex.__str__())
                return jsonify(return_dict)



            # call PREMAP
            premap_url = str(config["PREMAP"]["url"]).strip()
            try:
                # payload = {
                #     "Customer": customer_data,
                #     "Caller": input_json_body
                # }
                # response = requests.request("GET", premap_url, data=payload)
                # premap_response = response.json()
                # if premap_response["status"] == "fail":
                #     raise requests.exceptions.RequestException(premap_response["exception"])

                # premap_data = premap_response["response"]

                # return_dict["Response"] = premap_data

                return_dict["Response"] = "Hi John, how can I help you?"  # static data for testing

            except requests.exceptions.RequestException as ex:
                logger.error("Exception in fetching customer data from PREMAP API:" + ex.__str__())
                return jsonify(return_dict)

        else:
            raise Exception("Required keys are not present in request json")

        return jsonify(return_dict)
            
    except Exception as ex:
        logger.error("Error in get_automatic_response_from_premap. Exception: " + ex.__str__())
        return jsonify(return_dict)

if __name__ == "__main__":
	print("Application is starting up") 
	app.run(port=8080, host="0.0.0.0")
