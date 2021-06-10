import requests
from datetime import datetime
import json


class DataProvider(object):
    url = 'http://webserver:8000'

    @classmethod
    def post_user(cls, data):
        requests.post(url=(cls.url + '/api/saveuser'), json=data)

    @classmethod
    def get_user(cls, chat_id):
        response = requests.get(url=(cls.url + '/api/getuser/' + str(chat_id)))
        return response.json()

    @classmethod
    def post_group(cls, data):
        requests.post(url=(cls.url + '/api/savegroup'), json=data)

    @classmethod
    def create_group(cls, data):
        requests.post(url=(cls.url + '/api/creategroup'), json=data)

    @classmethod
    def get_group(cls, g_id):
        response = requests.get(url=(cls.url + '/api/getgroup/' + str(g_id)))
        return response.json()

    @classmethod
    def get_group_by_name(cls, g_name):
        response = requests.get(url=(cls.url + '/api/getgroupbyname/' + g_name))
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            return None

    @classmethod
    def post_queue(cls, data):
        data['date'] = datetime.strftime(data['date'], "%Y-%m-%d")
        requests.post(url=(cls.url + '/api/savequeue'), json=data)

    @classmethod
    def get_queue(cls, q_id):
        response = requests.get(url=(cls.url + '/api/getqueue/' + str(q_id)))
        data = response.json()
        data['date'] = datetime.strptime(data['date'], "%Y-%m-%d")
        return data

    @classmethod
    def get_queue_by_name_and_date(cls, name, date, group):
        response = requests.get(url=(cls.url + '/api/getqueuebynameanddate/' + name + '/' +
                                     datetime.strftime(date, "%Y-%m-%d") + '/' + str(group)))
        data = response.json()
        if 'date' in data:
            data['date'] = datetime.strptime(data['date'], "%Y-%m-%d")
        return data

    @classmethod
    def create_queue(cls, data):
        data['date'] = datetime.strftime(data['date'], "%Y-%m-%d")
        requests.post(url=(cls.url + '/api/createqueue'), json=data)

