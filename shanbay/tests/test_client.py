# coding=utf-8
import unittest
from shanbay import create_app, db
from flask import url_for
from flask_login import current_user
from shanbay.models import User


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
        response = self.client.post(url_for('account.signup'), data={
            'username': username,
            'password': password,
            'email': email
        })
        self.assertTrue(response.status_code == 302)

        # login test
        with self.client:
            response = self.client.post(url_for('account.login'), data={
                'username': username,
                'password': password
            }, follow_redirects=True)
            # self.assertTrue(b'Hi username' in response.data)
            self.assertTrue(bytes('你是新新新新, 新来的吧, 来<a href="/settings">设置</a>每日计划吧',
                                  encoding='utf8') in response.data)
            self.assertEqual(current_user.username, 'username')

            # ...
            self.test_index_page(is_login=True)
            self.test_index_page(method='POST')

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

