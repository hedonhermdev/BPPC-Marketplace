import os

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image

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
    # --- Hostel Choices ---
    HOSTEL_CHOICES = (
        ("SR", "SR Bhavan"),
        ("RP", "Rana Pratap Bhavan"),
        ("GN", "Gandhi Bhavan"),
        ("KR", "Krishna Bhavan"),
        ("MR", "Meera Bhavan"),
    )
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
    contact_no = PhoneNumberField(blank=True, null=True, unique=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    num_ratings = models.IntegerField(default=0)
    email = models.EmailField()
    is_complete = models.BooleanField(default=False) # Field to signify if user has filled all required details in profile.
    permission_level = models.SmallIntegerField(choices=LEVELS, default=2)

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


@receiver(post_save, sender=Profile)
def set_permission_level(sender, instance, created, **kwargs):
    """
    When a new user is created, set its permission_level according to its email.
    BITSIAN -> SELLER
    NON-BITSIAN -> BUYER
    """
    if instance.email != "" and instance.permission_level is not None:
        domain = instance.email.split('@')[1]

        # Bitsian or Non Bitsian
        if domain == "pilani.bits-pilani.ac.in":
            # Bitsians can be sellers
            permission_level = Profile.SELLER
        else:
            # Non-bitsians can be buyers only.
            permission_level = Profile.BUYER
            instance.permission_level = permission_level

@receiver(pre_save, sender=Profile)
def update_is_complete(sender, instance, **kwargs):
    if (instance.name!= "") and (instance.hostel != "") and (instance.contact_no != ""):
        instance.is_complete = True
    else:
        instance.is_complete = False

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
        Profile, related_name="ratings_received", on_delete=models.CASCADE
    )
    rated_by = models.ForeignKey(
        Profile, related_name="rating_given", on_delete=models.CASCADE
    )
    rating = models.IntegerField()


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

    class Meta:
        verbose_name_plural = "Categories"


class ProductManager(models.Manager):
    """
    Custom manager for products.
    objects.all() -> Only visible and non-expired products
    """
    def get_queryset(self):
        return super().get_queryset().filter(expired=False, visible=True)



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
    expected_price = models.PositiveIntegerField(blank=False, null=False)
    description = models.CharField(max_length=300)
    category = models.ForeignKey('Category', related_name="products", on_delete=models.SET_NULL, null=True)
    is_ticket = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    is_negotiable = models.BooleanField(default=False) # If product is non-negotiable, all offer prices must be equal to expected_price

    num_offers = models.IntegerField(default=0)

    visible = models.BooleanField(default=True) # For banning/unbanning products.
    expired = models.BooleanField(default=False) # For expiring products after given expiry period.
    sold = models.BooleanField(default=False) # For marking a product as sold after deal is complete.

    objects = ProductManager()

    def to_dict(self):
        return {
            "pk": self.pk,
            "name": self.name,
            # "images": [im.url for im in self.images]
            "seller": self.seller.pk,
            "expected_price": self.expected_price,
            "description": self.description,
            "sold": self.sold,
            "is_ticket": self.is_ticket,
            "created_at": self.created_at,
        }

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    """
    Model to save a user's wishlist. 
    Users can add/delete items from their wishlist.
    """
    profile = models.OneToOneField(Profile, related_name="wishlist", on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, symmetrical=False, limit_choices_to={'expired': False, 'visible': True, 'sold': False})


class ImageModel(models.Model):
    """
    Utility model for product images and profile photos.
    """
    image = models.ImageField(upload_to="images/")
    thumbnail = models.ImageField(upload_to="thumbs/")

    # @receiver(pre_save)
    # def resize_image(self,instance,**kwargs):
    #     pass


class ProductOffer(models.Model):
    offerer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="offers")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="offers")
    amount = models.IntegerField()
    message = models.CharField(max_length=400)

    def validate_offer_amount(self):
        """
        Check if offer amount is greater than product's base price
        """
        assert self.amount > product.expected_price

    def to_dict(self):
        return {
            "offerer": self.offerer.name,
            "product": self.product.name,
            "amount": self.amount,
        }

    def __str__(self):
        return f"ProductOffer({self.product.name}, {self.offerer.name}, {self.amount})"

@receiver(post_save, sender=ProductOffer)
def update_product_offers(sender, instance, created, **kwargs):
    """
    Update the number of offers of a product when a new offer is made.
    """
    if created:
        product = instance.product
        product.num_offers += 1
        product.save()


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

    class Meta:
        verbose_name = "Product QnA"
        verbose_name_plural = "Products QnA"


class UserReport(models.Model):
    """
    Model for handling reporting of users by other users.
    Reports can be categorized into three broad categories mentioned below.
    """
    CATEGORY_CHOICES = (
        (1, "Spam"),
        (2, "Profanity"),
        (3, "Refusal to Pay"),
    )
    reported_user = models.ForeignKey('Profile', related_name='reports', on_delete=models.CASCADE)
    reported_by = models.ForeignKey('Profile', on_delete=models.CASCADE)
    category = models.SmallIntegerField(choices=CATEGORY_CHOICES)


@receiver(post_save, sender=UserReport)
def moderate_profile(sender, instance, **kwargs):
    """
    Ban a user after 5 reports.
    """
    # TODO: Implement mechanism to notify moderators.
    MAX_ALLOWED_REPORTS = 5
    profile = instance.reported_user
    if profile.reports.count() > MAX_ALLOWED_REPORTS:
        profile.permission_level = Profile.BANNED
        profile.save()
