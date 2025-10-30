
from BankApi.models import Client
import json 
from flask import Blueprint, request, jsonify

# Définition du blueprint pour les routes client
client_bp = Blueprint('client', __name__, url_prefix='/api')

# Routes pour les opérations sur les clients
@client_bp.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.get_all_clients()
    clients_info = [client.get_client_info() for client in clients]
    return jsonify(clients_info)

@client_bp.route('/client/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.get_client_by_id(client_id)
    if client:
        return jsonify(client.get_client_info())
    return jsonify({"error": "Client not found"}), 404

#creation d'un client_v1 logic dans le controller
# @client_bp.route('/add_client', methods=['POST'])
# def create_client():
#     data = json.loads(request.data)# charge les données JSON de la requête ( body )
#     new_client = Client(**data)
#     new_client.save()
#     return jsonify(new_client.get_client_info()), 201

@client_bp.route('/add_client', methods=['POST'])
def create_client():
    client= Client.create_client(
        nom=request.json['nom'],
        email=request.json['email']
    )
    return jsonify(client.get_client_info()), 201

@client_bp.route('/client/<string:client_email>', methods=['GET'])
def get_client_by_email(client_email):
    client = Client.get_client_by_email(client_email)
    if client:
        return jsonify(client.get_client_info())
    return jsonify({"error": "Client not found"}), 404