from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass
class Meta:
    model = User
    fields = ("username",)


class GroceryList(models.Model):
    name = models.CharField(max_length=100)
    finished = models.BooleanField(default=False)
    saved_list = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)  # User who created the list
    shared_with = models.ManyToManyField(User, related_name='shared_lists', blank=True)  
    def serialize(self):
        return {
            "list_id": self.id,
            "name": self.name,
            "finished": self.finished,
            "saved_list": self.saved_list,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }

class GroceryItem(models.Model):
    list = models.ForeignKey(GroceryList, on_delete=models.CASCADE)  # Add this line
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)
    instruction = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userName")
    added=models.BooleanField(default=False)
  

    def serialize(self):
        return {
            "list_id": self.list.id,  # Changed to refer to the list's id
            "list": self.list.name,   # Changed to refer to the list's name
            "name": self.name,
            "quantity": self.quantity,
            "instruction": self.instruction,
            "added":self.added,
           
          
        }



class Groceries(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    def __str__(self):
      
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=128)
    category_items = models.ManyToManyField(Groceries, through="ListDatabase")

    def __str__(self):
        return self.name


class ListDatabase(models.Model):
    groceries= models.ForeignKey(Groceries, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField(blank=True,default=0)
    quantity= models.TextField(blank=True,default=1)