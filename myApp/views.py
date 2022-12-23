from django.http import HttpResponse
from datetime import datetime, timedelta
from msal import PublicClientApplication
from myApp import config
import requests


def index(request):
    app = PublicClientApplication(
        client_id=config.CLIENT_ID,
        authority=config.AUTHORITY
    )
    flow = app.initiate_device_flow(scopes=config.SCOPE)
    print(flow['message'])

    result = app.acquire_token_by_device_flow(flow=flow)
    access_token_id = result['access_token']
    headers = {'Authorization': 'Bearer ' + access_token_id}
    print(GetCalendarThisWeak(headers))

    return HttpResponse(flow['message'])


def GetCalendarThisWeak(headers):
    now = datetime.fromordinal(datetime.now().toordinal())
    weak_day = datetime.weekday(now)
    start_datatime = now - timedelta(days=weak_day)
    end_datetime = now + timedelta(days=7-weak_day)
    response = requests.get(f"https://graph.microsoft.com/v1.0/me/calendarview?startdatetime={start_datatime.isoformat()}&enddatetime={end_datetime.isoformat()}&timezone=Asia/Yekaterinburg", headers=headers)
    print(response)
    calendar = GetOutputJSON(response.json(), start_datatime)
    return calendar


def GetOutputJSON(content, start_datatime):
    output_json = {"name": "Оранжевая переговорка", "calendar": []}
    for i in range(0, 7):
        current_day = start_datatime + timedelta(days=i)
        current_day_str = str(current_day).partition(' ')[0]
        meetings = []
        for value in content["value"]:
            current_start = value["start"]["dateTime"].partition('T')
            current_start_day = current_start[0]
            if current_start_day > current_day_str:
                break
            if current_start_day == current_day_str:
                body_preview = value["bodyPreview"]
                name = ''
                phone = ''
                for j in range(0, len(body_preview)):
                    if body_preview[j].isdigit():
                        phone = body_preview[j:]
                        break
                    name += body_preview[j]
                meetings.append({
                    "start": current_start[2][0:5],
                    "end": value["end"]["dateTime"].partition('T')[2][0:5],
                    "name": name.strip(),
                    "phone": phone
                })
        current_day_obj = {"date": current_day_str, "meetings": meetings}
        output_json["calendar"].append(current_day_obj)
    print(output_json)
    return output_json
