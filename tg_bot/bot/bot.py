from telebot import TeleBot
from .stuff import texts, markups
from backend.models.state import State
from datetime import datetime, timedelta, time as tm
import re
import time
from threading import Thread
from .data_provider import DataProvider


def on_message(bot: TeleBot, text: str, name: str, chat_id: int):
    text = text.strip("\n ")

    user = DataProvider.get_user(chat_id)
    user['name'] = name

    if user['state'] == State.NOT_REGISTERED or text == "/start":
        bot.send_message(chat_id, f"Бот запущен. Добро пожаловать!\n\n{texts.get_input_name_text()}",
                         reply_markup=markups.empty_markup)
        user['state'] = State.INPUT_NAME
    elif user['state'] == State.INPUT_NAME:
        if len(text) > 32:
            bot.send_message(chat_id, f"Имя слишком длинное, попробуйте еще раз",
                             reply_markup=markups.empty_markup)
        else:
            user['display_name'] = text
            user['state'] = State.MAIN
            bot.send_message(chat_id, texts.get_main_text(user), reply_markup=markups.main_markup)
    elif user['state'] == State.MAIN:
        text = text.lower()
        del_match = re.fullmatch("удалить (\d+) *", text)
        if text.isdigit() and 1 <= int(text) <= len(user['groups']):
            ind = int(text)
            group = DataProvider.get_group(user['groups'][ind - 1])
            bot.send_message(chat_id, texts.get_group_text(user, group), reply_markup=markups.group_markup)
            user['cur_group'] = group['id']
            user['state'] = State.GROUP
        elif del_match and 1 <= int(del_match.group(1)) <= len(user['groups']):
            ind = int(del_match.group(1))
            group = DataProvider.get_group(user['groups'][ind - 1])
            group['users'].remove(chat_id)
            DataProvider.post_group(group)
            bot.send_message(chat_id, "Успешно удалено", reply_markup=markups.group_markup)
            bot.send_message(chat_id, texts.get_main_text(user), reply_markup=markups.main_markup)
        elif text == "изменить":
            bot.send_message(chat_id, texts.get_input_name_text(),
                             reply_markup=markups.empty_markup)
            user['state'] = State.INPUT_NAME
        elif text == "присоединиться":
            bot.send_message(chat_id, f"Введите название группы, к которой хотите присоединиться",
                             reply_markup=markups.empty_markup)
            user['state'] = State.GROUP_JOINING
        elif text == "создать":
            bot.send_message(chat_id, f"Введите название группы, которую хотите создать",
                             reply_markup=markups.empty_markup)
            user['state'] = State.GROUP_CREATING
        else:
            bot.send_message(chat_id, f"Ошибка ввода")
    elif user['state'] == State.GROUP_JOINING:
        if len(text) > 32:
            bot.send_message(chat_id, f"Слишком длинное название",
                             reply_markup=markups.empty_markup)
        else:
            group = DataProvider.get_group_by_name(text)
            if group is not None:
                bot.send_message(chat_id, f"Вы были успешно присоеденены к группе")
                bot.send_message(chat_id, texts.get_group_text(user, group), reply_markup=markups.group_markup)
                user['cur_group'] = group['id']
                user['state'] = State.GROUP
            else:
                bot.send_message(chat_id, f"Группы с таким именем не существует")
                bot.send_message(chat_id, texts.get_main_text(user), reply_markup=markups.main_markup)
                user['state'] = State.MAIN
    elif user['state'] == State.GROUP_CREATING:
        if len(text) > 32:
            bot.send_message(chat_id, f"Слишком длинное название",
                             reply_markup=markups.empty_markup)
        else:
            group = DataProvider.get_group_by_name(text)
            if group is not None:
                bot.send_message(chat_id, f"Группа с таким именем уже существует",
                                 reply_markup=markups.empty_markup)
                bot.send_message(chat_id, texts.get_main_text(user), reply_markup=markups.main_markup)
                user['state'] = State.MAIN
            else:
                group = {
                    'admin': chat_id,
                    'name': text,
                }
                DataProvider.create_group(group)
                group = DataProvider.get_group_by_name(text)
                user['cur_group'] = group['id']
                bot.send_message(chat_id, f"Группа создана", reply_markup=markups.group_markup)
                bot.send_message(chat_id, texts.get_group_text(user, group))
                user['state'] = State.GROUP
    elif user['state'] == State.GROUP:
        text = text.lower()
        del_queue_match = re.fullmatch("удалить (\d+) *", text)
        if text == "создать":
            bot.send_message(chat_id, texts.get_queue_create_text(),
                             reply_markup=markups.queue_creating_markup)
            user['state'] = State.QUEUE_CREATING
            pass
        elif text == "обновить":
            bot.send_message(chat_id, texts.get_group_text(user, user['cur_group']))
            pass
        elif text == "выход":
            bot.send_message(chat_id, texts.get_main_text(user), reply_markup=markups.main_markup)
            user['state'] = State.MAIN
        elif text.isdigit() and 1 <= int(text) <= len(DataProvider.get_group(user['cur_group'])['queues']):
            num = int(text)
            queue = DataProvider.get_queue(DataProvider.get_group(user['cur_group'])['queues'][num - 1])
            user['cur_queue'] = queue['id']
            bot.send_message(chat_id, texts.get_queue_text(queue), reply_markup=markups.queue_markup)
            user['state'] = State.QUEUE
        elif DataProvider.get_group(user['cur_group'])['admin'] == chat_id and del_queue_match and \
                1 <= int(del_queue_match.group(1)) <= len(DataProvider.get_group(user['cur_group'])['queues']):
            num = int(del_queue_match.group(1))
            queue = DataProvider.get_queue(DataProvider.get_group(user['cur_group'])['queues'][num - 1])
            # queue.delete()
            bot.send_message(chat_id, texts.get_group_text(user, DataProvider.get_group(user['cur_group'])),
                             reply_markup=markups.group_markup)
        else:
            bot.send_message(chat_id, f"Ошибка ввода")
    elif user['state'] == State.QUEUE_CREATING:
        text = text.lower()
        if text == "выход":
            bot.send_message(chat_id, texts.get_group_text(user, DataProvider.get_group(user['cur_group'])),
                             reply_markup=markups.group_markup)
            user['state'] = State.GROUP
        else:
            queue_match = re.fullmatch("([a-zа-я]+\d*)-(.*)", text)
            if queue_match:
                name = queue_match.group(1)
                date_str = queue_match.group(2)
                try:
                    q_date = datetime.strptime(date_str, "%d.%m.%Y").date()
                    if q_date < datetime.now().date():
                        bot.send_message(chat_id, f"Ошибка ввода. Эта дата уже прошла")
                    elif q_date > (datetime.now() + timedelta(days=100)).date():
                        bot.send_message(chat_id, f"Ошибка ввода. Пока рано "
                                                  f"создавать очередь на эту дату.")
                    else:
                        DataProvider.create_queue({
                            'name': name,
                            'date': q_date,
                            'group': user['cur_group'].date,
                        })
                        queue = DataProvider.get_queue()
                        bot.send_message(chat_id, f"Очередь создана")
                        bot.send_message(chat_id, texts.get_group_text(user, DataProvider.get_qroup(user['cur_group'])),
                                         reply_markup=markups.group_markup)
                        user['state'] = State.GROUP
                        for other in DataProvider.get_group(user['cur_group'])['users']:
                            if user != other:
                                bot.send_message(other.chat_id, f"Только что в группе \"{user['cur_group']}\" "
                                                                f"была создана очередь \"{name}\"")

                        def notification():
                            d = datetime.combine(q_date, tm(10, 10, 0))-datetime.now()
                            seconds = d.total_seconds()
                            if seconds < 1:
                                return
                            time.sleep(seconds)
                            for n_user in queue.users.all():
                                bot.send_message(n_user['chat_id'], f"Сегодня в группе \"{user['cur_group']}\" "
                                                                    f"будет очередь \"{name}\". Вы записаны.")

                        t = Thread(target=notification)
                        t.start()
                except ValueError:
                    bot.send_message(chat_id, f"Ошибка ввода. Не удалось расспознать дату")
            else:
                bot.send_message(chat_id, f"Ошибка ввода")
    elif user['state'] == State.QUEUE:
        text = text.lower()
        if text == "записаться":
            if chat_id in DataProvider.get_queue(user['cur_queue'])['users']:
                bot.send_message(chat_id, f"Вы уже записаны в эту очередь")
            else:
                for other in user['cur_queue']['cur_users']:
                    if other.state == State.QUEUE and other != chat_id:
                        other_o = DataProvider.get_user(other)
                        bot.send_message(other.chat_id, f"{other_o['display_name']} @{other_o['name']} записался в эту очередь")
                DataProvider.get_queue(user['cur_queue'])['users'].add(user)
                DataProvider.post_queue(user['cur_queue'])
                bot.send_message(chat_id, f"Готово!")
                bot.send_message(chat_id, texts.get_queue_text(DataProvider.get_queue(user['cur_queue'])),
                                 reply_markup=markups.queue_markup)
        elif text == "выписаться":
            if not DataProvider.get_queue(user['cur_queue'])['users'].cotains(chat_id):
                bot.send_message(chat_id, f"Вас и так нету в этой очереди")
            else:
                DataProvider.get_queue(user['cur_queue'])['users'].remove(user)
                DataProvider.post_queue(user['cur_queue'])
                bot.send_message(chat_id, f"Готово!")
                bot.send_message(chat_id, texts.get_queue_text(DataProvider.get_queue(user['cur_queue'])),
                                 reply_markup=markups.queue_markup)
        elif text == "обновить":
            bot.send_message(chat_id, texts.get_queue_text(DataProvider.get_queue(user['cur_queue'])),
                             reply_markup=markups.queue_markup)
        elif text == "выход":
            bot.send_message(chat_id, texts.get_group_text(user, DataProvider.get_group(user['cur_group'])),
                             reply_markup=markups.group_markup)
            user['state'] = State.GROUP
        else:
            bot.send_message(chat_id, "Ошибка ввода")

    print(user)
    DataProvider.post_user(user)
