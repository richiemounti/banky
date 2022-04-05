import copy

from flask import (
    Blueprint, request, jsonify, make_response, abort
)


bp = Blueprint('accounts', __name__)


from views import Views
from models.accountmodel import AccountModels, accounts

#create a new account
@bp.route('/v1/admin/account', methods=['POST'])
def create_account():
    try:
        data = Views.get_data()
        validateoffice(data)

        new_account = AccountModels (
            data["iban"],
            data["bankcode"],
        )
        party_exists = AccountModels.input_exists(accounts, new_account.iban)

        if party_exists:
            # pass
            res = jsonify({'status': 400, 'error': "Duplicate name error, Party {} already exists with id {}".format(
                data['iban'], party_exists), 'data': []})
            return make_response(res, 400)

        new_account.save_accounts()
        details = new_account.detail_list()

        res = jsonify({"status": 201, "data": details})
        return make_response(res, 201)
    except(ValueError, KeyError, TypeError):
        res = jsonify({"message": "missing parameters"})
        return make_response(res, 400)
    
#get accounts
@bp.route('/v1/user/account', methods=['GET'])
def accounts_list():
    return make_response(jsonify({
        "status": 200,
        "data": [accounts[x].serialize() for x in accounts]
    }), 200)

# get specific party
@bp.route('/v1/user/account/<int:x>', methods=['GET'])
def account_details(x):
    if len(accounts) == 0:
        pass
    if x in accounts:
        details = accounts[x].get_accounts()
        res = jsonify({"status": 200, "data": details})
        return make_response(res, 200)

    res = jsonify({"status": 404, "error": "Party with id {} not found".format(x)})
    return (res, 404)

# update a specific party
@bp.route('/v1/admin/account/<int:x>', methods=['PATCH'])
def party_update(x):
    data = Views.get_data()

    if x in accounts:
        accounts[x].update_name(data['name'], data['hqAddress'])
        res = jsonify({"status": 202, "data": accounts[x].detail_list()})
        return make_response(res, 202)

    res = jsonify({"status": 404, "error": "Party with id {} not found".format(x)})
    return (res, 404)

# delete a party
@bp.route('/v1/admin/account/<int:x>', methods=['DELETE'])
def party_delete(x):
    if x in accounts:
        accounts[x].delete_account()
        res = jsonify({"status": 200, "data": "Party {} deleted".format(x)})
        return (res, 200)

'''
VALIDATIONS
'''
def validateoffice(new_account):
    '''This function validates new office inputs '''
    
    account = new_account.items()
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