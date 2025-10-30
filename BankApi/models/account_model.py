from sqlalchemy import Column, ForeignKey, Integer, String, Float
# from sqlalchemy.sql import func
from BankApi.repository.database import Base, SessionLocal
from BankApi.models.client_model import Client

# Modèle Account
class Account(Base):
    __tablename__ = "accounts"  # nom de la table dans la base

    # Schéma de la table
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)  # clé primaire
    client_id = Column(Integer, ForeignKey("clients.id"))  # identifiant du client (clé étrangère)
    account_number = Column(String(35), unique=True, index=True)  # numéro de compte unique
    balance = Column(Float, default=0.0)  # solde du compte

    # Persistance simple, à la manière d'un repository.save(...) en Spring
    def save(self):
        SessionLocal.add(self)
        SessionLocal.commit()
        SessionLocal.refresh(self)

    # Format prêt pour jsonify dans les contrôleurs
    def get_account_info(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "account_number": self.account_number,
            "balance": self.balance,
        }

    # méthodes de classe pour les opérations de lecture
    @classmethod
    def get_all_accounts(cls):
        return SessionLocal.query(cls).all()

    @classmethod
    def get_account_by_id(cls, account_id):
        return SessionLocal.get(cls, account_id)
    
    @classmethod
    def get_account_by_number(cls, account_number):
        return SessionLocal.query(cls).filter_by(account_number=account_number).first()
    
    @classmethod
    def delete_account_by_id(cls, account_id):
        account = SessionLocal.get(cls, account_id)
        if account:
            SessionLocal.delete(account)
            SessionLocal.commit()
            return True
        return False
    
    @classmethod
    def withdraw(cls, account_number: str, amount: Float):
        account = cls.get_account_by_number(account_number)
        if account:
            if amount <= 0:
                raise Exception("Le montant du retrait doit être positif.")
            if amount > account.balance:
                raise Exception("Fonds insuffisants pour ce retrait.")
            account.balance -= amount
            SessionLocal.commit()
            return account
        raise Exception("Compte non trouvé.")
    
    @classmethod
    def deposit(cls, account_number: str, amount: Float):
        account = cls.get_account_by_number(account_number)
        if account:
            if amount <= 0:
                raise Exception("Le montant du dépôt doit être positif.")
            account.balance += amount
            SessionLocal.commit()
            return account
        raise Exception("Compte non trouvé.")
    
    @classmethod
    def get_balance(cls, account_number: str):
        account = cls.get_account_by_number(account_number)
        if account:
            return account.balance
        raise Exception("Compte non trouvé.")
    
    @classmethod
    def create_account_for_client(cls, client_id: int, account_number: str, initial_balance: Float = 0):
        client = Client.get_client_by_id(client_id)
        if not client:
            raise Exception("Client non trouvé.")
        new_account = cls(client_id=client_id, account_number=account_number, balance=initial_balance)
        new_account.save()
        return new_account
