import os
import psycopg2
import csv

CREATE_STATEMENTS = {
    'file1': '''
    CREATE TABLE IF NOT EXISTS accounts (
        customer_id INT PRIMARY KEY,
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        address_1 VARCHAR(255),
        address_2 VARCHAR(255),
        city VARCHAR(255),
        state VARCHAR(255),
        zip_code VARCHAR(10),
        join_date DATE
    );
    ''',
    'file2': '''
    CREATE TABLE IF NOT EXISTS products (
        product_id INT PRIMARY KEY,
        product_code VARCHAR(50),
        product_description TEXT
    );
    ''',
    'file3': '''
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id VARCHAR(255) PRIMARY KEY,
        transaction_date DATE,
        product_id INT REFERENCES products(product_id),  -- Updated
        product_code VARCHAR(50),
        product_description TEXT,
        quantity INT,
        account_id INT REFERENCES accounts(customer_id)  -- Updated
    );
    '''
}

def create_tables(conn, cur):
    for table, create_statement in CREATE_STATEMENTS.items():
        print(f"Creating table: {table}")
        cur.execute(create_statement)
    conn.commit()

def insert_data_from_csv(conn, cur, csv_file, table_name, columns):
    try:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row

            placeholders = ', '.join(['%s'] * len(columns))
            if table_name == 'accounts':
                conflict_column = 'customer_id'
            elif table_name == 'products':
                conflict_column = 'product_id'
            elif table_name == 'transactions':
                conflict_column = 'transaction_id'
            else:
                conflict_column = None  # Default to None, should not happen

            for row in reader:
                if conflict_column:
                    cur.execute(f"""
                        INSERT INTO {table_name} ({', '.join(columns)})
                        VALUES ({placeholders})
                        ON CONFLICT ({conflict_column}) DO NOTHING;
                    """, row)
                else:
                    cur.execute(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders});", row)

        conn.commit()
    except Exception as e:
        print(f"Error inserting data from {csv_file} into {table_name}: {e}")
        conn.rollback()

def main():
    host = "postgres"  
    database = "postgres"
    user = "postgres"
    pas = "postgres"
    
    conn = psycopg2.connect(host=host, database=database, user=user, password=pas)
    cur = conn.cursor()

    create_tables(conn, cur)

    data_folder = "data"
    csv_files = {
        'accounts.csv': ('accounts', ['customer_id', 'first_name', 'last_name', 'address_1', 'address_2', 'city', 'state', 'zip_code', 'join_date']),
        'products.csv': ('products', ['product_id', 'product_code', 'product_description']),
        'transactions.csv': ('transactions', ['transaction_id', 'transaction_date', 'product_id', 'product_code', 'product_description', 'quantity', 'account_id'])
    }

    for csv_file, (table_name, columns) in csv_files.items():
        csv_file_path = os.path.join(data_folder, csv_file)
        insert_data_from_csv(conn, cur, csv_file_path, table_name, columns)

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()