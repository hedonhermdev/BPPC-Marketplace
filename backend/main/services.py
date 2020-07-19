from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


# --------- CELERY TASKS -------------



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
    if instance.email != "" and instance.permission_level == Profile.UNSET:
        tasks.set_permission_level.delay(instance.id)
    """
    When a new user is created, set its permission_level according to its email.
    BITSIAN -> SELLER
    NON-BITSIAN -> BUYER
    """
    if instance.email != "" and instance.permission_level is not None:
        domain = instance.email.split("@")[1]

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
    if (
        (instance.name != "")
        and (instance.hostel != "")
        and (instance.contact_no != "")
    ):
        instance.is_complete = True
    else:
        instance.is_complete = False


@receiver(post_save, sender=ProfileRating)
def update_profile_rating(sender, instance, created, **kwargs):
    """
    Update the average rating of a profile when a new rating is given to the profile.
    """
    if created:
        tasks.update_profile_rating.delay(instance.rating_for.id, instance.rating.id)


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


@receiver(post_save, sender=ProductOffer)
def update_product_offers(sender, instance, created, **kwargs):
    """
    Update the number of offers of a product when a new offer is made.
    """
    if created:
        tasks.update_product_offers.delay(instance.product.id)
