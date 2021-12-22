import random

hello = 'Здравствуйте, проведем небольше интервью\n какой у вас опыт работы?'
too_small_experience = 'Извините, но это слишком маленький опыт работы :(\nБудем держаться на связи'
frameworks = 'С какими web фреймворками на python вы работали?'
missed_frameworks = 'Хм, а может вы работали с {0}?'
callback = 'Что ж, {0}!\nМы вам перезвоним в ближайшее время'
not_enough_frameworks = 'К сожалению мы ищем человека с опытом во всех этих фреймворков'
learn_frameworks = 'Думаю, разобраться с остальными не составит труда)'
tell_us_about_you = 'Расскажите подробнее о себе, меня больше интересуют Ваши soft-skills'
we_like_characteristics = 'Мы очень ценим в наших кандидатах такие качества как {0}. Soft-skills крайне важны в нашей сфере'


def gen_what():
    variants = ['Извините, я вас не понял', 'Переформулируете, пожалуйста)', 'Не понял']
    return variants[random.randint(0, len(variants) - 1)]


def gen_good():
    variants = ['Отлично', 'Супер', 'Хорошо']
    return variants[random.randint(0, len(variants) - 1)]
