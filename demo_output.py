import sqlite3
from sanitize import sanitize_database

source_db = "insurance.db"
sanitized_db = "sanitized.db"

sanitize_database(source_db, sanitized_db)

source_conn = sqlite3.connect(source_db)
source_cursor = source_conn.cursor()

sanitized_conn = sqlite3.connect(sanitized_db)
sanitized_cursor = sanitized_conn.cursor()

print("\n----- Original Client Data -----")

source_cursor.execute("SELECT * FROM clients")
clients = source_cursor.fetchall()
print(clients[0])


print("\n----- Sanitized Client Data -----")

sanitized_cursor.execute("SELECT * FROM clients")
sanitized_clients = sanitized_cursor.fetchall()
print(sanitized_clients[0])

print("\n----- Original Policies Data -----")

source_cursor.execute("SELECT * FROM policies")
policies = source_cursor.fetchall()
print(policies[0])


print("\n----- Sanitized Policies Data -----")

sanitized_cursor.execute("SELECT * FROM policies")
sanitized_policies = sanitized_cursor.fetchall()
print(sanitized_policies[0])

print("\n-----Relationship Preservation Test-----")
"""
Show that after sanitization, the database can still connect each client to their policies 
"""
sanitized_cursor.execute("""
SELECT clients.client_id,
       policies.policy_number,
       policies.policy_type
FROM clients
JOIN policies
ON clients.client_id = policies.client_id
LIMIT 10
""")

for row in sanitized_cursor.fetchall():
    print(row)