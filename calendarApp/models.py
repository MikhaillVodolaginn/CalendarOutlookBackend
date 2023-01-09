from datetime import tzinfo, timedelta

from django.db import models
from msal import PublicClientApplication


class Config:
    CLIENT_ID = ''
    AUTHORITY = 'https://login.microsoftonline.com/common'
    SCOPE = ['User.Read', 'Calendars.ReadWrite']
    APP = PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY)
    FLOW = APP.initiate_device_flow(scopes=SCOPE)
