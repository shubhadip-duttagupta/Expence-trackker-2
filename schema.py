from __future__ import annotations
from pydantic import BaseModel
from datetime import date as dt_date

class ExpenseCreate(BaseModel):
	title: str
	amount: float
	category: str
	date: dt_date | None = None
class Expense(BaseModel):
	id: int
	title: str
	amount: float
	category: str
	date: dt_date

	class Config:
		orm_mode = True

class UserCreate(BaseModel):
	username: str
	password: str

class User(BaseModel):
	id: int
	username: str

	class Config:
		orm_mode = True