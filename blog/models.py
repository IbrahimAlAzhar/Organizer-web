from django.db import models
from organizer.models import Startup,Tag
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=63)
    slug = models.SlugField(max_length=63, help_text='A label for URL config', unique_for_month='pub_date')  # Slugfield is a Charfield with validation,slug is unique according to the month,we don't care if blog posts with have same name because the years and months is always different,if the month is same then check uniqueness
    text = models.TextField()
    pub_date = models.DateField('date published', auto_now_add=True) # python uses datetime.date,publication date is automatically added,our field would be updated each and every time the model is modified,date automatically added,you can also override it
    tags = models.ManyToManyField(Tag,related_name='blog_posts') # Tag are attributes,we can define this many to many relationship in Tag model,related name option we've passed to our relationship fields,related name attribute is a tag can access all of his including posts by using 'blog_posts',if we don't created related name attribute then django creates automatically 'post_set' attribute
    startups = models.ManyToManyField(Startup,related_name='blog_posts') # here startup is an attribute of the blog post, a blog has multiple startup and a same startup is in multiple blog, a startup can access all of its related posts by using related_name parameter

    def __str__(self):
        return "{} on {}".format(self.title,self.pub_date.strftime('%Y-%m-%d')) # strftime is datetime.date objects in python

    class Meta:
        verbose_name = 'blog_post' # to access all of objects of this class
        ordering = ['-pub_date', 'title']  # ordering using pub_date,if pub_date of two posts is same then using title
        get_latest_by = 'pub_date'

    def get_absolute_url(self):  # this method is callable when we need to access detail view of post
        return reverse('blog_post_detail',  # call the url name which is post detail
                       kwargs={  # pass the parameter like year,month,slug to urls,pub_date is attribute of models
                           'year': self.pub_date.year,
                           'month': self.pub_date.month,
                           'slug': self.slug
                       })