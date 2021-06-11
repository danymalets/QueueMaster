from django.shortcuts import render
from rest_framework import status
from django.http import HttpResponse
from rest_framework import generics
from .models.user import User
from .models.group import Group
from .models.queue import Queue
from django.http import JsonResponse
from rest_framework.response import Response
from datetime import datetime


class GetOrCreateUser(generics.CreateAPIView):
    def get(self, request, pk):
        user, created = User.objects.get_or_create(chat_id=pk)
        return JsonResponse({
            'chat_id': pk,
            'name': user.name,
            'state': user.state,
            'display_name': user.display_name,
            'cur_group': user.cur_group.id if user.cur_group else -1,
            'cur_queue': user.cur_queue.id if user.cur_queue else -1,
            'groups': [group.id for group in user.groups.all().order_by('name')],
        })


class SaveUser(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.get(chat_id=int(data['chat_id']))
        user.name = data['name']
        user.state = data['state']
        user.display_name = data['display_name']
        user.cur_group = Group.objects.get(id=data['cur_group']) if data['cur_group'] != -1 else None
        user.cur_queue = Queue.objects.get(id=data['cur_queue']) if data['cur_queue'] != -1 else None
        user.save()
        return HttpResponse('')


class GetGroup(generics.CreateAPIView):
    def get(self, request, pk):
        group, created = Group.objects.get_or_create(id=pk)
        for queue in group.queues.all():
            if queue.date < datetime.now().date():
                queue.delete()
        group.save()
        return JsonResponse({
            'id': pk,
            'admin': group.admin.chat_id,
            'name': group.name,
            'queues': [queue.id for queue in group.queues.all().order_by('date')],
            'users': [user.chat_id for user in group.users.all()],
        })


class GetGroupByName(generics.CreateAPIView):
    def get(self, request, name):
        try:
            group = Group.objects.get(name=name)
            return JsonResponse({
                'exists': True,
                'id': group.id,
                'admin': group.admin.chat_id,
                'name': group.name,
                'queues': [queue.id for queue in group.queues.all()],
                'users': [user.chat_id for user in group.users.all()],
            })
        except Group.DoesNotExist:
            return JsonResponse({
                'exists': False
            })


class SaveGroup(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        group = Group.objects.get(id=data['id'])
        group.name = data['name']
        group.admin = User.objects.get(chat_id=data['admin'])
        group.name = data['name']
        group.users.clear()
        for chat_id in data['users']:
            group.users.add(User.objects.get(chat_id=chat_id))
        group.save()
        return HttpResponse('')


class CreateGroup(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        group = Group(
            name=data['name'],
            admin=User.objects.get(chat_id=int(data['admin'])),
        )
        group.save()
        group.users.add(User.objects.get(chat_id=int(data['admin'])))
        group.save()
        return HttpResponse('')


class GetQueue(generics.CreateAPIView):
    def get(self, request, pk):
        queue = Queue.objects.get(id=pk)
        return JsonResponse({
            'id': queue.id,
            'name': queue.name,
            'date': queue.date,
            'group': queue.group.id,
            'nums': eval(queue.nums),
            'users': [user.chat_id for user in queue.users.all()],
            'cur_users': [user.chat_id for user in queue.cur_users.all()],
        })


class GetQueueByName(generics.CreateAPIView):
    def get(self, request, name, date, group):
        try:
            queue = Queue.objects.get(name=name,
                                      date=datetime.strptime(date, "%Y-%m-%d"),
                                      group=Group.objects.get(id=group))
            return JsonResponse({
                'exists': True,
                'id': queue.id,
                'name': queue.name,
                'date': queue.date,
                'group': queue.group.id if queue.group else None,
                'nums': eval(queue.nums),
                'users': [user.chat_id for user in queue.users.all()],
                'cur_users': [user.chat_id for user in queue.cur_users.all()],
            })
        except Queue.DoesNotExist:
            return JsonResponse({
                'exists': False
            })


class SaveQueue(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        queue = Queue.objects.get(id=int(data['id']))
        queue.name = data['name']
        queue.date = datetime.strptime(data['date'], "%Y-%m-%d")
        queue.group = Group.objects.get(id=data['group']) if data['group'] != -1 else None
        queue.users.clear()
        for chat_id in data['users']:
            queue.users.add(User.objects.get(chat_id=chat_id))
        queue.nums = str(data['nums'])
        queue.save()
        return HttpResponse('')


class CreateQueue(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        queue = Queue(
            name=data['name'],
            date=datetime.strptime(data['date'], "%Y-%m-%d"),
            group=Group.objects.get(id=data['group']),
            nums=str([])
        )
        queue.save()
        return HttpResponse('')
