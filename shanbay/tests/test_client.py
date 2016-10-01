# coding=utf-8
import unittest
from shanbay import create_app, db
from flask import url_for
from flask_login import current_user
from shanbay.models import User, Word
import os


class ClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_signup_login(self, username='username', password='password', email='email@test.com'):
        response = self.client.get(url_for('account.signup'))
        self.assertTrue(bytes('注册', encoding='utf8') in response.data)

        response = self.client.get(url_for('account.login'))
        self.assertTrue(bytes('登录', encoding='utf8') in response.data)

        # post signup form data
        response = self.client.post(url_for('account.signup'), data={
            'username': username,
            'password': password,
            'email': email
        })
        self.assertTrue(response.status_code == 302)

        # post login form data
        with self.client:
            response = self.client.post(url_for('account.login'), data={
                'username': username,
                'password': password
            }, follow_redirects=True)
            self.assertTrue(bytes('你是新新新新, 新来的吧, 来<a href="/settings">设置</a>每日计划吧',
                                  encoding='utf8') in response.data)
            self.assertEqual(current_user.username, 'username')

            # index page test when user authentication needed
            self.test_index_page(is_login=True)
            self.test_index_page(method='POST')

            # settings page
            self.test_settings_page(is_login=True, method='GET')
            self.test_settings_page(is_login=True, method='POST')

            # review page test when user authentication needed
            self.test_review_page(is_login=True)

            # test logout
            response = self.client.get('/logout', follow_redirects=True)
            self.assertTrue(current_user.is_anonymous)
            self.assertTrue(b'Hi there' in response.data)

    def test_index_page(self, is_login=False, method='GET'):
        if method == 'GET':
            response = self.client.get(url_for('main.index'))
            if not is_login:
                self.assertTrue(b'Hi there' in response.data)
            else:
                self.assertTrue(b'Hi username' in response.data)
        elif method == 'POST':
            words_per_day = 5
            response = self.client.post(url_for('main.index'), data={
                'words_per_day': words_per_day
            })
            self.assertTrue(bytes('<h2>今日' + str(words_per_day) + '个单词任务完成, 客官要再来一斤吗? '
                                  '<a href="/review">再来一斤</a></h2>', encoding='utf8') in response.data)

    def test_review_page(self, is_login=False):
        response = self.client.get(url_for('main.review'))
        if not is_login:
            # when user is not logged in, it will redirect it to main view
            self.assertEqual(response.status_code, 302)
        else:
            self.assertTrue(bytes('认识', encoding='utf8') in response.data)

    def test_settings_page(self, is_login=False, words_per_day=5, method='GET'):
        # import dict data
        if not is_login:
            response = self.client.get('/settings')
            self.assertEqual(response.status_code, 302)
        else:
            self.import_dict()
            if method == 'GET':
                response = self.client.get('/settings')
                self.assertTrue(b'<label class="control-label" for="words_per_day">words per day</label>'
                                in response.data)
            elif method == 'POST':
                self.client.post('/settings', data={
                    'words_per_day': words_per_day,
                    'category': 'cet4'
                }, follow_redirects=True)

                user = User.query.filter_by(username=current_user.username).first()
                user_words = user.words.all()
                self.assertTrue(user_words)

    def import_dict(self):
        print('importing dict data to database')
        files = filter(lambda x: not x.startswith('.'), os.listdir('wordlist'))
        if isinstance(files, filter):
            files = list(files)
        for f in files:
            with open(os.path.join('wordlist', f), 'r') as words_file:
                words = words_file.readlines()
            words_list = [(i[0], i[1].strip()) for i in [str(word).split('\t') for word in words]]

            for w in words_list:
                word = w[0]
                translation = w[1]
                category = f.split('.')[0]

                # check if the word exists in :word: table before insert
                existed_word = Word.query.filter_by(word=word).first()
                if existed_word:
                    continue

                word = Word(word=word,
                            translation=translation,
                            category=category)
                db.session.add(word)
                db.session.commit()
