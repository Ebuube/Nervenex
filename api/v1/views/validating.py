#!/usr/bin/python3
import validators


def validate(req):
    """ Validate Data """

    if 'email' in req:
        if not validators.email(req['email']):
            return "Email is invalid."

    return None  # Return None when no validation issues are found
