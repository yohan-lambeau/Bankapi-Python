from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from BankApi.repository.database import Base, SessionLocal


# Modèle Client
class Client(Base):
    __tablename__ = "clients"  # nom de la table dans la base

    # Schéma de la table
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # clé primaire
    nom = Column(String(length=100), index=True)                    # nom du client
    email = Column(String(length=255), unique=True, index=True)     # email unique
    date_inscription = Column(DateTime(timezone=True), server_default=func.now())

    # Persistance simple, à la manière d'un repository.save(...) en Spring
    def save(self):
        # ajoute l'instance à la session, commit, puis rafraîchit l'objet
        # pour récupérer les valeurs générées par la base comme l'id
        SessionLocal.add(self)
        SessionLocal.commit()
        SessionLocal.refresh(self)

    # Format prêt pour jsonify dans les contrôleurs
    def get_client_info(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "email": self.email,
            # str(...) évite les soucis de sérialisation de datetime
            "date_inscription": str(self.date_inscription) if self.date_inscription else None
        }
    # méthodes de classe pour les opérations de lecture

    @classmethod 
    def create_client(cls, nom: str, email: str):
        new_client = cls(nom=nom, email=email)
        SessionLocal.add(new_client)
        SessionLocal.commit()
        SessionLocal.refresh(new_client)
        return new_client


    # Lecture de tous les clients
    @classmethod
    def get_all_clients(cls):
        return SessionLocal.query(cls).all()

    # Lecture par identifiant
    @classmethod
    def get_client_by_id(cls, client_id):
        return SessionLocal.get(cls, client_id)
    
    # Lecture par email
    @classmethod
    def get_client_by_email(cls, client_email):
        return SessionLocal.query(cls).filter_by(email=client_email).first()
    
    # Suppression par identifiant
    @classmethod
    def delete_client_by_id(cls, client_id):
        client = SessionLocal.get(cls, client_id)
        if client:
            SessionLocal.delete(client)
            SessionLocal.commit()
            return True
        return False
