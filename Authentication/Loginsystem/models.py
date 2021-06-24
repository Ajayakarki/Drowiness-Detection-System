from django.db import models

# Create your models here.

class Users(models.Model):
	id = models.AutoField(primary_key=True)
	firstname = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	email = models.CharField(max_length=50, default='Default Value')
	password = models.CharField(max_length=30)
	repassword = models.CharField(max_length=30)

	def __str__(self):
		return self.firstname + " " + self.lastname

	class Meta:
		db_table = "Clients"



