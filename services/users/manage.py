# Typing imports
import typing as typ

# External imports
import click, coverage, unittest
from flask.cli import FlaskGroup
from flask import Flask

# Internal Imports
from project import create_app, db
from project.api.models import User

COV = coverage.coverage(
    branch=True, include="project/*", omit=["project/tests/*", "project/config.py"]
)
COV.start()

app = create_app()  # new
cli = FlaskGroup(create_app=create_app)  # new


@cli.command("recreate_db")
def recreate_db() -> None:
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("test")
def test() -> int:
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover("project/tests", pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command("seed_db")
def seed_db_test() -> None:
    """Runs the tests without code coverage"""
    db.session.add(User(username="mike", email="test@test.com",password="test"))
    db.session.add(User(username="fred", email="test2@test.com",password="test"))
    db.session.commit()


@cli.command("cov")
def cov() -> int:
    """Runs the unittests with coverage"""
    tests = unittest.TestLoader().discover("project/tests", pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print("Coverage Summary:")
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


if __name__ == "__main__":
    cli()
