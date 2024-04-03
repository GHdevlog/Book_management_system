import datetime 
from random import randrange, randint

start_date = datetime.datetime(2024, 1, 1)
end_date = datetime.datetime(2024, 12, 31)
# 랜덤한 날짜 생성
random_date = start_date + datetime.timedelta(days=randint(0, (end_date - start_date).days))

user_id = 10
book_id = 10
loan_date = random_date.strftime('%Y-%m-%d')
return_date = (random_date + datetime.timedelta(days=10))

# SQL 쿼리 실행하여 데이터 삽입
sql = "INSERT INTO loans (user_id, book_id , loan_date, return_date) VALUES (%s, %s, %s, %s)"
loan = [user_id, book_id, str(loan_date), str(return_date)]

print(loan)