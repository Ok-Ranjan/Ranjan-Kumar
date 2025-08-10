from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(help_text="Enter skill level (0-100)")

    def _str_(self):
        return f"{self.name} ({self.level}%)"

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    github_link = models.URLField(blank=True, null=True)
    demo_link = models.URLField(blank=True, null=True)
    preview_image = models.ImageField(upload_to='project/',blank=True, null=True)
    preview_video = models.FileField(upload_to='project/videos', blank=True, null=True)

    def __str__(self):
        return self.title
    
class Achievement(models.Model):
    title = models.CharField(max_length = 200)
    description = models.TextField(blank=True, null=True)
    certificate_image = models.ImageField(upload_to=';achievements/')
    date_awarded = models.DateField(blank=True, null=True)

    def _str_(self):
        return self.title
    
class Resume(models.Model):
    title = models.CharField(max_length=100, default="My Resume")
    pdf_file = models.FileField(upload_to='resume/')

    def __str__(self):
        return self.title
    