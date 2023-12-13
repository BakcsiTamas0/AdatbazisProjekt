import mysql.connector

def establish_database_connection(host, user, password, database):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    connection.close()
    return connection