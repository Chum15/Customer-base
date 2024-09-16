import psycopg2



def create_table(conn):
    with conn.cursor() as cur:

        cur.execute("""
                    DROP TABLE phone;
                    DROP TABLE customer;""")

        cur.execute("""
                    CREATE TABLE customer(id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    surname TEXT NOT NULL,
                    email VARCHAR(100) NOT NULL
                    );""")
        
        cur.execute("""
                    CREATE TABLE phone(phone_id SERIAL PRIMARY KEY,
                    customer_id INTEGER NOT NULL REFERENCES customer(id) ON DELETE CASCADE,
                    phone VARCHAR(20));""")
        
        conn.commit()
      

def add_customer(conn, customer_data):
    with conn.cursor() as cur:
        cur.executemany("""INSERT INTO customer(name, surname, email)
                    VALUES (%s, %s, %s);""", customer_data)

        cur.execute("""SELECT * FROM customer;""")
        print(cur.fetchall())          


def add_phone(conn, phone_customer):
    with conn.cursor() as cur:
        cur.executemany("""INSERT INTO phone(customer_id, phone)
                        VALUES(%s, %s);""",(phone_customer))
            
        cur.execute("""SELECT * FROM phone;""")
        print(cur.fetchall())
        

def update(conn, id, name=None, surname=None, email=None):   
     with conn.cursor() as cur:
        arg_list = {'name': name, "surname": surname, 'email': email}
        for key, arg in arg_list.items():
            if arg:
                cur.execute("UPDATE customer SET {}=%s WHERE id=%s;".format(key), (arg, id))
        
        cur.execute(""" SELECT * FROM customer;""")
        print(cur.fetchall())


def delete_phone(conn, customer_id, phone):
     with conn.cursor() as cur:
        cur.execute("""
                    DELETE FROM phone WHERE customer_id = %s AND phone = %s;""",(customer_id, phone))
        
        cur.execute("""SELECT * FROM phone;""")
        print(cur.fetchall())


def delete_customer(conn, id):
     with conn.cursor() as cur:
        cur.execute("""
                   DELETE FROM customer WHERE id = %s;""",(id,))
        
        cur.execute(""" SELECT * FROM customer;""")
        print(cur.fetchall())


def select_customer(conn, name=None, surname=None, email=None, phone=None):
     with conn.cursor() as cur:
        cur.execute("""
                    SELECT name, surname, email, phone FROM customer
                    LEFT JOIN phone on phone.customer_id = customer.id
                    WHERE name = %s OR surname = %s OR email =%s OR phone =%s;""",(name, surname, email, phone))
        print(cur.fetchall()) 

       
      
customer_data =[('Иван', 'Иванов', 'ivanivanov@mail.ru'),('Петр','Петров', 'petrpetrov@mail.ru'),('Василий', 'Васильев', 'vasiliyvasilev@mail.ru')]
phone_customer = [(1, '89998887766'),(1, '89887776655'),(2, '89876665544')] 
with psycopg2.connect(database = "postgres", user = "postgres", password = "postgres") as conn:

    create_table(conn)
    add_customer(conn, customer_data)
    add_phone(conn, phone_customer)
    update(conn, name="Jon", id=2)
    delete_phone(conn, 1, '89998887766')
    delete_customer(conn, 2)
    select_customer(conn, surname='Васильев')


conn.close()    