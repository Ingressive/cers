from django.db import models

# Model to save reports made
class Report(models.Model):
    number = models.CharField(max_length=20)
    location = models.CharField(max_length=100) # Get location property value off unit
    message = models.CharField(max_length=100)

    def __str__(self):
        return "{} => {}".format(self.location, self.message)
