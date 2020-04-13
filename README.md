#MockDummyAccessRules

A collection of files that add three thousands of dummy access rules.

## Description

This collection enables you to create access rules to the top of the access policy layer, publishes the changes and verifies the policy package. Everything executed over the management machine avoiding issues with the self-certificate server.

## Instructions

> *Development environment*, Python language version 2.7 and [Check Point API Python SDK](https://github.com/CheckPoint-APIs-Team/cpapi-python-sdk) as a prerequisite.

### Step 1.

Begin by clonning this repository or by clicking the Download Zip button.

Download and install the [Check Point API Python SDK](https://github.com/CheckPoint-APIs-Team/cpapi-python-sdk) repository and follow the instructions in the SDK repository

### Step 2.

Next, change the value for user and password within the `settings.file` file .

```
[server]
user = paste-username-here
passwd = paste-password-here
```

### Step 3.

Execute the command line 'python make.py -h' and follow each subcommand in the right order.
