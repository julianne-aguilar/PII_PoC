import sqlite3
from transformers import pseudonymize_client_id, sanitize_name, sanitize_email, sanitize_ssn, mask_phone_number, dob_to_age_range, generalize_zip_code

def sanitize_database(source_db, output_db):
    #connect to source database
    source_conn = sqlite3.connect(source_db)
    source_cursor = source_conn.cursor()

    #create sanitized database
    sanitized_conn = sqlite3.connect(output_db)
    sanitized_cursor = sanitized_conn.cursor()

    #reset output tables
    sanitized_cursor.execute("DROP TABLE IF EXISTS policies")
    sanitized_cursor.execute("DROP TABLE IF EXISTS clients")

    #create sanitized clients table
    sanitized_cursor.execute("""
    CREATE TABLE clients (
        client_id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        phone TEXT,
        ssn TEXT,
        age_range TEXT,
        zip_code TEXT,
        occupation TEXT
    )
    """)

    #create sanitized policies table
    sanitized_cursor.execute("""
    CREATE TABLE policies (
        policy_number TEXT PRIMARY KEY,
        client_id TEXT NOT NULL,
        policy_type TEXT,
        premium REAL,
        coverage_amount REAL,
        status TEXT,
        FOREIGN KEY (client_id) REFERENCES clients(client_id)
    )
    """)

    #read clients
    source_cursor.execute("SELECT * FROM clients")
    clients = source_cursor.fetchall()

    #sanitize clients
    for client in clients:
        sanitized_client = (
            pseudonymize_client_id(client[0]),
            sanitize_name(client[1]),
            sanitize_email(client[2], client[0]),
            mask_phone_number(client[3]),
            sanitize_ssn(client[4]),
            dob_to_age_range(client[5]),
            generalize_zip_code(client[6]),
            client[7]
        )

        sanitized_cursor.execute("""
        INSERT INTO clients
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, sanitized_client)

    #read policies
    source_cursor.execute("SELECT * FROM policies")
    policies = source_cursor.fetchall()

    #sanitize policies
    for policy in policies:
        sanitized_policy = (
            policy[0],
            pseudonymize_client_id(policy[1]),
            policy[2],
            policy[3],
            policy[4],
            policy[5]
        )

        sanitized_cursor.execute("""
        INSERT INTO policies
        VALUES (?, ?, ?, ?, ?, ?)
        """, sanitized_policy)

    sanitized_conn.commit()

    source_conn.close()
    sanitized_conn.close()

    return output_db

