from dataclasses import field
from enum import unique
from itertools import product
from multiprocessing import Condition
from secrets import choice
from tkinter import CASCADE
from xml.etree.ElementTree import tostring
from django.db import models
from django.contrib.auth.models import User
from django.forms import fields_for_model
# Create your models here.
class Author(models.Model):
    authorName=models.CharField(max_length=100, verbose_name='author name', unique=True)

    def __str__(self):
        return self.authorName

    class Meta:
        order_with_respect_to = 'authorName'

class Hostel(models.Model):
    hostelID=models.CharField(max_length=2, unique=True)
    hostelName=models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.hostelName

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumber= models.BigIntegerField()
    bitsID= models.CharField(max_length=13, primary_key=True)
    hostelName=models.ForeignKey(Hostel, on_delete=models.CASCADE)
    roomNumber=models.IntegerField()
    wallet=models.IntegerField(default=1000)

    def __str__(self):
        return self.bitsID

class Branch(models.Model):
    branchName=models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.branchName
    class Meta:
        order_with_respect_to = 'branchName'

class Course(models.Model):
    courseID=models.CharField(unique=True, max_length=10)
    courseName=models.CharField(max_length=100)
    branch=models.ForeignKey(Branch, on_delete=models.CASCADE)
    def __str__(self):
        return self.courseName
    class Meta:
        order_with_respect_to = 'branch'

class Book(models.Model):
    bookID=models.BigAutoField(primary_key=True)
    bookName=models.CharField(max_length=100)
    edition=models.IntegerField()
    writtenby=models.ManyToManyField(Author)
    belongstocourse=models.ManyToManyField(Course)

    def course_names(self):
        return ', '.join([(a.courseID+": "+a.courseName) for a in self.belongstocourse.all()])
    course_names.short_description = "Course Names"

    def author_names(self):
        return ', '.join([a.authorName for a in self.writtenby.all()])
    author_names.short_description = "Author Names"

    
    def __str__(self):
        return self.bookName+str(self.edition)


class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = 'user'
        

class Product(models.Model):
    class Cond(models.IntegerChoices):
        BAD = 1
        OK = 2
        GOOD = 3
        NEW = 4

    conditionofbook=models.IntegerField(default=Cond.BAD, choices=Cond.choices)
    price=models.IntegerField()
    sold=models.BooleanField(default=False)
    bookID=models.ForeignKey(Book, on_delete=models.CASCADE)
    sellerID=models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    def product_photos(self):
        return [a.photo for a in ProductPhotos.objects.filter(productID=self)]
    product_photosshort_description = "product photos"
    
    def getcond(self):
        cond=[" ", "BAD","OK", "GOOD", "NEW"]
        return cond[self.conditionofbook]
    
    def __str__(self):
        return str(self.sellerID.bitsID) + self.bookID.bookName

class ProductPhotos(models.Model):
    productID=models.ForeignKey(Product, on_delete=models.CASCADE)
    photo=models.ImageField(unique=True, upload_to='productpics/')
  

    class Meta:
        unique_together = (('productID', 'photo'),)

class Transaction(models.Model):
    productID=models.ForeignKey(Product, on_delete=models.CASCADE)
    buyerID=models.ForeignKey(Profile, on_delete=models.CASCADE)
    time=models.DateTimeField(auto_now_add=True, blank=True)