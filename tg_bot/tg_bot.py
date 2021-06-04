from django.conf import settings
from django.http import HttpResponse
import telebot
from telebot import types
from .tgbot.state import State
from .tgbot.texts import *
from .tgbot.markups import *
import re
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from datetime import datetime, timedelta

bot = telebot.TeleBot(settings.TOKEN, threaded=True)


def main_page(request):
    return HttpResponse("Bot is running")


@csrf_exempt
def web_hook(request):
    if request.META['CONTENT_TYPE'] == 'application/json':
        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
        return HttpResponse("")
    else:
        raise PermissionDenied


@bot.message_handler(content_types=["text"])
def on_message(message):
    chat_id = message.chat.id
    name = message.chat.username
    text = message.text.strip("\n ")

    user, created = User.objects.get_or_create(
        chat_id=chat_id,
    )
    user.name = name

    if created or text == "/start":
        bot.send_message(message.chat.id, f"Бот запущен. Добро пожаловать!\n\n{get_input_name_text()}",
                         reply_markup=empty_markup)
        user.state = State.INPUT_NAME
    elif user.state == State.INPUT_NAME:
        if len(text) > 32:
            bot.send_message(message.chat.id, f"Имя слишком длинное, попробуйте еще раз",
                             reply_markup=empty_markup)
        else:
            user.display_name = text
            user.state = State.MAIN
            bot.send_message(message.chat.id, get_main_text(user), reply_markup=main_markup)
    elif user.state == State.MAIN:
        if text == "1":
            bot.send_message(message.chat.id, get_input_name_text(),
                             reply_markup=empty_markup)
            user.state = State.INPUT_NAME
        elif text == "2":
            bot.send_message(message.chat.id, f"Введите название группы, к которой хотите присоедениться",
                             reply_markup=empty_markup)
            user.state = State.GROUP_JOINING
        elif text == "3":
            bot.send_message(message.chat.id, f"Введите название группы, которую хотите создать",
                             reply_markup=empty_markup)
            user.state = State.GROUP_CREATING
        else:
            bot.send_message(message.chat.id, f"Ошибка ввода")
    elif user.state == State.GROUP_JOINING:
        try:
            group = Group.objects.get(name=text)
            bot.send_message(message.chat.id, f"Вы были успешно присоеденены к группе")
            bot.send_message(message.chat.id, get_group_text(user, group), reply_markup=group_markup)
            user.state = State.GROUP
        except Group.DoesNotExist:
            bot.send_message(message.chat.id, f"Группы с таким именем не существует")
            bot.send_message(message.chat.id, get_main_text(user), reply_markup=main_markup)
            user.state = State.MAIN
    elif user.state == State.GROUP_CREATING:
        try:
            Group.objects.get(name=text)
            bot.send_message(message.chat.id, f"Группа с таким именем уже существует",
                             reply_markup=empty_markup)
            bot.send_message(message.chat.id, get_main_text(user), reply_markup=main_markup)
            user.state = State.MAIN
        except Group.DoesNotExist:
            group = Group(
                name=text,
                admin=user,
            )
            group.save()
            user.group = group
            bot.send_message(message.chat.id, f"Группа создана", reply_markup=group_markup)
            bot.send_message(message.chat.id, get_group_text(user, group))
            user.state = State.GROUP
    elif user.state == State.GROUP:
        text = text.lower()
        del_queue_match = re.fullmatch("удалить (\d*)", text)
        if text == "создать":
            bot.send_message(message.chat.id, get_queue_create_text(), reply_markup=queue_creating_markup)
            user.state = State.QUEUE_CREATING
            pass
        elif text == "обновить":
            bot.send_message(message.chat.id, get_group_text(user, user.group))
            pass
        elif text == "выход":
            bot.send_message(message.chat.id, get_main_text(user), reply_markup=main_markup)
            user.state = State.MAIN
        elif text.isdigit() and 1 <= int(text) <= len(user.group.queues.all()):
            num = int(text)
            queue = user.group.queues.all().order_by('date')[num-1]
            user.tmp_queue = queue
            bot.send_message(message.chat.id, get_queue_text(queue), reply_markup=queue_markup)
            user.state = State.QUEUE
        elif user.group.admin == user and del_queue_match and \
                1 <= int(del_queue_match.group(1)) <= len(user.group.queues.all()):
            num = int(del_queue_match.group(1))
            queue = user.group.queues.all()[num-1]
            queue.delete()
            bot.send_message(message.chat.id, get_group_text(user, user.group), reply_markup=group_markup)
        else:
            bot.send_message(message.chat.id, f"Ошибка ввода")
    elif user.state == State.QUEUE_CREATING:
        text = text.lower()
        if text == "выход":
            bot.send_message(message.chat.id, get_group_text(user, user.group), reply_markup=group_markup)
            user.state = State.GROUP
        else:
            queue_match = re.fullmatch("([a-zа-я]+\d*)-(.*)", text)
            if queue_match:
                name = queue_match.group(1)
                date_str = queue_match.group(2)
                try:
                    date = datetime.strptime(date_str, "%d.%m.%Y").date()
                    if date < datetime.now().date():
                        bot.send_message(message.chat.id, f"Ошибка ввода. Эта дата уже прошла")
                    elif date > (datetime.now() + timedelta(days=100)).date():
                        bot.send_message(message.chat.id, f"Ошибка ввода. Пока рано "
                                                          f"создавать очередь на эту дату. ")
                    else:
                        queue = Queue(
                            name=name,
                            date=date,
                            group=user.group,
                        )
                        queue.save()
                        bot.send_message(message.chat.id, f"Очередь создана")
                        bot.send_message(message.chat.id, get_group_text(user, user.group),
                                         reply_markup=group_markup)
                        user.state = State.GROUP
                        for other in user.group.users.all():
                            if user != other:
                                bot.send_message(other.chat_id, f"Только что была создана очередь \"{queue.name}\" "
                                                                f"другим пользователем")
                except ValueError:
                    bot.send_message(message.chat.id, f"Ошибка ввода. Не удалось расспознать дату")
            else:
                bot.send_message(message.chat.id, f"Ошибка ввода")
    elif user.state == State.QUEUE:
        text = text.lower()
        if text == "записаться":
            user.tmp_queue.users.add(user)
            bot.send_message(message.chat.id, f"Готово!")
            bot.send_message(message.chat.id, get_queue_text(user.tmp_queue), reply_markup=queue_markup)
        elif text == "обновить":
            bot.send_message(message.chat.id, get_queue_text(user.tmp_queue), reply_markup=queue_markup)
        elif text == "выход":
            bot.send_message(message.chat.id, get_group_text(user, user.group), reply_markup=group_markup)
            user.state = State.GROUP
        else:
            bot.send_message(message.chat.id, "Ошибка ввода")

    user.save()


bot.remove_webhook()
bot.set_webhook(settings.DOMAIN + "/" + settings.WEB_HOOK)
