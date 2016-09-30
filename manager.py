# coding=utf-8
import os
from flask_script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand
from shanbay import create_app, db, models
from shanbay.models import Word
import coverage
import unittest


app = create_app('dev')
manager = Manager(app)
migrate = Migrate(app, db)


def _make_context():
    return dict(app=app, db=db, models=models)

manager.add_command("db", MigrateCommand)
manager.add_command("runserver", Server(use_debugger=app.config["DEBUG"]))
manager.add_command("shell", Shell(make_context=_make_context))


@manager.command
def test():
    tests = unittest.TestLoader().discover('shanbay.tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def cov():
    cov = coverage.coverage(branch=True, include='shanbay/*') 
    cov.start()
    tests = unittest.TestLoader().discover('shanbay.tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print("coverage summary: ")
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'coverage')
    cov.html_report(directory=covdir)
    cov.erase()


@manager.command
def import_dict():
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
                print("word  {0}:{1}  is already in database. skipping...".
                      format(existed_word.word, existed_word.translation))
                continue

            word = Word(word=word,
                        translation=translation,
                        category=category)
            db.session.add(word)
            db.session.commit()

if __name__ == '__main__':
    manager.run()
