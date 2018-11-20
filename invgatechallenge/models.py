from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Submission(models.Model):
    submission_time = models.DateTimeField(auto_now_add=True, blank=True)
    email = models.EmailField(blank=False, db_index=True)
    is_correct = models.BooleanField()

class HackDetection(models.Model):
    email = models.EmailField(blank=False, db_index=True)


class Token(models.Model):
    pass

