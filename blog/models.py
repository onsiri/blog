from django.db import models
from django.http import request
from django.urls import reverse
from django.shortcuts import render

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
    )
    body = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

class Product(models.Model):
    product_description = models.CharField(max_length=2000)
    product_name = models.CharField(max_length=2000)

    def __str__(self):
        return self.product_name


class Transaction(models.Model):
    UserId = models.CharField(max_length=100)
    TransactionId = models.CharField(max_length=100)
    TransactionTime = models.CharField(max_length=500)
    ItemCode = models.CharField(max_length=100)
    ItemDescription = models.TextField()
    NumberOfItemsPurchased = models.IntegerField()
    CostPerItem = models.DecimalField(max_digits=10, decimal_places=2)
    Country = models.CharField(max_length=100)

    def __str__(self):
        return self.UserId