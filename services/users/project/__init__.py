#Typing imports
import typing as typ

#External imports
from flask import Flask, jsonify

#Internal Imports


# instantiate the app
app = Flask(__name__)


# set configuration
app.config.from_object('project.config.DevelopmentConfig')

@app.route('/users/ping', methods = ('GET',))
def ping_pong()->str:
    return jsonify({
        'status': 'success',
        'message' : 'pong'
    })
