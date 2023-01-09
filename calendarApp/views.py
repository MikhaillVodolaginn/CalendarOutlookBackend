from django.shortcuts import render
from datetime import datetime, timedelta
import requests
from .models import Config
config = Config()


def index(request):
    message = config.FLOW['message']
    print(message)
    context = {'link': message[47:80], 'code': message[100:109]}
    return render(request, 'index.html', context)


def calendar(request):
    app = config.APP
    flow = config.FLOW
    access_token = app.acquire_token_by_device_flow(flow=flow)['access_token']
    headers = {'Authorization': 'Bearer ' + access_token}
    context = GetCalendarThisWeak(headers)
    return render(request, 'calendar.html', context)


def GetCalendarThisWeak(headers):
    now = datetime.fromordinal(datetime.now().toordinal())
    weak_day = datetime.weekday(now)
    start_datatime = now - timedelta(days=weak_day)
    end_datetime = now + timedelta(days=7 - weak_day)
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/me/calendarview?startdatetime={start_datatime.isoformat()}&enddatetime={end_datetime.isoformat()}",
        headers=headers)
    output = GetOutputJSON(response.json(), start_datatime)
    return output


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
