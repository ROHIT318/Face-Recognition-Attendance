from django.db import models

# Create your models here.
class registration_form(models.Model):
	unique_id = models.CharField(max_length=10, primary_key=True)
	name = models.CharField(max_length=60)
	img_1 = models.ImageField(upload_to='pics')
	img_2 = models.ImageField(upload_to='pics')
	img_3 = models.ImageField(upload_to='pics')
	img_4 = models.ImageField(upload_to='pics')
	img_5 = models.ImageField(upload_to='pics')
	img_6 = models.ImageField(upload_to='pics')
	img_7 = models.ImageField(upload_to='pics')