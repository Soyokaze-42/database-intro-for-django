from django.core.management.base import BaseCommand, CommandError
from registration.models import Owner, Pet, PetWeight

import random
import names
import random_address
import phone_gen
import petname
import datetime
import sqlite3


class Command(BaseCommand):
    help = "Creates dummy data as an example"

    def handle(self, *args, **options):
        phone_numbers = phone_gen.PhoneNumber("US")
        owners = []
        pets = []
        pet_weights = []

        # Setup the database
        db_connection = sqlite3.connect("pets.db")
        db_connection.execute("DROP TABLE IF EXISTS owner")
        db_connection.execute("DROP TABLE IF EXISTS pet")
        db_connection.execute("DROP TABLE IF EXISTS pet_weight")
        db_connection.execute(
            "CREATE TABLE owner(id INT, first_name TEXT, last_name TEXT, address1 TEXT, address2 TEXT, city TEXT, state TEXT, postal_code INT, phone INT)"
        )
        db_connection.execute(
            "CREATE TABLE pet(id INT, owner_id INT, name TEXT, type TEXT, birthday DATE, FOREIGN KEY(owner_id) REFERENCES owner(id))"
        )
        db_connection.execute(
            "CREATE TABLE pet_weight(pet_id INT, weight INT, weight_date DATE, FOREIGN KEY(pet_id) REFERENCES pet(id))"
        )

        with open("pets.csv", "w") as f:
            f.write(
                "owner_first_name,owner_last_name,owner_address1,owner_address2,owner_city,owner_state,owner_postal_code,owner_phone,owner_credit_card,pet_name,pet_type,pet_birthday,pet_weight1,pet_weight1_date,pet_weight2,pet_weight2_date\n"
            )
            for owner_num in range(10):
                owner_first_name = names.get_first_name()
                owner_last_name = names.get_last_name()
                address = random_address.real_random_address_by_state("CA")
                owner_address1 = address["address1"]
                owner_address2 = address["address2"]
                owner_city = address["city"]
                owner_state = address["state"]
                owner_postal_code = address["postalCode"]
                owner_phone = phone_numbers.get_number()
                owner_id = owner_num
                owners.append(
                    f"{owner_id},{owner_first_name},{owner_last_name},{owner_address1},{owner_address2},{owner_city},{owner_state},{owner_postal_code},{owner_phone}\n"
                )
                db_connection.execute(
                    "INSERT INTO owner VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        str(owner_id),
                        owner_first_name,
                        owner_last_name,
                        owner_address1,
                        owner_address2,
                        owner_city,
                        owner_state,
                        owner_postal_code,
                        owner_phone,
                    ),
                )
                owner = Owner.objects.create(
                    first_name=owner_first_name,
                    last_name=owner_last_name,
                    address1=owner_address1,
                    address2=owner_address2,
                    city=owner_city,
                    state=owner_state,
                    postal_code=owner_postal_code,
                    phone=owner_phone,
                )
                for pet_num in range(random.randint(1, 10)):
                    pet_name = petname.adverb().capitalize() + " " + petname.adjective().capitalize()
                    pet_type = petname.name()
                    pet_id = pet_num
                    pet_birthday = datetime.datetime.fromtimestamp(
                        random.randint(
                            int(datetime.datetime.now().timestamp() - 500000000),
                            int(datetime.datetime.now().timestamp() - 20000),
                        )
                    )
                    pets.append(
                        f"{pet_id},{owner_id},{pet_name},{pet_type},{pet_birthday.date()}\n"
                    )
                    pet = Pet.objects.create(
                        owner=owner, name=pet_name, type=pet_type, birthday=pet_birthday
                    )
                    db_connection.execute(
                        "INSERT INTO pet VALUES (?, ?, ?, ?, ?)",
                        (
                            str(pet_id),
                            str(owner_id),
                            pet_name,
                            pet_type,
                            pet_birthday.date(),
                        ),
                    )
                    pet_weight1 = random.randint(1, 100)
                    pet_weight1_date = datetime.datetime.fromtimestamp(
                        random.randint(
                            int(pet_birthday.timestamp()),
                            int(datetime.datetime.now().timestamp() - 10000),
                        )
                    )
                    pet_weights.append(
                        f"{pet_id},{pet_weight1},{pet_weight1_date.date()}\n"
                    )
                    PetWeight.objects.create(
                        pet=pet, weight=pet_weight1, weight_date=pet_weight1_date
                    )
                    db_connection.execute(
                        "INSERT INTO pet_weight VALUES (?, ?, ?)",
                        (str(pet_id), pet_weight1, pet_weight1_date.date()),
                    )
                    if random.randint(0, 1):
                        pet_weight2 = random.randint(pet_weight1, 100)
                        pet_weight2_date = datetime.datetime.fromtimestamp(
                            random.randint(
                                int(pet_weight1_date.timestamp()),
                                int(datetime.datetime.now().timestamp()),
                            )
                        )
                        pet_weights.append(
                            f"{pet_id},{pet_weight2},{pet_weight2_date.date()}\n"
                        )
                        PetWeight.objects.create(
                            pet=pet, weight=pet_weight2, weight_date=pet_weight2_date
                        )
                        db_connection.execute(
                            "INSERT INTO pet_weight VALUES (?, ?, ?)",
                            (str(pet_id), pet_weight2, pet_weight2_date.date()),
                        )
                        f.write(
                            f"{owner_first_name},{owner_last_name},{owner_address1},{owner_address2},{owner_city},{owner_state},{owner_postal_code},{owner_phone},{pet_name},{pet_type},{pet_birthday.date()},{pet_weight1},{pet_weight1_date.date()},{pet_weight2},{pet_weight2_date.date()}\n"
                        )
                    else:
                        pet_weight2 = ""
                        pet_weight2_date = ""
                        f.write(
                            f"{owner_first_name},{owner_last_name},{owner_address1},{owner_address2},{owner_city},{owner_state},{owner_postal_code},{owner_phone},{pet_name},{pet_type},{pet_birthday.date()},{pet_weight1},{pet_weight1_date.date()}\n"
                        )

            f.write("\n\n\n")
            f.write(
                "id,owner_first_name,last_name,address1,address2,city,state,postal_code,phone\n"
            )
            for owner in owners:
                f.write(owner)

            f.write("\n\n\n")
            f.write("id,owner_id,name,type,birthday\n")
            for pet in pets:
                f.write(pet)

            f.write("\n\n\n")
            f.write("pet_id,weight,weight_date\n")
            for pet_weight in pet_weights:
                f.write(pet_weight)

        db_connection.commit()
