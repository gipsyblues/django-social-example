from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()


class Image(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name="images")
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, blank=True, null=True)
    url = models.URLField()
    image = models.ImageField(upload_to="images/%Y/%m/%d/")
    description = models.TextField(blank=True, null=True)
    users_like = models.ManyToManyField(User, related_name="liked_images", blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)
    created = models.DateField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created",)

    def get_absolute_url(self):
        return reverse("images:detail", kwargs=dict(id=self.id, slug=self.slug))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
