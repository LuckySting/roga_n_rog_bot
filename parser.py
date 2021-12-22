from enum import Enum
from typing import Optional, Generator
import string
import pymorphy2
from pymorphy2.analyzer import Parse
from deep_translator import GoogleTranslator
from word2number.w2n import word_to_num

morph = pymorphy2.MorphAnalyzer()
translator = GoogleTranslator('ru')


def clear_punctuation(text: str) -> str:
    for punct in string.punctuation:
        text = text.replace(punct, '')
    return text


def normalize_text(text: str) -> str:
    text = clear_punctuation(text)
    normalized_text: list[str] = []
    for word in text.split(' '):
        morphed: list[Parse] = morph.parse(word)
        normalized_text.append(morphed[0].normal_form)
    return ' '.join(normalized_text)


def get_work_experience(text: str) -> float:
    normal_text = normalize_text(text)
    if normal_text == 'год':
        return 1
    if normal_text == 'нет опыт':
        return 0
    fix = 0
    for word in text.split(' '):
        try:
            return float(word) + fix
        except:
            pass
        morphed: list[Parse] = morph.parse(word)
        if 'ADVB' in morphed[0].tag:
            if word == 'менее':
                fix = -0.5
            if word == 'более':
                fix = 0.5
            continue
        if 'NUMR' in morphed[0].tag:
            eng_word = translator.translate(morphed[0].normal_form)
            years = word_to_num(eng_word)
            return years + fix
    return -1


#  научить прощаться  и повторять вопрос

def get_frameworks(text: str) -> list:
    text = normalize_text(text)
    frameworks: list[str] = []
    for word in text.split(' '):
        normalized: list[Parse] = morph.parse(word)
        for norm_word in normalized:
            if norm_word.normal_form == 'django' or norm_word.normal_form == 'джанго':
                frameworks.append('django')
                break
            if norm_word.normal_form == 'fastapi' or norm_word.normal_form == 'фастапи':
                frameworks.append('fastapi')
                break
            if norm_word.normal_form == 'flask' or norm_word.normal_form == 'фласк':
                frameworks.append('flask')
                break
            if norm_word.normal_form == 'starlette' or norm_word.normal_form == 'старлетта':
                frameworks.append('starlette')
                break
    return frameworks


def get_yes_no(text: str) -> Optional[bool]:
    for norm_word in normalize_text(text).split(' '):
        if norm_word in ['да', 'конечно', 'разумеется']:
            return True
        if norm_word in ['нет', 'неа']:
            return False

    return None


def get_adjectives(text: str, max_words: int = 2) -> list[str]:
    text = normalize_text(text)
    good_adjectives = ['пунктуальный', 'ответственный',
                       'собранный', 'коммуникабельный',
                       'вежливый', 'сообразительный',
                       'самостоятельный', 'обучаемый',
                       'целеустремлённый', 'амбициозный'
                       ]
    similar_nouns = ['пунктуальность', 'ответственность',
                     'собранность', 'коммуникабельность',
                     'вежливость', 'сообразительность',
                     'самостоятельность', 'обучаемость',
                     'целеустремлённость', 'амбициозность'
                     ]
    res = []
    for word in text.split(' '):
        if len(res) == max_words:
            break
        if word in good_adjectives:
            res.append(similar_nouns[good_adjectives.index(word)])
        if word in similar_nouns:
            res.append(word)

    return res

# добавить поиск отрицаний
# спросить конкретно с чем работал
# выгрузить результат в консоль

