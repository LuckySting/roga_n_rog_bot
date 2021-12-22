from enum import Enum

import telebot

from telebot.types import Message
import phrases
import parser

bot = telebot.TeleBot('2045363317:AAHvm1YdkZytOuH5W93ouOXIMWg3rajj2KU')


class Cases(Enum):
    HELLO = 'HELLO'
    EXPERIENCE = 'EXPERIENCE'
    FRAMEWORKS = 'FRAMEWORKS'
    OTHER_FRAMEWORKS = 'OTHER_FRAMEWORKS'
    TELL_US_ABOUT_YOU = 'TELL_US_ABOUT_YOU'
    END = 'END'


current_case = Cases.HELLO


@bot.message_handler(content_types=['text'])
def get_text_messages(message: Message):
    print(f'{message.from_user.full_name} :', message.text)
    global current_case
    if message.text == '/start':
        current_case = Cases.EXPERIENCE
        bot.send_message(message.from_user.id, phrases.hello)
        return

    if current_case is Cases.EXPERIENCE:
        years = parser.get_work_experience(message.text)
        if -1 < years < 2:
            bot.send_message(message.from_user.id, phrases.too_small_experience)
            current_case = Cases.END
        elif years >= 2:
            bot.send_message(message.from_user.id, phrases.gen_good())
            current_case = Cases.FRAMEWORKS
            bot.send_message(message.from_user.id, phrases.frameworks)
        else:
            bot.send_message(message.from_user.id, phrases.gen_what())
        return

    if current_case is Cases.FRAMEWORKS:
        frameworks = parser.get_frameworks(message.text)
        missed_frameworks = list(filter(lambda f: f not in frameworks, ['flask', 'django', 'starlette', 'fastapi']))
        if len(missed_frameworks) == 0:
            bot.send_message(message.from_user.id, phrases.gen_good())
        else:
            answer = phrases.missed_frameworks.format(', '.join(missed_frameworks))
            bot.send_message(message.from_user.id, answer)
            current_case = Cases.OTHER_FRAMEWORKS
        return

    if current_case is Cases.OTHER_FRAMEWORKS:
        other_frameworks = parser.get_frameworks(message.text)
        answer = parser.get_yes_no(message.text)
        if answer is None and len(other_frameworks) == 0:
            bot.send_message(message.from_user.id, phrases.gen_what())
        if answer or len(other_frameworks) > 0:
            bot.send_message(message.from_user.id, phrases.gen_good())
            if len(other_frameworks) > 0:
                bot.send_message(message.from_user.id, phrases.learn_frameworks)
            bot.send_message(message.from_user.id, phrases.tell_us_about_you)
            current_case = Cases.TELL_US_ABOUT_YOU
        else:
            bot.send_message(message.from_user.id, phrases.not_enough_frameworks)
            current_case = Cases.END
        return

    if current_case is Cases.TELL_US_ABOUT_YOU:
        good_characteristics = parser.get_adjectives(message.text)
        if len(good_characteristics) > 0:
            bot.send_message(message.from_user.id,
                             phrases.we_like_characteristics.format(' и '.join(good_characteristics)))
        bot.send_message(message.from_user.id, phrases.callback.format(phrases.gen_good()))
        current_case = Cases.END
        return


bot.polling(none_stop=True, interval=0)
