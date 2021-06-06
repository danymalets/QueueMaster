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


class GetUser(generics.CreateAPIView):
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
        user, created = User.objects.get(chat_id=data['chat_id'])
        user.name = data['name']
        user.state = data['state']
        user.display_name = data['display_name']
        user.cur_group = Group.objects.get(id=data['cur_group'])
        user.cur_queue = Queue.objects.get(id=data['cur_queue'])
        user.save()
        return HttpResponse('')


class GetGroup(generics.CreateAPIView):
    def get(self, request, pk):
        group, created = Group.objects.get_or_create(id=pk)
        return JsonResponse({
            'id': pk,
            'admin': group.admin.chat_id,
            'name': group.name,
            'queues': [queue.id for queue in group.queues.all()],
            'users': [user.id for user in group.users.all()],
        })


class GetGroupByName(generics.CreateAPIView):
    def get(self, request, name):
        try:
            group = Group.objects.get(name=name)
            return JsonResponse({
                'id': group.id,
                'admin': group.admin.chat_id,
                'name': group.name,
                'queues': [queue.id for queue in group.queues.all()],
                'users': [user.id for user in group.users.all()],
            })
        except Group.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)


class SaveGroup(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        group, created = User.objects.get(id=data['id'])
        group.name = data['name']
        group.admin = User.object.get(chat_id=data['admin'])
        group.name = data['name']
        group.queues.clear()
        for chat_id in data['users']:
            group.users.add(User.obects.get(chat_id=chat_id))
        group.save()
        return HttpResponse('')


class CreateGroup(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        group = Group(
            name=data['name'],
            admin=User.object.get(chat_id=data['admin']),
        )
        group.users.add(User.obects.get(chat_id=data['admin']))
        group.save()
        return HttpResponse('')


class GetQueue(generics.CreateAPIView):
    def get(self, request, pk):
        queue, created = Queue.objects.get_or_create(id=pk)
        return JsonResponse({
            'id': queue.id,
            'name': queue.name,
            'date': queue.date,
            'group': queue.group.id,
            'users': [user.chat_id for user in queue.users.all()]
        })


class SaveQueue(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        queue, created = User.objects.get(id=data['id'])
        queue.name = data['name']
        queue.date = datetime.strptime(data['date'], "%Y-%m-%d")
        queue.group = Group.objects.get(id=data['group'])
        queue.users.clear()
        for chat_id in data['users']:
            queue.users.add(User.objects.get(chat_id=chat_id))
        queue.save()
        return HttpResponse('')


class CreateQueue(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        queue = Queue(
            name=data['name'],
            admin=User.object.get(chat_id=data['admin']),
            date=datetime.strptime(data['date'], "%Y-%m-%d")
        )
        queue.save()
        return HttpResponse('')
