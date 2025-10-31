# BankApi/repository/database.py
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
import os

# --- Base MySQL (principale) ---
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

MYSQL_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# moteur + base
MYSQL_engine = create_engine(MYSQL_DATABASE_URL, pool_pre_ping=True, echo=False)
MYSQLBase = declarative_base()

# session
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=MYSQL_engine)
)

# ⚙️ Alias rétro-compatibles (pour que vos modèles existants continuent d'importer Base/engine)
Base = MYSQLBase
engine = MYSQL_engine

# Dépendance FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Création des tables au démarrage
def init_db():
    # Importer les modèles AVANT create_all
    from BankApi.models import client_model, account_model  # noqa: F401
    Base.metadata.create_all(bind=engine)

    # (optionnel) test de connexion
    with engine.begin() as conn:
        conn.execute(text("SELECT 1"))

# --- (Optionnel) Base SQLite secondaire, à activer plus tard ---
# SQLITE_DATABASE_URL = "sqlite:///./bank.db"
# sqlite_engine = create_engine(SQLITE_DATABASE_URL, connect_args={"check_same_thread": False})
# SQLiteBase = declarative_base()
# SQLiteSession = scoped_session(sessionmaker(bind=sqlite_engine))
# def get_sqlite_db():
#     db = SQLiteSession()
#     try:
#         yield db
#     finally:
#         db.close()
