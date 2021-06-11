from datetime import datetime, timedelta
from .data_provider import DataProvider


def get_input_name_text():
    return "Введите имя и фамилию для отображения в очередях"


def get_main_text(user):
    groups = user['groups']
    if groups:
        s = ""
        for i in range(len(groups)):
            s += f"{i+1}) {DataProvider.get_group(groups[i])['name']}\n"
    else:
        s = " - групп нет\n"
    return f"ГЛАВНОЕ МЕНЮ\n" \
           f"\n" \
           f"Ваше имя - \"{user['display_name']}\"\n" \
           f"\n" \
           f"Ваши группы:\n" \
           f"\n" \
           f"{s}" \
           f"\n" \
           f"Х - Перейти в группу №X из списка\n" \
           f"удалить Х - Удалить группу №Х из списка\n" \
           f"изменить - Изменить имя\n" \
           f"присоединиться - Присоединиться к группе\n" \
           f"создать - Создать группу"


def get_group_text(user, group):
    queues = group['queues']
    s = ""
    for i in range(len(queues)):
        queue = DataProvider.get_queue(queues[i])
        s += f"{i + 1}) {queue['name']}-{queue['date'].strftime('%d.%m.%Y')}"
        print("tttt")
        print(queue['date'])
        print(datetime.now().date)
        if queue['date'] == datetime.now().date():
            s += " (сегодня)\n"
        elif queue['date'] == (datetime.now() + timedelta(days=1)).date():
            s += " (завтра)\n"
        elif queue['date'] == (datetime.now() + timedelta(days=2)).date():
            s += " (послезавтра)\n"
        else:
            s += f"\n"

    if len(queues) == 0:
        s = " - очередей нет\n"
    admin_text = ""
    if group['admin'] == user['chat_id']:
        admin_text = "удалить X - удалить очередь №X\n"
    return f"Группа \"{group['name']}\"\n" \
           f"\n" \
           f"Доступные очереди:\n" \
           f"\n" \
           f"{s}" \
           f"\n" \
           f"X - перейти в очередь №X\n" \
           f"{admin_text}" \
           f"создать - Создать очередь\n" \
           f"обновить - Обновить это меню\n" \
           f"выход - Выйти из группы"


def get_queue_create_text():
    return f"Введите название очереди в следующем формате:\n" \
           f"\n" \
           f"[название предмета]-[дата ДД.ММ.ГГГГ]\n" \
           f"или\n" \
           f"[название предмета][номер подгруппы]-[дата ДД.ММ.ГГГГ]\n" \
           f"\n" \
           f"Для справки: сегодня - {datetime.now().strftime('%d.%m.%Y')}\n" \
           f"\n" \
           f"Например:\n" \
           f"исп-31.12.2021\n" \
           f"ооп2-05.01.2022\n" \
           f"\n" \
           f"выход - Вернуться в меню группы"


def get_queue_text(queue):
    users = [(queue['nums'][i], queue['users'][i]) for i in range(len(queue['nums']))]
    users.sort()
    if users:
        s = ""
        for i in range(len(users)):
            user = DataProvider.get_user(users[i][1])
            s += f"{users[i][0]}) {user['display_name']}\n"
    else:
        s = " - очередь пуста\n"
    return f"Очередь \"{queue['name']}-{queue['date'].strftime('%d.%m.%Y')}\"\n" \
           f"Группа  \"{DataProvider.get_group(queue['group'])['name']}\"\n" \
           f"\n" \
           f"{s}" \
           f"\n" \
           f"X - Занять определённое место в очереди (1-30)\n" \
           f"записаться - Записаться в очередь\n" \
           f"выписаться - Выписаться из очереди\n" \
           f"обновить - Обновить очередь\n" \
           f"выход - Вернуться в меню группы"
