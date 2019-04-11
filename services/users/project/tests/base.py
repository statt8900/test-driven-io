#Typing imports
import typing as typ
if typ.TYPE_CHECKING:
    from flask import Flask
#External imports
from flask_testing import TestCase # type: ignore
import unittest
#Internal Imports
from project import create_app, db

app = create_app()



class BaseTestCase(TestCase):
    def create_app(self)->'Flask':
        app.config.from_object('project.config.TestingConfig')
        return app
    def setUp(self)->None:
        db.create_all()
        db.session.commit()
    def tearDown(self)->None:
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
