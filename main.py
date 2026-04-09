from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

app = FastAPI()

# CORS Configuration

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],  # allow all (for development)
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

@app.get("/")
def home():
	return {"message": "Expense Tracker API running"}

@app.post("/expenses")
def add_expense(title: str, amount: float, category: str, db: Session = Depends(get_db)):
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
def get_expenses(db: Session = Depends(get_db)):
	expenses = db.query(models.Expense).all()
	return expenses

@app.get("/expenses/total")
def get_total_expenses(db: Session = Depends(get_db)):
	expenses = db.query(models.Expense).all()
	total = sum(e.amount for e in expenses)
	return {"total_expense": total}

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, title: str = None, db: Session = Depends(get_db)):
	expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
	if not expense:
		return {"error": "Expense not found"}
	
	# Optional: Verify title matches if provided
	if title and expense.title != title:
		return {"error": "Expense title doesn't match"}
	
	db.delete(expense)
	db.commit()
	return {"message": "Expense deleted successfully"}