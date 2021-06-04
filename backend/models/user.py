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
    group = models.ForeignKey(
        'Group',
        verbose_name="Группа",
        on_delete=models.SET_NULL,
        related_name="users",
        null=True,
        blank=True,
    )
    tmp_group = models.ForeignKey(
        'Group',
        verbose_name="Текушая очередь",
        on_delete=models.SET_NULL,
        related_name="tmp_users0",
        null=True,
        blank=True,
    )
    tmp_queue = models.ForeignKey(
        'Queue',
        verbose_name="Текушая очередь",
        on_delete=models.SET_NULL,
        related_name="tmp_users",
        null=True,
        blank=True,
    )
    cur_queue = models.ForeignKey(
        'Queue',
        verbose_name="Текущая очередь",
        on_delete=models.SET_NULL,
        related_name="tmp_users2",
        null=True,
        blank=True,
    )
    state = models.IntegerField(
        verbose_name="Текущее состояние чата",
        default=State.INPUT_NAME,
        choices=[
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
