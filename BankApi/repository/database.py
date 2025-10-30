from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import os

# URL de connexion (SQLite locale FASTAPI - pour tests rapides)
# SQLALCHEMY_DATABASE_URL = "sqlite:///./bank.db"

# Création du moteur fastAPI
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     connect_args={"check_same_thread": False}  # requis pour SQLite
# )


# Chargement des variables d'environnement pour la configuration de la base de données MySQL (si utilisation wamp)
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Classe de base pour tous les modèles SQLAlchemy
Base = declarative_base()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,   # meilleur handling des connexions mortes
    echo=False            # mets True pour voir les SQL dans la console
)



# Fabrique de sessions
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

# Optionnel : fonction utilitaire (utile pour l'injecter dans d'autres modules)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# fonction pour créer les tables
def init_db():
    # 🔴 IMPORTANT : importer les modèles qui héritent de `Base`
    # avant d’appeler create_all, sinon SQLAlchemy “n connaît” aucune table.
    from BankApi.models import client_model, account_model  # noqa: F401
    Base.metadata.create_all(bind=engine)

    # (Optionnel) tester la connexion
    with engine.begin() as conn:
        conn.execute(text("SELECT 1"))