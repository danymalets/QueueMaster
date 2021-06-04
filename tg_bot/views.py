import config
from django.http import HttpResponse
import telebot
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from .tg_bot import bot


def main_page(request):
    return HttpResponse("Bot is running")


@csrf_exempt
def web_hook(request):
    if request.META['CONTENT_TYPE'] == 'application/json':
        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
        return HttpResponse("")
    else:
        raise PermissionDenied


if config.USE_WEB_HOOK:
    bot.remove_webhook()
    bot.set_webhook(config.DOMAIN + "/" + config.WEB_HOOK)


