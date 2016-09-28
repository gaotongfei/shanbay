import os
from flask_script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand
from shanbay import create_app, db, models
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
def words():
    pass

if __name__ == '__main__':
    manager.run()
