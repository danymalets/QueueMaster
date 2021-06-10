from django.db import models


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
        default=1,
        choices=[
            (0, "Не зарегистрирован"),
            (1, "Ввод имени"),
            (2, "Главное меню"),
            (3, "Создание группы"),
            (4, "Присоединение к группе"),
            (5, "Группа"),
            (6, "Создание очереди"),
            (7, "Очередь"),
        ]
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
