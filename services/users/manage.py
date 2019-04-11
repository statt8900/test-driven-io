#Typing imports
import typing as typ

#External imports
import unittest
from flask.cli import FlaskGroup
from flask import Flask
import click
#Internal Imports
from project import create_app,db
from project.api.models import User

app = create_app()  # new
cli = FlaskGroup(create_app=create_app)  # new

@cli.command('recreate_db')
def recreate_db()->None:
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command('test')
def test()->int:
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests',pattern='test_*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command('seed_db')
def seed_db_test()->None:
    """Runs the tests without code coverage"""
    db.session.add(User(username='mike',email='test@test.com'))
    db.session.add(User(username='mike',email='test2@test.com'))
    db.session.commit()

if __name__ == '__main__':
    cli()
