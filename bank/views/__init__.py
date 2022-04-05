from flask import request, make_response, jsonify, abort

from models.accountmodel import accounts
from models.cardmodel import cards

class Views(object):
        
    @staticmethod
    def get_data():
        data = request.get_json()
        if data is not request.get_json:
            data = request.get_json(force=True)
        return data
    

    @staticmethod
    def destroy_lists():
        accounts.clear()
        cards.clear()
        return make_response(jsonify({"message":"Done", "status" : 200}))