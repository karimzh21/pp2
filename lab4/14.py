from datetime import datetime, timedelta

сегодня = datetime.now()
вчера = сегодня - timedelta(days=1)
завтра = сегодня + timedelta(days=1)

print("Вчерашний день:", вчера.strftime('%d.%m'))
print("Сегодняшний день:", сегодня.strftime('%d.%m'))
print("Завтрашний день:", завтра.strftime('%d.%m'))
