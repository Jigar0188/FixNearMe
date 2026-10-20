
from database import test_connection

try:
    database_name, tables = test_connection()

    print("Database connection successful!")
    print(f"Connected database: {database_name}")
    print("\nExisting tables:")

    for table in tables:
        print(f"- {table}")

except Exception as error:
    print("Database connection failed.")
    print(f"Error: {type(error).__name__}: {error}")
