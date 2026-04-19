from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal_expenses, engine_expenses, engine_users
import models
from userdetails import router as user_router

app = FastAPI()

# CORS Configuration

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],  # allow all (for development)
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

models.Base_expenses.metadata.create_all(bind=engine_expenses)
models.Base_users.metadata.create_all(bind=engine_users)

def get_db_expenses():
	db = SessionLocal_expenses()
	try:
		yield db
	finally:
		db.close()

@app.get("/")
def home():
	return {"message": "Expense Tracker API running"}


app.include_router(user_router)

@app.post("/expenses")
def add_expense(title: str, amount: float, category: str, db: Session = Depends(get_db_expenses)):
	new_expense = models.Expense(
		title=title,
		amount=amount,
		category=category
	)
	db.add(new_expense)
	db.commit()
	db.refresh(new_expense)
	return {"message": "Expense added successfully"}

@app.get("/expenses")
def get_expenses(db: Session = Depends(get_db_expenses)):
	expenses = db.query(models.Expense).all()
	return expenses

@app.get("/expenses/total")
def get_total_expenses(db: Session = Depends(get_db_expenses)):
	expenses = db.query(models.Expense).all()
	total = sum(e.amount for e in expenses)
	return {"total_expense": total}

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, title: str = None, db: Session = Depends(get_db_expenses)):
	expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
	if not expense:
		return {"error": "Expense not found"}
	
	# Optional: Verify title matches if provided
	if title and expense.title != title:
		return {"error": "Expense title doesn't match"}
	
	db.delete(expense)
	db.commit()
	return {"message": "Expense deleted successfully"}