from django.db import models
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=31,unique=True)
    slug = models.SlugField(max_length=31,unique=True,help_text='A label for URL config') # help text is quick information what is slug is

    def __str__(self):
        return self.name.title() # here using title for captalizing the name field,representation of object in the interpreter and admin

    class Meta:
        ordering = ['name']  # order our tag model alphabetically by the model's name field

    def get_absolute_url(self): # get_absolute_url() method is helpful only for detail pages,for list pages,we'll continue to use reverse() and the url template tag
        return reverse('organizer_tag_detail',kwargs={'slug':self.slug}) # when need to detail of tag,then we call this method,here it returns the url name of tag detail url,pass slug as a argument which needs on url
        # return reverse('organizer_tag_detail',args=(self.slug,)) # here using args in place of kwargs


class Startup(models.Model):
    name = models.CharField(max_length=31, db_index=True) # here applying database indexing
    slug = models.SlugField(max_length=31, unique=True, help_text='A label for URL config.')
    description = models.TextField()
    founded_date = models.DateField('date founded')
    contact = models.EmailField()
    website = models.URLField(max_length=255)
    tags = models.ManyToManyField(Tag) # a startup has multiple tag and a same tag in multiple startup,we could have just as easily created this realtionship in the Tag model by adding an attribute startups.

    def __str__(self):
        return self.name  # for string representation of this class

    class Meta:
        ordering = ['name'] # order lists of startup by name but specify that the latest startup should be the object with most recent founded_date
        get_latest_by = 'founded_date'

    def get_absolute_url(self): # using this method for detail view of startup when it calls
        return reverse('organizer_startup_detail',kwargs={'slug': self.slug}) # pass the parameter self.slug to slug varibale using kwargs dictionary,this parameter needs because urls.py file needs slug
        # return reverse('organizer_startup_detail',args=(self.slug))


class NewsLink(models.Model):
    title = models.CharField(max_length=63)
    pub_date = models.DateField('date published')
    link = models.URLField(max_length=255)
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE) # here one newslink has multiple startup but not reverse, here using one to many relationship on startup and newslink,in one to many field we have to define 'on_delete' where if a field is delete then the releven all field also remove

    def __str__(self):
        return "{}:{}".format(self.startup, self.title) # here show not only title of the link but also which startup object the link is related to

    class Meta:
        verbose_name = 'news article' # this attribute defines the way django displays instances of our models,to display all of instance of this model using verbose_name,normally appending 's' for using verbose_name
        ordering = ['-pub_date']  # using pub_date for ordering,if dash is provide django will order from newest to oldest
        get_latest_by = 'pub_date'  # getting the latest objects using pub_date

    #def get_absolute_url(self): # use this get_absolute url is set to startup get_absolute_url method which define the detail view of startup
       # return self.startup.get_absolute_url() # if i use
