import sqlite3
import random
from faker import Faker

fake = Faker()

DB_NAME = "insurance.db"

# -----------------------------
# Connect to SQLite
# -----------------------------

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Enable foreign key checking
cursor.execute("PRAGMA foreign_keys = ON")


# -----------------------------
# Create tables
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS clients (
    client_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone TEXT,
    ssn TEXT,
    dob TEXT,
    zip_code TEXT,
    occupation TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS policies (
    policy_number TEXT PRIMARY KEY,
    client_id INTEGER NOT NULL,
    policy_type TEXT,
    premium REAL,
    coverage_amount REAL,
    status TEXT,
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
)
""")


# -----------------------------
# Generate clients
# -----------------------------

NUM_CLIENTS = 20

for client_id in range(1001, 1001 + NUM_CLIENTS):

    cursor.execute("""
    INSERT INTO clients (
        client_id,
        name,
        email,
        phone,
        ssn,
        dob,
        zip_code,
        occupation
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        client_id,
        fake.name(),
        fake.email(),
        fake.phone_number(),
        fake.ssn(),
        fake.date_of_birth(
            minimum_age=18,
            maximum_age=80
        ).isoformat(),
        fake.zipcode(),
        fake.job()
    ))


# -----------------------------
# Generate policies
# -----------------------------

policy_types = [
    "Auto",
    "Home",
    "Life",
    "Health"
]

statuses = [
    "Active",
    "Inactive"
]

policy_counter = 1

for client_id in range(1001, 1001 + NUM_CLIENTS):

    # Give each client 1-3 policies
    number_of_policies = random.randint(1, 3)

    for _ in range(number_of_policies):

        policy_number = f"POL{policy_counter:05d}"

        cursor.execute("""
        INSERT INTO policies (
            policy_number,
            client_id,
            policy_type,
            premium,
            coverage_amount,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            policy_number,
            client_id,
            random.choice(policy_types),
            round(random.uniform(500, 5000), 2),
            random.choice([
                50000,
                100000,
                250000,
                500000,
                1000000
            ]),
            random.choice(statuses)
        ))

        policy_counter += 1


# -----------------------------
# Save database
# -----------------------------

conn.commit()
conn.close()

print(f"Fake database created: {DB_NAME}")