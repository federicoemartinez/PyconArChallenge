from __future__ import unicode_literals
import uuid

from django.db import models

# Create your models here.

class Submission(models.Model):
    submission_time = models.DateTimeField(auto_now_add=True, blank=True)
    email = models.EmailField(blank=False, db_index=True)
    name = models.TextField(blank=True)
    lastname = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    is_correct = models.BooleanField()

class HackDetection(models.Model):
    email = models.EmailField(blank=False, db_index=True)



class Token(models.Model):
    uniqid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)

