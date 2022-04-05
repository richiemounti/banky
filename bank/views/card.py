import copy

from flask import (
    Blueprint, request, jsonify, make_response, abort
)


bp = Blueprint('cards', __name__)


from views import Views
from models.cardmodel import CardsModel, cards

#create a new account
@bp.route('/v1/admin/card', methods=['POST'])
def create_party():
    try:
        data = Views.get_data()
        validateoffice(data)

        new_card = CardsModel (
            data["cardalias"],
            data["cardtype"],
            data["accountid"]
        )
        card_exists = CardsModel.input_exists(cards, new_card.cardalias)

        if card_exists:
            # pass
            res = jsonify({'status': 400, 'error': "Duplicate name error, Card {} already exists with id {}".format(
                data['cardalias'], card_exists), 'data': []})
            return make_response(res, 400)

        new_card.save_cards()
        details = new_card.detail_list()

        res = jsonify({"status": 201, "data": details})
        return make_response(res, 201)
    except(ValueError, KeyError, TypeError):
        res = jsonify({"message": "missing parameters"})
        return make_response(res, 400)
    
#get accounts
@bp.route('/v1/user/card', methods=['GET'])
def cards_list():
    return make_response(jsonify({
        "status": 200,
        "data": [cards[x].serialize() for x in cards]
    }), 200)

# get specific party
@bp.route('/v1/user/card/<int:x>', methods=['GET'])
def account_details(x):
    if len(cards) == 0:
        pass
    if x in cards:
        details = cards[x].get_cards(x)
        res = jsonify({"status": 200, "data": details})
        return make_response(res, 200)

    res = jsonify({"status": 404, "error": "Card with id {} not found".format(x)})
    return (res, 404)

def get_cards(x):
    if x in cards:
        return cards[x]


# update a specific party
@bp.route('/v1/admin/card/<int:x>', methods=['PATCH'])
def cards_update(x):
    data = Views.get_data()

    if x in cards:
        cards[x].update_name(data['cardalias'])
        res = jsonify({"status": 202, "data": cards[x].detail_list()})
        return make_response(res, 202)

    res = jsonify({"status": 404, "error": "Card with id {} not found".format(x)})
    return (res, 404)

# delete a party
@bp.route('/v1/admin/card/<int:x>', methods=['DELETE'])
def party_delete(x):
    if x in cards:
        cards[x].delete_account()
        res = jsonify({"status": 200, "data": "Card {} deleted".format(x)})
        return (res, 200)

'''
VALIDATIONS
'''
def validateoffice(new_card):
    '''This function validates new office inputs '''
    
    account = new_card.items()
    required_fields = ['iban', 'bankcode']
    for key, value in account:
        # ensure keys have values
        if not value:
            return abort(make_response(jsonify({"message":"{} is lacking. it is a required field".format(key)})))
        # validate length
        if key == "iban" or key == "bankcode":
            if len(value) < 3:
                return abort(make_response(jsonify({"message":"The {} provided is too short".format(key)}), 400))
            elif len(value) > 20:
                return abort(make_response(jsonify({"message":"The {} provided is too long".format(key)}), 400))
        if key not in required_fields:
            return abort(make_response(jsonify({"message": "invalid credentials"}), 400))