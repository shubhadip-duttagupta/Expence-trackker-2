from sqlalchemy import Column, Integer, String, Float, Date
from database import Base_expenses, Base_users
import datetime
import hashlib
import hmac
import os

class Expense(Base_expenses):
	__tablename__ = "expenses"
	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, nullable=False)
	amount = Column(Float, nullable=False)
	category = Column(String, nullable=False)
	date = Column(Date, default=datetime.date.today)

class User(Base_users):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, unique=True, nullable=False)
	password_hash = Column(String, nullable=False)

	def set_password(self, password: str):
		# Store as "salt_hex$derived_key_hex" using PBKDF2-HMAC-SHA256.
		salt = os.urandom(16)
		derived_key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120000)
		self.password_hash = f"{salt.hex()}${derived_key.hex()}"

	def check_password(self, password: str) -> bool:
		try:
			salt_hex, stored_key_hex = self.password_hash.split("$", 1)
			salt = bytes.fromhex(salt_hex)
			derived_key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120000)
			return hmac.compare_digest(derived_key.hex(), stored_key_hex)
		except (ValueError, TypeError):
			return False