import pymysql 

conn = pymysql.connect(host='localhost', user='root', password='0000', charset='utf8') 
cursor = conn.cursor() 

sql = "CREATE DATABASE IF NOT EXISTS library_management" 

cursor.execute(sql) 

conn.commit() 
conn.close() 