from __future__ import print_function

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# A package for reading user and password from a configuration file.
import util

# cpapi is a library that handles the communication with the Check Point management server.
from cpapi import APIClient, APIClientArgs

_PORT = 20000

def add():
    username, password = util.get_credentials_access()

    client_args = APIClientArgs()

    with APIClient(client_args) as client:
        #
        # The API client, would look for the server's certificate SHA1 fingerprint in a file.
        # If the fingerprint is not found on the file, it will ask the user if he accepts the server's fingerprint.
        # In case the user does not accept the fingerprint, exit the program.
        if client.check_fingerprint() is False:
            print("Could not get the server's fingerprint - Check connectivity with the server.")
            exit(1)

        # login to server:
        login_res = client.login(username, password)

        if login_res.success is False:
            print("Login failed:\n{}".format(login_res.error_message))
            exit(1)

        for i in range(_PORT, _PORT+3000):
            add_service_response = client.api_call("add-service-tcp",
                                                {"name" : 'TCP-' + str(i),
                                                "port" : i})
            if add_service_response.success:
                print("The service: '{}' has been added successfully".format(add_service_response.data['name']))
            else:
                print("Port: '{}'\n{}".format(i, add_service_response.error_message))
                print("[{}] {}: {}".format(add_service_response.status_code, add_service_response.data['code'], add_service_response.data['message']))

        # publish the result
        publish_res = client.api_call("publish", {})
        if publish_res.success:
            print("The changes were published successfully.")
        else:
            print("Failed to publish the changes.")
