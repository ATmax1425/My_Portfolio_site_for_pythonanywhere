from django.db import models


# Create your models here.
class Message(models.Model):
    name = models.CharField(max_length=50)
    email_id = models.EmailField(max_length=50)
    organization_name = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return f"{str(self.name)} || {str(self.email_id)} || {str(self.organization_name)} \n{str(self.message)}"
