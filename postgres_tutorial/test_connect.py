import psycopg2

# conn = psycopg2.connect("dbname=suppliers user=postgres_tutorial password=149367139Diez")

conn = psycopg2.connect(host="localhost", database="suppliers",
                        user="postgres_tutorial", password="149367139Diez")

print(conn)