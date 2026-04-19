from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Expenses database
DATABASE_URL_EXPENSES = "sqlite:///./expenses.db"
engine_expenses = create_engine(
    DATABASE_URL_EXPENSES, connect_args={"check_same_thread": False}
)
SessionLocal_expenses = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_expenses
)
Base_expenses = declarative_base()

# Users database
DATABASE_URL_USERS = "sqlite:///./users.db"
engine_users = create_engine(
    DATABASE_URL_USERS, connect_args={"check_same_thread": False}
)
SessionLocal_users = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_users
)
Base_users = declarative_base()

# For backward compatibility, keep Base as expenses
Base = Base_expenses

if __name__ == "__main__":
    from models import Base_expenses, Base_users
    Base_expenses.metadata.create_all(bind=engine_expenses)
    Base_users.metadata.create_all(bind=engine_users)
    print("Databases and tables created successfully!")