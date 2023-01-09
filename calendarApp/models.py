from django.db import models


class Config:
    def __init__(self):
        self.CLIENT_ID = '4d76c578-e336-4d69-ae97-7489722340d2'
        self.CLIENT_SECRET = 'zth8Q~8rfrO8gNHmnVSXEJWq~EEpLMkfajYRpdvB'
        self.AUTHORITY = 'https://login.microsoftonline.com/common'
        self.REDIRECT_PATH = 'http://localhost:63337/myApp/templates/index.html'
        self.SCOPE = ['User.Read', 'Calendars.ReadWrite']
