from ugc.models.user import User
from ugc.models.group import Group
from ugc.models.queue import Queue
from datetime import datetime, timedelta


def get_input_name_text():
    return "Введите имя и фамилию для отображения в очередях"


def get_main_text(user: User):
    return f"ГЛАВНОЕ МЕНЮ\n" \
           f"\n" \
           f"Ваше имя - \"{user.display_name}\"\n" \
           f"\n" \
           f"1. Изменить имя\n" \
           f"2. Присоединиться к группе\n" \
           f"3. Создать группу"


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
                s += "\n"
    if cnt == 0:
        s = " - очередей нет\n"
    admin_text = ""
    if group.admin == user:
        admin_text = "удалить X - удалить очередь X\n"
    return f"Группа \"{group.name}\"\n" \
           f"\n" \
           f"Доступные очереди (введите номер чтобы перейти):\n" \
           f"\n" \
           f"{s}" \
           f"\n" \
           f"создать - Создать очередь\n" \
           f"обновить - Обновить это меню\n" \
           f"{admin_text}" \
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
           f"обновить - Обновить очередь\n" \
           f"выход - Вернуться в меню группы"
