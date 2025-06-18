from django.db import models
from django.utils.timezone import now


# class ContactMessage(models.Model):
#     full_name = models.CharField(max_length=255)
#     email = models.EmailField()
#     subject = models.CharField(max_length=255)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Message from {self.full_name} - {self.email}"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    message = models.TextField()
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Hashtag(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tool(models.Model):
    name = models.CharField(max_length=200)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    logo_url = models.URLField(max_length=500, blank=True, null=True)
    description = models.TextField()
    upvote_count = models.PositiveIntegerField(default=0)
    trend_count = models.PositiveIntegerField(default=0)  
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    is_verified = models.BooleanField(default=False)
    url = models.URLField(max_length=200, blank=True, null=True)
    rank_in_category = models.PositiveIntegerField(default=0)

    # Relations
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tools')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='tools')
    hashtags = models.ManyToManyField(Hashtag, related_name='tools')

    # Timestamps
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name
