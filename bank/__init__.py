import imp
import os
from flask import Flask, make_response, jsonify
from config import configs

from views import accounts, cards

def internal_server_error(e):
    res = jsonify(dict(
        error = "it's us not you",
        status = 500
    ))
    return make_response(res, 500)


def page_not_found(e):
    ''' handles page not found errors '''
    res = jsonify(dict(
        error = "Page not found",
        status = 404
    ))
    return make_response(res, 404)

def method_not_allowed(e):
    ''' handles method not allowed errors '''
    res = jsonify(dict(
        error = "Method not allowed",
        status = 405
    ))
    return make_response(res, 405)

def handle_bad_request(e):
    res= jsonify(dict(error= 'bad request!', status= 400))
    return make_response(res, 400)


def create_app(test_config):
    # create and configure the app
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_object(
        configs['production']
    )

    if test_config:
        app.config.from_object(configs['testing'])

    @app.route('/', methods=['GET'])
    def home():
        ''' Default route for Banky'''
        routes = []
        for route in app.url_map.iter_rules():
            routes.append(str(route))
        res = jsonify(dict(
            endpoints = routes,
            message = "Welcome to Banky",
            status = 200
        ))
        return make_response(res, 200)

    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(404, page_not_found)

    app.register_blueprint(accounts.bp)
    app.register_blueprint(cards.bp)
    
    return app