from BankApi.models import Client
from BankApi.models.account_model import Account
import json 
from flask import Blueprint, request, jsonify

# Définition du blueprint pour les routes account
account_bp = Blueprint('account', __name__, url_prefix='/api')


# Routes pour les opérations sur les comptes

# Création d'un compte
@account_bp.route('/create_account', methods= ['POST'])
def create_account():
    data = json.loads(request.data) # charge les données JSON de la requête ( body )
    new_account = Account(**data)
    new_account.save()
    return jsonify(new_account.get_account_info()), 201

# Récupération de tous les comptes
@account_bp.route('/accounts', methods=['GET'])
def get_all_accounts():
    accounts = Account.get_all_accounts()
    return jsonify([account.get_account_info() for account in accounts]), 200

# Récupération d'un compte par ID
@account_bp.route('/account/<int:account_id>', methods=['GET'])
def get_account_by_id(account_id):
    account = Account.get_account_by_id(account_id)
    if account:
        return jsonify(account.get_account_info()), 200
    return jsonify({'error': 'Account not found'}), 404

# Retrait d'argent d'un compte
@account_bp.route('/withdraw', methods=['POST'])
def withdraw():
    data = json.loads(request.data)
    account_number = data.get('account_number')
    amount = data.get('amount')
    try:
        account = Account.withdraw(account_number, amount)
        return jsonify(account.get_account_info()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@account_bp.route('/deposit', methods=['POST'])
def deposit():
    data = json.loads(request.data)
    account_number = data.get('account_number')
    amount = data.get('amount')
    try:
        account = Account.deposit(account_number, amount)
        return jsonify(account.get_account_info()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Suppression d'un compte par ID
@account_bp.route('/delete_account/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    account = Account.get_account_by_id(account_id)
    if account:
        account.delete()
        return jsonify({'message': 'Account deleted successfully'}), 200
    return jsonify({'error': 'Account not found'}), 404

