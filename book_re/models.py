# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

class Bookrating(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    user_id = models.IntegerField(db_column='User_Id', blank=True, null=True)  # Field name made lowercase.
    name = models.IntegerField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    rating = models.IntegerField(db_column='Rating', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bookrating'


class Books(models.Model):
    id = models.IntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=999, blank=True, null=True)  # Field name made lowercase.
    ratingdist1 = models.CharField(db_column='RatingDist1', max_length=999, blank=True, null=True)  # Field name made lowercase.
    pagesnumber = models.IntegerField(db_column='pagesNumber', blank=True, null=True)  # Field name made lowercase.
    ratingdist4 = models.CharField(db_column='RatingDist4', max_length=999, blank=True, null=True)  # Field name made lowercase.
    ratingdisttotal = models.CharField(db_column='RatingDistTotal', max_length=999, blank=True, null=True)  # Field name made lowercase.
    publishmonth = models.IntegerField(db_column='PublishMonth', blank=True, null=True)  # Field name made lowercase.
    publishday = models.IntegerField(db_column='PublishDay', blank=True, null=True)  # Field name made lowercase.
    publisher = models.CharField(db_column='Publisher', max_length=999, blank=True, null=True)  # Field name made lowercase.
    countsofreview = models.IntegerField(db_column='CountsOfReview', blank=True, null=True)  # Field name made lowercase.
    publishyear = models.IntegerField(db_column='PublishYear', blank=True, null=True)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=999, blank=True, null=True)  # Field name made lowercase.
    authors = models.CharField(db_column='Authors', max_length=999, blank=True, null=True)  # Field name made lowercase.
    rating = models.FloatField(db_column='Rating', blank=True, null=True)  # Field name made lowercase.
    ratingdist2 = models.CharField(db_column='RatingDist2', max_length=999, blank=True, null=True)  # Field name made lowercase.
    ratingdist5 = models.CharField(db_column='RatingDist5', max_length=999, blank=True, null=True)  # Field name made lowercase.
    isbn = models.CharField(db_column='ISBN', max_length=999, blank=True, null=True)  # Field name made lowercase.
    ratingdist3 = models.CharField(db_column='RatingDist3', max_length=999, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'books'


class Cart(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    userid = models.CharField(db_column='UserID', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bookid = models.CharField(db_column='BookID', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cart'


class User_cast(models.Model):
    cast_id = models.AutoField(db_column='Id', primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Chat_record(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.IntegerField(blank=True, null=True)
    question = models.CharField(max_length=200, blank=True, null=True)
    answer = models.CharField(max_length=200, blank=True, null=True)

