import requests
from datetime import datetime
import json


class DataProvider(object):
    url = 'http://webserver:8000'

    @classmethod
    def post_user(cls, data):
        requests.post(url=(cls.url + '/api/save-user'), json=data)

    @classmethod
    def get_user(cls, chat_id):
        response = requests.get(url=(cls.url + '/api/get-user/' + str(chat_id)))
        return response.json()

    @classmethod
    def post_group(cls, data):
        requests.post(url=(cls.url + '/api/save-group'), json=data)

    @classmethod
    def create_group(cls, data):
        requests.post(url=(cls.url + '/api/create-group'), json=data)

    @classmethod
    def get_group(cls, g_id):
        response = requests.get(url=(cls.url + '/api/get-group/' + str(g_id)))
        return response.json()

    @classmethod
    def get_group_by_name(cls, g_name):
        response = requests.get(url=(cls.url + '/api/get-group-by-name/' + g_name))
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            return None

    @classmethod
    def post_queue(cls, data):
        data['date'] = datetime.strftime(data['date'], "%Y-%m-%d")
        requests.post(url=(cls.url + '/api/save-queue'), json=data)

    @classmethod
    def get_queue(cls, q_id):
        response = requests.get(url=(cls.url + '/api/get-queue/' + str(q_id)))
        data = response.json()
        data['date'] = datetime.strptime(data['date'], "%Y-%m-%d").date()
        return data

    @classmethod
    def get_queue_by_name_and_date(cls, name, date, group):
        response = requests.get(url=(cls.url + '/api/get-queue-by-name/' + name + '/' +
                                     datetime.strftime(date, "%Y-%m-%d") + '/' + str(group)))
        data = response.json()
        if 'date' in data:
            data['date'] = datetime.strptime(data['date'], "%Y-%m-%d").date()
        return data

    @classmethod
    def create_queue(cls, data):
        data['date'] = datetime.strftime(data['date'], "%Y-%m-%d")
        requests.post(url=(cls.url + '/api/create-queue'), json=data)

