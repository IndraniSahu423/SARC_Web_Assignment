from django.db import models


class LocalUserProfile(models.Model):
    roll_number = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    hostel_number = models.CharField(max_length=50)
    bio = models.TextField(blank=True, default="")
    year_of_study = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.roll_number} - {self.name}"
