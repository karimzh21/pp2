from datetime import datetime

date1 = datetime(2024, 10, 10, 0, 0, 0)
date2 = datetime(2024, 10, 11, 0, 0, 0)

difference = date2 - date1
seconds = difference.total_seconds()

print("Разница между двумя датами в секундах:", seconds)
