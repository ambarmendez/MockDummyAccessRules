from __future__ import print_function

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# A package for reading user and password from a configuration file.
import util

# cpapi is a library that handles the communication with the Check Point management server.
from cpapi import APIClient, APIClientArgs

_PORT = 20000

def add():
    username, password = util.get_access_credentials()

    client_args = APIClientArgs()

    with APIClient(client_args) as client:
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

        session_id = login_res.data['uid']

        rule_name = "WEB_API-RULE"

        for index_port in range(_PORT, _PORT+3000):
            source = 'NG-1'
            destination = 'NG-2'

            # add a rule to the top of the "Network" layer
            add_rule_response = client.api_call("add-access-rule",
                                                {"name": rule_name,
                                                "layer": "Network",
                                                "source": source,
                                                "destination": destination,
                                                "action": "Accept",
                                                "service": 'TCP-' + str(index_port),
                                                "track": {"type":"Log"},
                                                "position": "top"})

            if add_rule_response.success:
                print("Rule for port '{}' has been added successfully".format(index_port))
            else:
                print("Failed to add the access-rule: '{}', Error:\n{}".format(rule_name, add_rule_response.error_message))
                print("[{}] {}: {}".format(add_rule_response.status_code, add_rule_response.data['code'], add_rule_response.data['message']))

        print("Now, publishing the result ... REMEMBER session_id: {}!!!".format(session_id))

        # publish the result
        response = client.api_call("publish", {})
        if response.success:
            print("The changes were published successfully.")
        else:
            print("Failed to publish the changes.")

        print("Now, validating the policy ...")

        # Verifies the policy package
        response = client.api_call("verify-policy", {"policy-package" : "standard"})
        if response.success:
            print("The rule were verified successfully.\n{}".format(response.data))
        else:
            print("Failed to publish the changes.")
