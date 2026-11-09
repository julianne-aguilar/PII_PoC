import sqlite3

conn = sqlite3.connect("insurance.db")
cursor = conn.cursor()

print("\nCLIENTS:")
cursor.execute("SELECT * FROM clients LIMIT 10")

for row in cursor.fetchall():
    print(row)

print("\nPOLICIES:")
cursor.execute("SELECT * FROM policies LIMIT 10")

for row in cursor.fetchall():
    print(row)

print("\nJOIN TEST:")
cursor.execute("""
SELECT clients.client_id, clients.name,
       policies.policy_number, policies.policy_type
FROM clients
JOIN policies
ON clients.client_id = policies.client_id
LIMIT 10
""")

for row in cursor.fetchall():
    print(row)

conn.close()