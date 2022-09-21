import requests
import json
import time
import sys
import argparse


# This class should not use models so that client-server structure is separated

BASE_URL = ""

choices_list = {
    "type": "list",
    "name": "choice",
    "message": "What would you like to do?",
    "choices": ["Increase", "Decrease", "Log out"],
}

final_list = {
    "type": "list",
    "name": "choice",
    "message": "What would you like to do?",
    "choices": ["Log in again", "Quit"],
}

login_questions = [
    {"type": "input", "message": "ID", "name": "id"},
    {"type": "input", "message": "Password", "name": "password"}
]

amount_questions = [
    {"type": "input", "message": "Amount", "name": "amount"}
]


def login_client(id, password):
    public_key = get_public_key()
    # TODO: encrypt data using public (Giaco)
    response = requests.post(BASE_URL + "/login-client", data={"id": id, "password": password})
    print(response.json())
    return response.json()


def logout_client(id):
    public_key = get_public_key()
    # TODO: encrypt data using public (Giaco)
    response = requests.delete(BASE_URL + "/logout-client", data={"id": id})
    print(response.json())
    return response


def increase_counter(id, amount):
    public_key = get_public_key()
    # TODO: encrypt data using public (Giaco)
    response = requests.post(BASE_URL + "/increase-counter", data={"id": id, "amount": amount})
    print(response.json())
    return response


def decrease_counter(id, amount):
    public_key = get_public_key()
    # TODO: encrypt data using public (Giaco)
    response = requests.post(BASE_URL + "/decrease-counter", data={"id": id, "amount": amount})
    print(response.json())
    return response


def get_public_key():
    response = requests.get(BASE_URL + "/public-key/")
    return response.json()


def initialize_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file')
    return vars(parser.parse_args())


# python client.py --file data.json
if __name__ == "__main__":
    # source: https://www.geeksforgeeks.org/read-json-file-using-python/
    # Opening JSON file
    try:
        args = initialize_argparse()
        file = open('./data/'+args['file'])
        data = json.load(file)
    except Exception:
        sys.exit("Error: Invalid JSON file provided.")

    try:
        BASE_URL = 'http://' + data["server"]["ip"] + ':' + data["server"]["port"]
        print(BASE_URL)
        user_id = data["id"]
        password = data["password"]
        delay = int(data["actions"]["delay"])
    except KeyError:
        sys.exit("Error: Input file does not contain right input format.")

    result = login_client(user_id, password)
    if result['result'] == 'fail':
        sys.exit('Error: Invalid combination of password and user ID.')

    # loop throw actions
    for step in data["actions"]["steps"]:
        if "INCREASE" in step:
            new_casted_amount = step.replace("INCREASE ", "")
            increase_counter(user_id, new_casted_amount)

        if "DECREASE" in step:
            new_casted_amount = step.replace("DECREASE ", "")
            decrease_counter(user_id, new_casted_amount)

        time.sleep(delay)
    logout_client(user_id)
    file.close()
