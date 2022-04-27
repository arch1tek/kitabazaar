from asyncio import tasks
from django.contrib import admin
from .models import Task, Course, Author,  Book,  Branch, Profile, Transaction, Product, ProductPhotos, Hostel
# Register your models here.
admin.site.register(Task)
admin.site.register(Course)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Branch)
admin.site.register(Profile)
admin.site.register(Transaction)
admin.site.register(Product)
admin.site.register(ProductPhotos)
admin.site.register(Hostel)


