from django.contrib import admin

from .models import User, GroceryItem,ListDatabase,Category,Groceries,GroceryList
# Register your models here.
# Register your models here.
admin.site.register(GroceryItem)
admin.site.register(User)
admin.site.register(ListDatabase)
admin.site.register(Category)
admin.site.register(Groceries)
admin.site.register(GroceryList)
