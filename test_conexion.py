import json
import pyodbc

try:
    with open('config.json') as config_file:
        config = json.load(config_file)

    driver = config["driver"]
    server = config["server"]
    database = config["database"]
    user = config["user"]
    password = config["password"]

    connection_string = (
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
        f"TrustServerCertificate=yes"
    )

    conexion = pyodbc.connect(connection_string)
    print("Conexión exitosa a SQL Server")
    conexion.close()

except Exception as e:
    print("Error al conectar a SQL Server:")
    print(e)
