# app_fastapi.py
from fastapi import FastAPI
from BankApi.fastapi_controllers.client_routes import router as client_router
from BankApi.fastapi_controllers.account_routes import router as account_router
from BankApi.fastapi_controllers.home_routes import router as home_router

# 🟢 Point d’entrée de l’application FastAPI
# C’est l’équivalent de "app = Flask(__name__)" dans Flask
app = FastAPI(
    title="Bank API",
    version="2.0.0",
    description="Version FastAPI de l'application bancaire. Documentation interactive disponible sur /docs."
)

# 🔗 Inclusion des routes (équivalent des Blueprints Flask)
app.include_router(client_router)
app.include_router(account_router)
app.include_router(home_router)

# 🧪 Route de test simple
@app.get("/ping")
def ping():
    return {"status": "ok", "message": "FastAPI fonctionne parfaitement 🚀"}

# 🚀 Commande de lancement :
# uvicorn app_fastapi:app --reload
# Accéder à la documentation interactive : http://localhost:8000/docs