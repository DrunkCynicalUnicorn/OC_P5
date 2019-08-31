# -*- coding: utf-8 -*-

import getpass

def get_credentials():
    credentials = dict()
    credentials["login"] = input("Please enter your MySQL login : ")
    credentials["password"] = getpass.getpass(prompt="Please enter your MySQL password : ")
    return credentials
