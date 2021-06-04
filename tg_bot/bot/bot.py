from telebot import TeleBot
from .stuff import texts, markups
from backend.models.state import State
from backend.models.user import User
from backend.models.group import Group
from backend.models.queue import Queue
from datetime import datetime, timedelta
import re


def on_message(bot: TeleBot, text: str, name: str, chat_id: int):
    text = text.strip("\n ")

    user, created = User.objects.get_or_create(
        chat_id=chat_id,
    )
    user.name = name

    if created or text == "/start":
        bot.send_message(chat_id, f"Бот запущен. Добро пожаловать!\n\n{texts.get_input_name_text()}",
                         reply_markup=markups.empty_markup)
        user.state = State.INPUT_NAME
    elif user.state == State.INPUT_NAME:
        if len(text) > 32:
            bot.send_message(chat_id, f"Имя слишком длинное, попробуйте еще раз",
                             reply_markup=markups.empty_markup)
        else:
            user.display_name = text
            user.state = State.MAIN
            bot.send_message(chat_id, texts.get_main_text(user), reply_markup=markups.main_markup)
    elif user.state == State.MAIN:
        text = text.lower()
        del_match = re.fullmatch("удалить (\d+) *", text)
        if text.isdigit() and 1 <= int(text) <= len(user.groups.all()):
            ind = int(text)
            group = user.groups.all().order_by('name')[ind - 1]
            bot.send_message(chat_id, texts.get_group_text(user, group), reply_markup=markups.group_markup)
            user.cur_group = group
            user.state = State.GROUP
        elif del_match and 1 <= int(del_match.group(1)) <= len(user.groups.all()):
            ind = int(del_match.group(1))
            group = user.groups.all().order_by('name')[ind - 1]
            group.users.remove(user)
            bot.send_message(chat_id, "Успешно удалено", reply_markup=markups.group_markup)
            bot.send_message(chat_id, texts.get_main_text(user), reply_markup=markups.main_markup)
        elif text == "изменить":
            bot.send_message(chat_id, texts.get_input_name_text(),
                             reply_markup=markups.empty_markup)
            user.state = State.INPUT_NAME
        elif text == "присоединиться":
            bot.send_message(chat_id, f"Введите название группы, к которой хотите присоединиться",
                             reply_markup=markups.empty_markup)
            user.state = State.GROUP_JOINING
        elif text == "создать":
            bot.send_message(chat_id, f"Введите название группы, которую хотите создать",
                             reply_markup=markups.empty_markup)
            user.state = State.GROUP_CREATING
        else:
            bot.send_message(chat_id, f"Ошибка ввода")
    elif user.state == State.GROUP_JOINING:
        if len(text) > 32:
            bot.send_message(chat_id, f"Слишком длинное название",
                             reply_markup=markups.empty_markup)
        else:
            try:
                group = Group.objects.get(name=text)
                bot.send_message(chat_id, f"Вы были успешно присоеденены к группе")
                bot.send_message(chat_id, texts.get_group_text(user, group), reply_markup=markups.group_markup)
                user.cur_group = group
                user.state = State.GROUP
            except Group.DoesNotExist:
                bot.send_message(chat_id, f"Группы с таким именем не существует")
                bot.send_message(chat_id, texts.get_main_text(user), reply_markup=markups.main_markup)
                user.state = State.MAIN
    elif user.state == State.GROUP_CREATING:
        if len(text) > 32:
            bot.send_message(chat_id, f"Слишком длинное название",
                             reply_markup=markups.empty_markup)
        else:
            try:
                Group.objects.get(name=text)
                bot.send_message(chat_id, f"Группа с таким именем уже существует",
                                 reply_markup=markups.empty_markup)
                bot.send_message(chat_id, texts.get_main_text(user), reply_markup=markups.main_markup)
                user.state = State.MAIN
            except Group.DoesNotExist:
                group = Group(
                    name=text,
                    admin=user,
                )
                group.save()
                group.users.add(user)
                group.save()
                user.cur_group = group
                bot.send_message(chat_id, f"Группа создана", reply_markup=markups.group_markup)
                bot.send_message(chat_id, texts.get_group_text(user, group))
                user.state = State.GROUP
    elif user.state == State.GROUP:
        text = text.lower()
        del_queue_match = re.fullmatch("удалить (\d+) *", text)
        if text == "создать":
            bot.send_message(chat_id, texts.get_queue_create_text(),
                             reply_markup=markups.queue_creating_markup)
            user.state = State.QUEUE_CREATING
            pass
        elif text == "обновить":
            bot.send_message(chat_id, texts.get_group_text(user, user.cur_group))
            pass
        elif text == "выход":
            bot.send_message(chat_id, texts.get_main_text(user), reply_markup=markups.main_markup)
            user.state = State.MAIN
        elif text.isdigit() and 1 <= int(text) <= len(user.cur_group.queues.all()):
            num = int(text)
            queue = user.cur_group.queues.all().order_by('date')[num - 1]
            user.cur_queue = queue
            bot.send_message(chat_id, texts.get_queue_text(queue), reply_markup=markups.queue_markup)
            user.state = State.QUEUE
        elif user.cur_group.admin == user and del_queue_match and \
                1 <= int(del_queue_match.group(1)) <= len(user.cur_group.queues.all()):
            num = int(del_queue_match.group(1))
            queue = user.cur_group.queues.all()[num - 1]
            queue.delete()
            bot.send_message(chat_id, texts.get_group_text(user, user.cur_group),
                             reply_markup=markups.group_markup)
        else:
            bot.send_message(chat_id, f"Ошибка ввода")
    elif user.state == State.QUEUE_CREATING:
        text = text.lower()
        if text == "выход":
            bot.send_message(chat_id, texts.get_group_text(user, user.cur_group),
                             reply_markup=markups.group_markup)
            user.state = State.GROUP
        else:
            queue_match = re.fullmatch("([a-zа-я]+\d*)-(.*)", text)
            if queue_match:
                name = queue_match.group(1)
                date_str = queue_match.group(2)
                try:
                    date = datetime.strptime(date_str, "%d.%m.%Y").date()
                    if date < datetime.now().date():
                        bot.send_message(chat_id, f"Ошибка ввода. Эта дата уже прошла")
                    elif date > (datetime.now() + timedelta(days=100)).date():
                        bot.send_message(chat_id, f"Ошибка ввода. Пока рано "
                                                  f"создавать очередь на эту дату.")
                    else:
                        queue = Queue(
                            name=name,
                            date=date,
                            group=user.cur_group,
                        )
                        queue.save()
                        bot.send_message(chat_id, f"Очередь создана")
                        bot.send_message(chat_id, texts.get_group_text(user, user.cur_group),
                                         reply_markup=markups.group_markup)
                        user.state = State.GROUP
                        for other in user.cur_group.users.all():
                            if user != other:
                                bot.send_message(other.chat_id, f"Только что в группе \"{queue.group.name}\" "
                                                                f"была создана очередь \"{queue.name}\"")
                except ValueError:
                    bot.send_message(chat_id, f"Ошибка ввода. Не удалось расспознать дату")
            else:
                bot.send_message(chat_id, f"Ошибка ввода")
    elif user.state == State.QUEUE:
        text = text.lower()
        if text == "записаться":
            if user.cur_queue.users.filter(id=user.id):
                bot.send_message(chat_id, f"Вы уже записаны в эту очередь")
            else:
                for other in user.cur_queue.cur_users.all():
                    if other.state == State.QUEUE and other != user:
                        bot.send_message(other.chat_id, f"{user.display_name} @{user.name} записался в эту очередь")
                user.cur_queue.users.add(user)
                bot.send_message(chat_id, f"Готово!")
                bot.send_message(chat_id, texts.get_queue_text(user.cur_queue),
                                 reply_markup=markups.queue_markup)
        elif text == "выписаться":
            if not user.cur_queue.users.filter(id=user.id):
                bot.send_message(chat_id, f"Вас и так нету в этой очереди")
            else:
                for other in user.cur_queue.cur_users.all():
                    if other.state == State.QUEUE and other != user:
                        bot.send_message(other.chat_id, f"{user.display_name} @{user.name} выписался из этой очереди")
                user.cur_queue.users.remove(user)
                bot.send_message(chat_id, f"Готово!")
                bot.send_message(chat_id, texts.get_queue_text(user.cur_queue),
                                 reply_markup=markups.queue_markup)
        elif text == "обновить":
            bot.send_message(chat_id, texts.get_queue_text(user.cur_queue),
                             reply_markup=markups.queue_markup)
        elif text == "выход":
            bot.send_message(chat_id, texts.get_group_text(user, user.cur_group),
                             reply_markup=markups.group_markup)
            user.state = State.GROUP
        else:
            bot.send_message(chat_id, "Ошибка ввода")

    user.save()
