import sqlite3

db_connection = sqlite3.connect("pets.db")
db_cursor = db_connection.cursor()

queries = [
    "SELECT * FROM owner;",

    """
    SELECT owner.first_name, owner.last_name, pet.name, pet.birthday
    FROM owner
    JOIN pet ON owner.id = pet.owner_id;
    """,

    """
    SELECT DISTINCT pet.name
    FROM pet
    JOIN pet_weight ON pet.id = pet_weight.pet_id
    WHERE pet_weight.weight > 80;
    """,

    """
    SELECT owner.first_name, owner.last_name, owner.address1, owner.address2, owner.city, owner.state, owner.postal_code, owner.phone,
           pet.name, pet.type, pet.birthday,
           pet_weight.weight, pet_weight.weight_date
    FROM owner
    JOIN pet ON owner.id = pet.owner_id
    JOIN pet_weight ON pet.id = pet_weight.pet_id;
    """
]

for query in queries:
    print("We are about to run the following query:")
    print(query)
    input("Press any key to continue...")
    print()
    db_cursor.execute(query)
    for row in db_cursor.fetchall():
        print(row)
    print()