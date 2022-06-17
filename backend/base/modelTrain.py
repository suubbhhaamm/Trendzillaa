import pandas as pandas
import psycopg2

print('hi')

connection = psycopg2.connect(user="postgres",
                                      password="student@postgres123",
                                      host="localhost",
                                      port="5432",
                                      database="proshop")
dataFrame = pd.read_sql("select * from select * from auth_user", connection)
print('hi')
print(dataFrame.head(5))