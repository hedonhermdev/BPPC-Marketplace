from django.db import models
from django.contrib.auth.models import User

HOSTEL_CHOICES = (
    ("SR","SR Bhavan"),
    ("RP","Rana Pratap Bhavan"),
    ("GN","Gandhi Bhavan"),
    ("KR","Krishna Bhavan"),
    ("MR","Meera Bhavan"),

)
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    hostel = models.CharField(choices=HOSTEL_CHOICES,max_length=2)
    room_no = models.PositiveIntegerField()
    contact_no = models.PositiveIntegerField()
    rating = models.DecimalField(max_digits=2,decimal_places=1,null=True,blank=True)
    no_of_ratings = models.IntegerField(default=0)
    email = models.EmailField()

    def save(self):
        """
        always updae the rating of user
        """
        user = self.user
        raters = user.ratings_recieved.all()

        rate_points = 0
        no_of_ratings = 0
        for r in raters:
            rate_points = r.rating + rate_points
            no_of_ratings = no_of_ratings +1
        
        self.no_of_ratings = no_of_ratings
        rating = rate_points/no_of_ratings
        self.rating = round(rating,1)

        super.save()

    def to_dict(self):
        return{
            'pk': self.pk,
            'user': self.user.pk,
            'name': self.name,
            'hostel': self.hostel,
            'room_no': self.room_no,
            'contact_no': self.contact_no,
            'rating': self.rating,
            'no_of_rating': self.no_of_ratings,
            'email': self.email,
        
        }

class RateUsers(models.Model):
    rating_for = models.ForeignKey(User,related_name='ratings_recieved',on_delete=models.PROTECT)
    rated_by = models.ForeignKey(User,related_name='rating_given',on_delete=models.PROTECT)
    rating = models.IntegerField()

class ProductManager(models.Manager):
    def tickets():
        return super(ProductManager,self).get_query_set().filter(is_ticket=True)

class Product(models.Model):
    seller = models.ForeignKey(User,related_name='my_items',on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    price = models.IntegerField(blank=False,null=False)
    description = models.CharField(max_length=300)
    interested_buyers = models.ManyToManyField(User)
    sold = models.BooleanField(default=False)
    is_ticket = models.BooleanField(default=False)
    
    retrieve = ProductManager()
    objects = models.Manager()

    def to_dict(self):
        return{
            'pk': self.pk,
            'seller': self.seller.pk,
            'price': self.price,
            'description': self.description,
            'interested_buyers': [i.profile.to_dict() for i in self.interested_buyers.all()],
            'sold': self.sold,
            'is_ticket': self.is_ticket,
        }


 


        

