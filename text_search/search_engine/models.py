from django.db import models
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, get_list_or_404


class PageManager(models.Manager):

    def get_page(self, text):
        return get_list_or_404(Page, text__icontains=text)


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Book(models.Model):
    title = models.CharField(max_length=200)
    pages_number = models.PositiveIntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()

    def __str__(self):
        return str(self.title)


class Page(models.Model):
    number = models.PositiveIntegerField()
    text = models.TextField()
    part_name = models.CharField(max_length=200)
    section_name = models.CharField(max_length=200)
    chapter_name = models.CharField(max_length=200)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    objects = PageManager()

    def __str__(self):
        return str(self.number)
