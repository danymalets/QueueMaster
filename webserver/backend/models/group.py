from django.db import models


class Group(models.Model):
    name = models.CharField(
        verbose_name="Имя группы",
        max_length=100,
        null=True
    )
    admin = models.ForeignKey(
        'User',
        verbose_name="Админ",
        on_delete=models.SET_NULL,
        related_name="administered_group",
        null=True,
    )
    users = models.ManyToManyField(
        'User',
        verbose_name="Участники группы",
        related_name="groups",
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
