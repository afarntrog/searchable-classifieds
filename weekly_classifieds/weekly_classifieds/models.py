from django.db import models

# Create your models here.

# only store this weeks paper. bec if last week job not in this week then must be taken
class JobPosts(models.Model):
    job_post = models.TextField()

    def __str__(self):
        return self.job_post[:50]

class Date(models.Model):
    week_date = models.CharField(max_length=30)

    def __str__(self):
        return self.week_date