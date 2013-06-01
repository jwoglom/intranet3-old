from django.db import models
from django.contrib import admin

# Create your models here.

class User(models.Model):
    USER_GRADES = (
        ('9', 'Freshman'),
        ('10', 'Sophomore'),
        ('11', 'Junior'),
        ('12', 'Senior'),
        ('staff', 'Staff Member'),
        ('office', 'Office Admin'),
        ('other', 'Other'),
    )
    USER_CLASSYRS = (
        ('14', '2014'),
        ('15', '2015'),
        ('16', '2016'),
        ('17', '2017'),
        ('00', 'Other'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_id = models.CharField(max_length=30)
    email_addr = models.EmailField(blank=True, null=True)
    grade = models.CharField(max_length=10, choices=USER_GRADES, default='other')
    class_yr = models.CharField(max_length=10, choices=USER_CLASSYRS, default='00')
    absences = models.IntegerField(default=0)

    def __unicode__(self):
        return u'%s %s (%s) - %s' % (self.first_name, self.last_name, self.user_id, self.grade)

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'user_id', 'grade', 'class_yr', 'absences')

admin.site.register(User, UserAdmin)

class Room(models.Model):
    name = models.CharField(max_length=10)
    desc = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.desc)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc')

admin.site.register(Room, RoomAdmin)

class Staff(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_id = models.CharField(max_length=30)
    email_addr = models.EmailField()
    can_sponsor_acts = models.BooleanField(default=True)
    staff_rooms = models.ManyToManyField(Room, blank=True, null=True, related_name='staff_rooms')

    def __unicode__(self):
        return u'%s %s (%s)' % (self.first_name, self.last_name, self.user_id)

class StaffAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'user_id')

def get_sponsor_default():
    return Staff.objects.get(id=1)

admin.site.register(Staff, StaffAdmin)

class EighthActivity(models.Model):
    name = models.CharField(max_length=50)
    room = models.ForeignKey(Room, blank=True, null=True)
    sponsor = models.ForeignKey(Staff, default=get_sponsor_default)
    max_size = models.IntegerField()
    restricted = models.BooleanField(default=False)
    restricted_to = models.ManyToManyField(User, blank=True, null=True, related_name='restricted_to')
    restricted_for = models.ManyToManyField(User, blank=True, null=True, related_name='restricted_for')
    cancelled = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    hidden_to = models.ManyToManyField(User, blank=True, null=True, related_name='hidden_to')

    def __unicode__(self):
        return u'%s (%s) (%s - %i)' % (self.name, self.sponsor, self.room, self.max_size)

class EighthActivityAdmin(admin.ModelAdmin):    
    list_display = ('name', 'room', 'sponsor', 'max_size', 'cancelled', 'hidden')

admin.site.register(EighthActivity, EighthActivityAdmin)

class EighthBlock(models.Model):
    block_name = models.CharField(max_length=1)
    block_date = models.DateField()
    block_daynum = models.IntegerField()
    block_acts = models.ManyToManyField(EighthActivity, related_name='block_acts')
    def __unicode__(self):
        return u'%s (%s)' % (self.block_name, self.block_date)
class EighthBlockAdmin(admin.ModelAdmin):
    list_display = ('block_date', 'block_name', 'block_daynum')

admin.site.register(EighthBlock, EighthBlockAdmin)

class EighthActivityBlock(models.Model):
    block = models.ManyToManyField(EighthBlock)
    activity = models.ForeignKey(EighthActivity)
    signed_up_users = models.ManyToManyField(User, blank=True, null=True, related_name='signed_up_users')

    def __unicode__(self):
        return u'%s %s' % (self.activity, self.block)

#class EighthActivityBlockAdmin(admin.ModelAdmin):
#    list_display = ('block', 'activity', 'signed_up_users')

admin.site.register(EighthActivityBlock)  #, EighthActivityBlockAdmin)
