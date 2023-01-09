from django.db import models
from msal import PublicClientApplication


class Config:
    CLIENT_ID = '4d76c578-e336-4d69-ae97-7489722340d2'
    AUTHORITY = 'https://login.microsoftonline.com/common'
    SCOPE = ['User.Read', 'Calendars.ReadWrite']
    APP = PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY)
    FLOW = APP.initiate_device_flow(scopes=SCOPE)
