from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile

# signal receiver
@receiver(post_save, sender=User)
def create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance) 
        # automatically create user profile


    else: # update the profile if the user update
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # create the user profile if not exist
            UserProfile.objects.create(user=instance)

@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    pass
    # print(instance.username, "this user is being created")
    