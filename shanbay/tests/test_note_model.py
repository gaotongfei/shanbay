# coding=utf-8
import unittest
from shanbay import create_app, db
from shanbay.models import Note


class NoteModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_note_repr(self):
        note = Note(content='content')
        self.assertEqual(repr(note), "<Note 'content'>")

    def test_note_setter(self):
        note = Note(content='content')
        self.assertTrue(note.content is not None)
