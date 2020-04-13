from __future__ import print_function

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# A package for reading user and password from a configuration file.
import util

# cpapi is a library that handles the communication with the Check Point management server.
from cpapi import APIClient, APIClientArgs

def add():
    username, password = util.get_credentials_access()

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

        for i in range(4):
            for j in range(1, 251):
                ip_address = '13.0.' + str(i) + '.' + str(j)
                host = {"name": 'H-' + ip_address, "ip-address": ip_address}

                add_host_response = client.api_call("add-host", host)

                if add_host_response.success:
                    print("The host: '{}' has been added successfully".format(add_host_response.data["name"]))
                else:
                    print("Failed to add-host: '{}', Error:\n{}".format(ip_address, add_host_response.error_message))

                subnet = '103.' + str(i) + '.' + str(j) + '.0'
                network = {"name" : 'N-' + subnet + '_24',
                            "subnet" : subnet,
                            "subnet-mask" : "255.255.255.0"}
                add_network_response = client.api_call("add-network", network)

                if add_network_response.success:
                    print("The network: '{}' has been added successfully".format(add_network_response.data["name"]))
                else:
                    print("Failed to add-network: '{}', Error:\n{}".format(subnet, add_network_response.error_message))

        print("Now, publishing the result ... REMEMBER session_id: {}!!!".format(session_id))

        # publish the result
        publish_res = client.api_call("publish", {})
        if publish_res.success:
            print("The changes were published successfully.")
        else:
            print("Failed to publish the changes.")
