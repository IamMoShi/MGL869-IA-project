from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:changeme@127.0.0.1:5432/web-database")
with engine.connect() as conn:
    print("✅ Connexion OK :", conn.execute("SELECT 1").scalar())