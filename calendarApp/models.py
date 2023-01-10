from datetime import tzinfo, timedelta

from django.db import models
from msal import PublicClientApplication


class Config:
    CLIENT_ID = '4d76c578-e336-4d69-ae97-7489722340d2'  # your application's CLIENT_ID
    AUTHORITY = 'https://login.microsoftonline.com/common'
    SCOPE = ['User.Read', 'Calendars.ReadWrite']
    APP = PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY)
    FLOW = APP.initiate_device_flow(scopes=SCOPE)
    ACCESS_TOKEN = ''


class Calendars:
    orange = {'name': 'Оранжевая переговорка', 'id': ''}
    green = {'name': 'Зеленая переговорка', 'id': ''}
    red = {'name': 'Красная переговорка', 'id': ''}
    yellow = {'name': 'Желтая переговорка', 'id': ''}
