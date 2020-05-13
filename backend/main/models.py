import os

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from PIL import Image

import uuid

HOSTEL_CHOICES = (
    ("SR", "SR Bhavan"),
    ("RP", "Rana Pratap Bhavan"),
    ("GN", "Gandhi Bhavan"),
    ("KR", "Krishna Bhavan"),
    ("MR", "Meera Bhavan"),
)

CATEGORY_CHOICES = (
    "Stationary",
    "Movie Ticket",
    "Grub Ticket",
    "Electronics",
    "Clothing",
    "Other Utility",
)


# Create your models here.
class Profile(models.Model):
    # --- Permission levels ---
    BANNED = 0
    BUYER = 1
    SELLER = 2
    ADMIN = 3
    LEVELS = (
        (BANNED, "Banned"), # Banned users cannot perform any action other than browsing products. 
        (BUYER, "Buyer"),
        (SELLER, "Seller"),
        (ADMIN, "Admin"),
    )
    # --- xxx ---

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=100)
    avatar = models.ManyToManyField('Avatar', symmetrical=False, blank=True)
    hostel = models.CharField(choices=HOSTEL_CHOICES, max_length=2)
    room_no = models.PositiveIntegerField(blank=True, null=True)
    contact_no = models.PositiveIntegerField(blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    num_ratings = models.IntegerField(default=0)
    email = models.EmailField()

    permission_level = models.SmallIntegerField(choices=LEVELS, default=2)

    @property
    def hostel_name(self):
        return getattr(dict(HOSTEL_CHOICES), self.hostel, "")

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "name": self.name,
            "hostel": self.hostel,
            "room_no": self.room_no,
            "contact_no": self.contact_no,
            "rating": self.rating,
            "num_rating": self.num_ratings,
            "email": self.email,
        }

    def to_compact_dict(self):
        return {
            "pk": self.pk,
            "user": self.user.pk,
            "name": self.name,
        }

    def __str__(self):
        return f"Profile({self.user.username})"


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """
    When a new user is created, create a profile for it. 
    When the user is updated, update its profile.
    """
    if created:
        Profile.objects.create(user=instance)
        Wishlist.objects.create(profile=instance.profile)
    instance.profile.save()
    

class Avatar(models.Model):
    """
    Model to save avatars of user profiles.
    """
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='avatars')
    url = models.CharField(max_length=40, null=True)
    
    def save(self, *args, **kwargs):
        self.url = self.image.url
        super().save(*args, **kwargs)


class ProfileRating(models.Model):
    rating_for = models.ForeignKey(
        Profile, related_name="ratings_recieved", on_delete=models.CASCADE
    )
    rated_by = models.ForeignKey(
        Profile, related_name="rating_given", on_delete=models.CASCADE
    )
    rating = models.IntegerField()

    def to_dict(self):
        return {
            "pk": self.pk,
            "rated_by": self.rated_by.name,
            "rating_for": self.rating_for.name,
            "rating": self.rating,
        }


@receiver(post_save, sender=ProfileRating)
def update_profile_rating(sender, instance, created, **kwargs):
    """
    Update the average rating of a profile when a new rating is given to the profile.
    """
    if created:
        profile = instance.rating_for
        num_ratings = profile.num_ratings
        profile.rating = (profile.rating * num_ratings + instance.rating) / (num_ratings + 1)
        profile.num_ratings += 1
        profile.save()

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    """
    All the instances of CATEGORY_CHOICES gets automatically created by migrations file 0014_auto_20200427_1006.py .
    """
    
    def __str__(self):
        return f"Category({self.name})"


class ProductManager(models.Manager):
    def tickets(self):
        return self.filter(is_ticket=True)


class Product(models.Model):
    name = models.CharField(max_length=60)
    images = models.ManyToManyField('ImageModel', symmetrical=False, blank=True)
    seller = models.ForeignKey(
        Profile,
        related_name="products",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    base_price = models.IntegerField(blank=False, null=False)
    description = models.CharField(max_length=300)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    sold = models.BooleanField(default=False)
    is_ticket = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)

    objects = ProductManager()

    def to_dict(self):
        return {
            "pk": self.pk,
            "name": self.name,
            # "images": [im.url for im in self.images]
            "seller": self.seller.pk,
            "base_price": self.base_price,
            "description": self.description,
            "sold": self.sold,
            "is_ticket": self.is_ticket,
            "created": self.created,
        }

    def __str__(self):
        return self.name

class Wishlist(models.Model):
    profile = models.OneToOneField(Profile, related_name="wishlist", on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, symmetrical=False, blank=True)

class ImageModel(models.Model):
    """
        Utility model for product images and profile photos.
    """
    image = models.ImageField(upload_to="images/")
    thumbnail = models.ImageField(upload_to="thumbs/")

    # @receiver(pre_save)
    # def resize_image(self,instance,**kwargs):
    #     pass


class ProductBid(models.Model):
    bidder = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="bids")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="bids")
    amount = models.IntegerField()
    message = models.CharField(max_length=400)

    def validate_bid_amount(self):
        """
        Check if bid amount is greater than product's base price
        """
        assert self.amount > product.base_price

    def __str__(self):
        return f"ProductBid({self.product.name}, {self.bidder.name}, {self.amount})"

    def to_dict(self):
        return {
            "bidder": self.bidder.name,
            "product": self.product.name,
            "amount": self.amount,
        }


class ProductQnA(models.Model):
    """
    Potential buyers can ask questions and the seller can answer.
    """
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="questions"
    )
    question = models.CharField(max_length=600)
    answer = models.CharField(max_length=600, blank=True)
    asked_by = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="questions"
    )
    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return f"Question({self.question}), Product({self.product.name}), Asked by({self.asked_by.name})"


class ProductReport(models.Model):
    product = models.ForeignKey('Product', related_name='reports', on_delete=models.CASCADE)
    message = models.CharField(max_length=400)
    reported_by = models.ForeignKey('Profile', on_delete=models.CASCADE)


@receiver(post_save, sender=ProductReport)
def moderate_product(sender, instance, **kwargs):
    """
        Make a product not visible if it has been reported more than 5 times.
    """
    # TODO: Implement mechanism to notify moderators.
    MAX_ALLOWED_REPORTS = 5
    product = instance.product
    if product.reports.count() > MAX_ALLOWED_REPORTS:
        product.visible = False
        product.save()
