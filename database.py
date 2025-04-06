import pyodbc

def get_connection():
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=D:/laravel/Projects/Tamam/pythonProject/База_данных.accdb;'
    )
    return pyodbc.connect(conn_str)


conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\laravel\Projects\Tamam\pythonProject\База_данных.accdb;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()


def fetch_data(table_name):
    cursor.execute(f'SELECT * FROM {table_name}')
    return cursor.fetchall(), [desc[0] for desc in cursor.description]


def insert_data(table_name, columns, values):
    placeholders = ', '.join(['?' for _ in values])
    cursor.execute(f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({placeholders})', values)
    conn.commit()


def update_data(table_name, columns, values, key_column, key_value):
    set_clause = ', '.join([f'{col}=?' for col in columns if col != key_column])  # Exclude primary key column from SET clause
    update_query = f'UPDATE {table_name} SET {set_clause} WHERE {key_column}=?'

    values_to_update = [value for col, value in zip(columns, values) if col != key_column]

    try:
        cursor.execute(update_query, values_to_update + [key_value])
        conn.commit()
        print("Данные успешно обновлены")
    except Exception as e:
        print(f"Exception in update_data: {e}")
        raise


def delete_data(table_name, key_column, key_value):
    cursor.execute(f'DELETE FROM {table_name} WHERE {key_column}=?', (key_value,))
    conn.commit()