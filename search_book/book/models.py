from django.db import models

# Create your models here.


class Book(models.Model):
    """Model to represent the fields of book"""
    class Meta:
        """Meta class for this model."""
        ordering = ['id']
    
    title = models.CharField(max_length=200,
                             null=False, blank=False)
    download_count = models.IntegerField()
    rating_avg = models.FloatField(
        null=False,
        blank=False,
        default=0.0
    )

    def update_rating_avg(self):
        reviews = Review.objects.filter(book__id=self.id)
        num = len(reviews)
        rating = 0
        for review in reviews:
            rating += review.rating
        if num != 0:
            self.rating_avg = rating / num
            self.save()
            

class Authors(models.Model):
    """Model to represent the fields of authors"""
    class Meta:
        """Meta class for this model."""
        ordering = ['id']
    
    name = models.CharField(max_length=400,
                            null=False, blank=False)
    birth_year = models.IntegerField()
    death_year = models.IntegerField()
    books = models.ManyToManyField(
        Book,
        related_name='authors')


class Language(models.Model):
    """Model to represent the fields of language"""
    class Meta:
        """Meta class for this model."""
        ordering = ['id']
    
    language = models.CharField(max_length=10,
                                null=False, blank=False)
    books = models.ManyToManyField(
        Book,
        related_name='languages')


class Review(models.Model):
    """Model to represent the fields of review"""
    class Meta:
        """Meta class for this model."""
        ordering = ['id']
    
    review = models.CharField(max_length=1000,
                              null=False, blank=False)
    rating = models.IntegerField()
    book = models.ForeignKey(
        Book,
        related_name='reviewers',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
