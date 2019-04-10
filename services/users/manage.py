#Typing imports
import typing as typ

#External imports
from flask.cli import FlaskGroup
from flask import Flask
import click
#Internal Imports


def create_app()->Flask:
    from project import app
    return app

@click.group(cls=FlaskGroup, create_app=create_app)
def cli()->None:
    pass


if __name__ == '__main__':
    cli()
