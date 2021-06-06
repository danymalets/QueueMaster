import requests
from datetime import datetime


class DataProvider(object):
    url = 'http://0.0.0.0:8000'

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
        if response.status_code == 404:
            return None
        else:
            return response.json()

    @classmethod
    def post_queue(cls, data):
        requests.post(url=(cls.url + '/api/savequeue'), json=data)

    @classmethod
    def get_queue(cls, q_id):
        response = requests.get(url=(cls.url + '/api/getqueue/' + str(q_id)))
        data = response.json()
        data['date'] = datetime.strptime(data['date'], "%Y-%m-%d")
        return data

    @classmethod
    def create_queue(cls, data):
        requests.post(url=(cls.url + '/api/createqueue'), json=data)

