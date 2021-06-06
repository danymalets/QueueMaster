from django.db import models
from .state import State


class User(models.Model):
    chat_id = models.PositiveIntegerField(
        verbose_name="ID пользователя в тг",
        default=0,
    )
    name = models.CharField(
        max_length=32,
        verbose_name="Имя пользователя в тг",
        default="",
    )
    display_name = models.CharField(
        max_length=32,
        verbose_name="Отображаемое имя пользователя",
        default="???",
        blank=True,
    )
    cur_group = models.ForeignKey(
        'Group',
        verbose_name="Текушая группа",
        on_delete=models.SET_NULL,
        related_name="cur_users",
        null=True,
        blank=True,
    )
    cur_queue = models.ForeignKey(
        'Queue',
        verbose_name="Текушая очередь",
        on_delete=models.SET_NULL,
        related_name="cur_users",
        null=True,
        blank=True,
    )
    state = models.IntegerField(
        verbose_name="Текущее состояние чата",
        default=State.INPUT_NAME,
        choices=[
            (State.NOT_REGISTERED, "Не зарегистрирован"),
            (State.INPUT_NAME, "Ввод имени"),
            (State.MAIN, "Главное меню"),
            (State.GROUP_CREATING, "Создание группы"),
            (State.GROUP_JOINING, "Присоединение к группе"),
            (State.GROUP, "Группа"),
            (State.QUEUE_CREATING, "Создание очереди"),
            (State.QUEUE, "Очередь"),
        ]
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
