from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Connect to database
SQLALCHEMY_DATABASE_URL = "sqlite:///./mzeechakula.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_users():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT id, email, is_active FROM users"))
        users = result.fetchall()
        print(f"Found {len(users)} users:")
        for user in users:
            print(f"ID: {user.id}, Email: {user.email}, Active: {user.is_active}")
    except Exception as e:
        print(f"Error querying database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_users()
