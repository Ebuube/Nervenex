#!/usr/bin/python3
import validators


def validate(req):
    """ Validate Data """
    if not req:
        return None

    if 'email' in req:
        if not validators.email(req['email']):
            return None
        else:
            return True

    return None  # Return None when no validation issues are found
