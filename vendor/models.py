from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification
from datetime import time
from datetime import date, datetime

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100,unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.vendor_name
    
    # check the vendor if it's open now
    def is_open(self):
        # check current days' opening hour
        today_day = date.today() # get today's date 2023-11-16
        today = today_day.isoweekday() # get weekday 4 (Thursday)
        current_day_open_hours = OpeningHour.objects.filter(vendor=self, day=today)
        # current time
        now = datetime.now() # now time
        current_time = now.strftime('%H:%M:%S') # change to 15:40:39 (format, string)

        is_open = None
        for i in current_day_open_hours:
            if not i.is_closed:
                start = str(datetime.strptime(i.start_hour,'%I:%M %p').time()) # convert to time
                end = str(datetime.strptime(i.end_hour,'%I:%M %p').time())
                if current_time > start and current_time < end:
                    is_open = True
                    break
                else:
                    is_open = False
            else:
                is_open = False
        return is_open
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            # update
            original_status = Vendor.objects.get(pk = self.pk)
            if original_status.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email,
                }
                if self.is_approved == True:
                    # send notification email
                    mail_subject = "Congratulations! Your restaurant has been approved."
                    send_notification(mail_subject, mail_template, context)
                else:
                    # send error email
                    mail_subject = "Sorry! You are not eligible for publishing your products on our marketplace."
                    send_notification(mail_subject, mail_template, context)
        return super(Vendor, self).save(*args, **kwargs)

days = [
    (1, ("Monday")), # 1 is value, ("monday") is label
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Satuarday")),
    (7, ("Sunday")),
]    
# datetime
hours = [(time(h,m).strftime('%I:%M %p'),(time(h,m).strftime('%I:%M %p'))) 
         for h in range(0,24) for m in (0,30)]


class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=days)
    start_hour = models.CharField(choices=hours, max_length=10, blank=True)
    end_hour = models.CharField(choices=hours, max_length=10,blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day', '-start_hour')
        unique_together = ('vendor','day', 'start_hour', 'end_hour')

    def __str__(self) -> str:
        return self.get_day_display()