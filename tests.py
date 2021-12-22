from unittest import TestCase
from parser import normalize_text, get_work_experience, get_frameworks, get_adjectives


class ParserTests(TestCase):
    def test_normalization(self):
        text = 'Люди любят животных'
        normalized = normalize_text(text)
        self.assertEqual(normalized, 'человек любить животное')

    def test_work_experience(self):
        text1 = 'Пятнадцать лет'
        text2 = '2 года'
        text3 = 'более 2 лет'
        text4 = 'год'
        text5 = 'нет опыта'
        text6 = 'менее двух лет'
        text7 = 'привет'
        self.assertEqual(get_work_experience(text1), 15)
        self.assertEqual(get_work_experience(text2), 2)
        self.assertEqual(get_work_experience(text3), 2.5)
        self.assertEqual(get_work_experience(text4), 1)
        self.assertEqual(get_work_experience(text5), 0)
        self.assertEqual(get_work_experience(text6), 1.5)
        self.assertEqual(get_work_experience(text7), -1)

    def test_frameworks(self):
        text1 = 'flask'
        text2 = 'джанго'
        text3 = 'Я работал со старлетте и джанго'
        text4 = 'был опыт с фласк'
        text5 = 'не работал с ними'
        self.assertListEqual(get_frameworks(text1), ['flask'])
        self.assertListEqual(get_frameworks(text2), ['django'])
        self.assertListEqual(get_frameworks(text3), ['starlette', 'django'])
        self.assertListEqual(get_frameworks(text4), ['flask'])
        self.assertListEqual(get_frameworks(text5), [])

    def test_adjectives(self):
        text = 'Я целеустремленная студент третьего курса бакалаквриата, ' \
               'обучаюсь по направлению вежливый, отличаюсь собранностью и готовностью к делу'
        self.assertListEqual(get_adjectives(text, 3), ['целеустремлённость', 'вежливость', 'собранность'])
