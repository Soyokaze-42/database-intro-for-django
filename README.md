Database introduction for Django developers

This repo is for an activity to introduce databases to Django developers. To flow with Django, we need a data-centric view of our application. Django has a wonderful ORM that allows us to interact with our database in a Pythonic way. This is a great way to use a database in Django, but it is important to understand how the database works and how to interact with it directly.

To get started, make sure you have python 3 installed, clone this repo, cd into the clone, and run the following commands:
```
cd pet_registration
pip install -r requirements.txt
python manage.py migrate
python manage.py make_dummy_data
python manage.py makesuperuser
```

This will create a sqlite3 database with dummy data in it and a superuser for you to login to the admin site later. First, we are going to to look through the data in pets.csv and query a sample database.

Get familiar with the data in pets.csv. The first block of data is a list of pets that have been registered at a vet office. Notice the two situations that are not ideal:
1. There is overlap between pets that have the same owner.
2. There are multiple weights for some pets.

We can use a database to organize our data in a way that will make it faster to find information, more efficient to store, and most importantly, less susceptible to errors. The three other blocks of data in pets.csv are the same data, but organized in a way that will make it easier to work with in a database. Another way to put it is that the data is normalized.

We have loaded the data into a sqlite3 database called pets.db. To query the database, we are going to use SQL and the sqlite3 command line tool.

sqlite3 is a lightweight database that does not run as a service, but runs as part of the application. It is a great tool for learning about databases and for prototyping. It is often not a good tool for production applications.

SQL is the language that we use to interact with a database. We are just going to query the database to get information out in this activity. We will not be modifying the database. In our examples, the SQL comes after the name of the sqlite database file inside the quotation marks.

To query the database for the list of tables, run the following command:
```
sqlite3 pets.db ". tables"
```

To query the database for all the data about owners, run the following command. The output of this command should match the owner data in pets.csv.
```
sqlite3 pets.db "SELECT * FROM owner;"
```

Now try on your own to query the database for all the data about pets and their weights.

In the database, we have set up some relationships between the tables to keep the data consistent. In our examples, we use the id fields in the owner and pet tables to keep track of these relationships. In this next example, pet.owner_id must match owner.id.

If you want to get data from multiple tables, you can use a SQL JOIN. To query the database for some of the data about owners and their pets, run the following command.
```
sqlite3 pets.db "
SELECT owner.first_name, owner.last_name, pet.name, pet.birthday
FROM owner
JOIN pet ON owner.id = pet.owner_id;"
```

If you want to filter the data that you get back, you can use a WHERE clause. In this example, we are filtering the data to only get pets that have weights over 80 pounds. 
To query the database for useful information about pets and their weights, run the following command.
```
sqlite3 pets.db "
SELECT DISTINCT pets.name
FROM pet
JOIN pet_weights ON pet.id = pet_weight.pet_id
WHERE pet_weight.weight > 80;"
```

Finally, if you want to completly recreate the data in pets.csv, you can use two SQL JOINs on all the id fields. 
```
sqlite3 pets.db "
SELECT owner.first_name, owner.last_name, owner.address1, owner.address2, owner.city, owner.state, owner.postal_code, owner.phone,
       pet.name, pet.type, pet.birthday,
       pet_weight.weight, pet_weight.weight_date
FROM owner
JOIN pet ON owner.id = pet.owner_id
JOIN pet_weight ON pet.id = pet_weight.pet_id;"
```

You can login to the admin site at http://localhost:8000/admin. You can also run the server and go to http://localhost:8000 to see the app.