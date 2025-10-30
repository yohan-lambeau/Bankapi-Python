from flask import Flask
from BankApi.controllers.client_controllers import client_bp
from BankApi.controllers.home_controllers import home_bp
from BankApi.controllers.account_controllers import account_bp
from BankApi.repository.database import Base, engine


# Fonction de création de l'application Flask
def create_app():
    app = Flask(__name__)
    app.register_blueprint(client_bp) # declare les routes du client
    app.register_blueprint(home_bp)  # <-- Important : enregistre le blueprint home
    app.register_blueprint(account_bp)  # declare les routes du account

    # Crée les tables dans la base de données si elles n'existent pas
    from BankApi.models.client_model import Client  # Assure-toi d'importer les modèles nécessaires
    from BankApi.models.account_model import Account  # Assure-toi d'importer les modèles nécessaires
    Base.metadata.create_all(bind=engine)
    return app

# Point d'entrée de l'application
app = create_app()

