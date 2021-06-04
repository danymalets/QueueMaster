from django.core.management.base import BaseCommand
from tg_bot.tg_bot import bot


class Command(BaseCommand):
    def handle(self, *args, **options):
        bot.infinity_polling()

