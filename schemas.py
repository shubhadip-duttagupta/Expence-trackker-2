from __future__ import annotations
from pydantic import BaseModel
from datetime import date

class ExpenseCreate(BaseModel):
	title: str
	amount: float
	category: str
	date: date | None = None
class Expense(BaseModel):
	id: int
	title: str
	amount: float
	category: str
	date: date

	class Config:
		orm_mode = True