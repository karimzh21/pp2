from datetime import datetime, timedelta

current_date = datetime.now()
new_date = current_date - timedelta(days=5)

print("Текущая дата:", current_date)
print("Дата после вычитания 5 дней:", new_date) 
