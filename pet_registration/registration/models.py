from django.db import models


class Owner(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    postal_code = models.IntegerField()
    phone = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Pet(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    birthday = models.DateField()

    def __str__(self):
        return f"{self.name}"


class PetWeight(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    weight = models.IntegerField()
    weight_date = models.DateField()

    def __str__(self):
        return f"{self.pet.name}: {self.weight} on {self.weight_date}"
