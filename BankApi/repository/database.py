from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


# URL de connexion (SQLite locale)
SQLALCHEMY_DATABASE_URL = "sqlite:///./bank.db"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:motdepasse@localhost:3306/bankdb"



# Classe de base pour tous les modèles SQLAlchemy
Base = declarative_base()

# Création du moteur
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # requis pour SQLite
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
