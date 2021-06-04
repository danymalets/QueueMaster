from backend.models.user import User
from backend.models.group import Group
from backend.models.queue import Queue
from datetime import datetime, timedelta


def get_input_name_text():
    return "Введите имя и фамилию для отображения в очередях"


def get_main_text(user: User):
    groups = user.groups.all().order_by('name')
    if groups:
        s = ""
        for i in range(len(groups)):
            s += f"{i+1}) {groups[i].name}\n"
    else:
        s = " - групп нет\n"
    return f"ГЛАВНОЕ МЕНЮ\n" \
           f"\n" \
           f"Ваше имя - \"{user.display_name}\"\n" \
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


def get_group_text(user: User, group: Group):
    queues = group.queues.all().order_by('date')
    s = ""
    cnt = 0
    for i in range(len(queues)):
        if queues[i].date < datetime.now().date():
            queues[i].delete()
            print(len(queues))
        else:
            cnt += 1
            s += f"{i+1}) {queues[i].name}-{queues[i].date.strftime('%d.%m.%Y')}"
            if queues[i].date == datetime.now().date():
                s += " (сегодня)\n"
            elif queues[i].date == (datetime.now() + timedelta(days=1)).date():
                s += " (завтра)\n"
            elif queues[i].date == (datetime.now() + timedelta(days=2)).date():
                s += " (послезавтра)\n"
            else:
                s += f"\n"
    if cnt == 0:
        s = " - очередей нет\n"
    admin_text = ""
    if group.admin == user:
        admin_text = "удалить X - удалить очередь №X\n"
    return f"Группа \"{group.name}\"\n" \
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
           f"(сегодня {datetime.now().strftime('%d.%m.%Y')})\n" \
           f"\n" \
           f"Например:\n" \
           f"исп-31.12.2021\n" \
           f"ооп2-05.01.2022\n" \
           f"\n" \
           f"выход - Вернуться в меню группы"


def get_queue_text(queue: Queue):
    users = queue.users.all()
    if users:
        s = ""
        for i in range(len(users)):
            s += f"{i+1}) {users[i].display_name} @{users[i].name}\n"
    else:
        s = " - очередь пуста\n"
    return f"Очередь \"{queue.name}-{queue.date.strftime('%d.%m.%Y')}\"\n" \
           f"Группа  \"{queue.group.name}\"\n" \
           f"\n" \
           f"{s}" \
           f"\n" \
           f"записаться - Записаться в очередь\n" \
           f"выписаться - Выписаться из очереди\n" \
           f"обновить - Обновить очередь\n" \
           f"выход - Вернуться в меню группы"
