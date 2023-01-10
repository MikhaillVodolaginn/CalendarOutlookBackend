from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from .models import Config, Calendars

config = Config()
calendars = Calendars()


class Login(APIView):
    @staticmethod
    def get(request):
        if config.ACCESS_TOKEN == '':
            message = config.FLOW['message']
            print(message)
            return Response({'hasToken': 'false', 'link': message[47:80], 'code': message[100:109]})
        return Response({'hasToken': 'true'})


class Orange(APIView):
    @staticmethod
    def get(request):
        return Response(GetCalendar(calendars.orange))


class Green(APIView):
    @staticmethod
    def get(request):
        return Response(GetCalendar(calendars.green))


class Red(APIView):
    @staticmethod
    def get(request):
        return Response(GetCalendar(calendars.red))


class Yellow(APIView):
    @staticmethod
    def get(request):
        return Response(GetCalendar(calendars.yellow))


def GetCalendar(room):
    if config.ACCESS_TOKEN == '':
        app = config.APP
        flow = config.FLOW
        config.ACCESS_TOKEN = app.acquire_token_by_device_flow(flow=flow)['access_token']
        GetAllCalendars({'Authorization': 'Bearer ' + config.ACCESS_TOKEN})

    context = GetCalendarThisWeak({
        'Authorization': 'Bearer ' + config.ACCESS_TOKEN,
        'Prefer': 'outlook.timezone="Asia/Yekaterinburg"'},
        room)
    return context


def GetAllCalendars(headers):
    response = requests.get(f"https://graph.microsoft.com/v1.0/me/calendars", headers=headers)
    print(response.ok)
    for item in response.json()["value"]:
        if item["name"] == calendars.orange['name']:
            calendars.orange["id"] = item["id"]
        elif item["name"] == calendars.green['name']:
            calendars.green["id"] = item["id"]
        elif item["name"] == calendars.red['name']:
            calendars.red["id"] = item["id"]
        elif item["name"] == calendars.yellow['name']:
            calendars.yellow["id"] = item["id"]


def GetCalendarThisWeak(headers, room=calendars.orange):
    now = datetime.fromordinal(datetime.now().toordinal())
    weak_day = datetime.weekday(now)
    start_datatime = now - timedelta(days=weak_day)
    end_datetime = now + timedelta(days=7 - weak_day)
    room_id = room['id']
    response = requests.get(
        f"https://graph.microsoft.com/v1.0/me/calendars/{room_id}/calendarView?startdatetime={start_datatime.isoformat()}&enddatetime={end_datetime.isoformat()}",
        headers=headers)
    print(response.ok)
    return GetOutputDict(response.json(), start_datatime, room)


def GetOutputDict(content, start_datatime, room):
    output_dict = {"name": room['name'], "calendar": []}
    for i in range(0, 7):
        current_day = start_datatime + timedelta(days=i)
        current_day_str = str(current_day).partition(' ')[0]
        meetings = []
        print(content)
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
        output_dict["calendar"].append(current_day_obj)
    print(output_dict)
    return output_dict
