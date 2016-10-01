# coding=utf-8
import unittest
from shanbay import create_app, db
from shanbay.models import Word


class WordModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_word_setter(self):
        word = Word('test')
        self.assertTrue(word.word is not None)

    def test_word_repr(self):
        word = Word('test')
        self.assertEqual(repr(word), "<Word 'test'>")

    def test_word_empty(self):
        with self.assertRaises(TypeError):
            Word()

