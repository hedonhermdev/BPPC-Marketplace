from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

HOSTEL_CHOICES = (
    ("SR", "SR Bhavan"),
    ("RP", "Rana Pratap Bhavan"),
    ("GN", "Gandhi Bhavan"),
    ("KR", "Krishna Bhavan"),
    ("MR", "Meera Bhavan"),
)

CATEGORY_CHOICES = (
    ("STAT", "Stationay"),
    ("MOVI", "Movie Ticket"),
    ("GRUB", "Grub Ticket"),
    ("ELEC", "Electronics"),
    ("CLOT", "Clothing"),
    ("OTHR", "Other Utility"),
)


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    hostel = models.CharField(choices=HOSTEL_CHOICES, max_length=2)
    room_no = models.PositiveIntegerField()
    contact_no = models.PositiveIntegerField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    no_of_ratings = models.PositiveIntegerField(default=0)
    email = models.EmailField()

    def save(self):
        """
        always update the rating of user
        """
        user = self.user
        raters = user.ratings_recieved.all()

        rate_points = 0
        no_of_ratings = 0
        rating = 0
        for r in raters:
            rate_points = r.rating + rate_points
            no_of_ratings = no_of_ratings + 1

        self.no_of_ratings = no_of_ratings
        if no_of_ratings != 0:
            rating = rate_points / no_of_ratings
        self.rating = round(rating, 1)

        super().save()

    def to_dict(self):
        return {
            "pk": self.pk,
            "user": self.user.pk,
            "name": self.name,
            "hostel": self.hostel,
            "room_no": self.room_no,
            "contact_no": self.contact_no,
            "rating": self.rating,
            "no_of_rating": self.no_of_ratings,
            "email": self.email,
        }

    def to_compact_dict(self):
        return {
            "pk": self.pk,
            "user": self.user.pk,
            "name": self.name,
        }


    def __str__(self):
        return self.user.username


@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()

@receiver(post_save,sender=User)
def update_profile(sender,instance,**kwargs):
    instance.profile.save()

class RateUsers(models.Model):
    rating_for = models.ForeignKey(
        User, related_name="ratings_recieved", on_delete=models.PROTECT
    )
    rated_by = models.ForeignKey(
        User, related_name="rating_given", on_delete=models.PROTECT
    )
    rating = models.IntegerField()

    def __str__(self):
        return self.rating_for.username


class ProductManager(models.Manager):
    def tickets():
        return super(ProductManager, self).get_query_set().filter(is_ticket=True)


class Product(models.Model):
    seller = models.ForeignKey(User, related_name="my_items", on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    price = models.IntegerField(blank=False, null=False)
    description = models.CharField(max_length=300)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=4, null=True)
    interested_buyers = models.ManyToManyField(User, blank=True)
    sold = models.BooleanField(default=False)
    is_ticket = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)

    reported_by = models.ForeignKey(
        User,
        related_name="products_reported",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    retrieve = ProductManager()
    objects = models.Manager()

    def to_dict(self):
        return {
            "pk": self.pk,
            "seller": self.seller.pk,
            "price": self.price,
            "description": self.description,
            "interested_buyers": [
                i.profile.to_compact_dict() for i in self.interested_buyers.all()
            ],
            "sold": self.sold,
            "is_ticket": self.is_ticket,
        }

    def __str__(self):
        return self.name
