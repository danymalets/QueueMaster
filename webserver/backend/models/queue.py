from django.db import models


class Queue(models.Model):
    name = models.CharField(
        verbose_name="Название очереди",
        max_length=32,
        null=True,
    )
    date = models.DateField(
        verbose_name="Дата события",
        null=True,
    )
    group = models.ForeignKey(
        'Group',
        verbose_name="Группа",
        on_delete=models.CASCADE,
        related_name="queues",
        null=True,
    )
    nums = models.CharField(
        verbose_name="Номера в очереди",
        max_length=150,
        default="[]",
    )
    users = models.ManyToManyField(
        'User',
        verbose_name="Участники очереди",
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Очередь"
        verbose_name_plural = "Очереди"
