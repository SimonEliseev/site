# -*- coding: utf-8 -*-
from lektor.pluginsystem import Plugin

from telegram.ext import Updater


class TelegramApiPlugin(Plugin):
    name = 'telegram_api'
    description = u'Here we get number of members in our chat.'

    def on_setup_env(self, **extra):
        self.env.jinja_env.globals.update(
            members=get_count_of_members
        )


def get_count_of_members():
    updater = Updater(token='1849075565:AAFGssB-CwiLolopU1ipBRUD8m0xBRF6Esg', use_context=True)
    return updater.bot.get_chat_member_count('@it_sochi')
