from datetime import datetime

current_date = datetime.now()
no_microsecond = current_date.replace(microsecond=0)

print("Дата с микросекундами:", current_date)
print("Дата без микросекунд:", no_microsecond)
