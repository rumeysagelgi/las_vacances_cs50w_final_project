from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.URLField()


class Suite(models.Model):
    title = models.CharField(max_length=255, blank=False)
    address = models.CharField(max_length=255, blank=False)
    details = models.TextField(blank=False)
    image = models.URLField(blank=False)
    price = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return f" ID: {self.id} | Title: {self.title} | Address: {self.address}"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "address": self.address,
            "details": self.details,
            "image": self.image,
            "price": self.price
        }


class List(models.Model):
    name = models.CharField(max_length=255, blank=False)
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="lists")

    def __str__(self):
        return f" ID: {self.id} | Author: {self.author} | Name: {self.name}"


class List_item(models.Model):
    list = models.ForeignKey("List", on_delete=models.CASCADE, related_name="list_items")
    suite = models.ForeignKey("Suite", on_delete=models.CASCADE, related_name="listed")

    def __str__(self):
        return f" ID: {self.id} | List: {self.list} | Suite: {self.suite}"


class Rating(models.Model):
    suite = models.ForeignKey("Suite", on_delete=models.CASCADE, related_name="ratings", unique=True)
    rating = models.DecimalField(max_digits=4, decimal_places=2, blank=False)

    def __str__(self):
        return f" ID: {self.id} | Suite: {self.suite} | Rating: {self.rating}"


class Review(models.Model):
    title = models.CharField(max_length=255, blank=False)
    suite = models.ForeignKey("Suite", on_delete=models.CASCADE, related_name="reviewed")
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="reviews")
    review = models.TextField(blank=False)
    rating = models.IntegerField(blank=False)

    def __str__(self):
        return f" ID: {self.id} | Author: {self.author} | Title: {self.title} | Suite: {self.suite.title} | Rating: {self.rating}"