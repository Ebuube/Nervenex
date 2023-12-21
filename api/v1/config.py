#!/usr/bin/python3
from decouple import config


class Config:
    SECRET_KEY = config('SECRET_KEY')
