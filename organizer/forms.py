from django import forms
from .models import Tag, NewsLink, Startup
from django.core.exceptions import ValidationError


class SlugCleanMixin:
    # mixin class for slug cleaning method
    def clean_slug(self):  # field specific clean method
        new_slug = (self.cleaned_data['slug'].lower())  # here we create lower form of slug for store into database
        if new_slug == 'create':  # we can't use the slug name 'create',because it is url path name
            raise ValidationError('Slug may not be "create".')
        return new_slug


class TagForm(SlugCleanMixin,forms.ModelForm): # here extend ModelForm in place of form for DRY(don't repeat yourself) principle
    # here this class inherit from SlugCleanMixin,so we don't need to create clean_slug method,it's automatically works
    class Meta:  # using class meta for declaring this form is mirror of model
        model = Tag # if we using modelForm then we don't need to use save method for creating a new obj
        # fields = '__all__'  # here we use all attributes of model,we can customize this by using the name of attr.
        # exclude = ['slug'] # we can also use exclude in place of fields,here exclude slug and rest of store in fields
        # exclude = tuple() # here exclude nothing
        fields = ['name','slug']  # using class meta for mapping into model then many of the model fields like verbose_name,help_text are in forms

    def clean_name(self): # a user can type the tag name is all caps,then we have to do lowercase for other purposes
        return self.cleaned_data['name'].lower() # all lowercase tag name store in database


class NewsLinkForm(forms.ModelForm): # her using modelForm so we don't need to create form field explicitly
    class Meta:   # we also don't need to use save() method for validation and create instance
        model = NewsLink
        fields = '__all__' # we can use define fields explicitly


class StartupForm(SlugCleanMixin,forms.ModelForm):
    # here this class inherit from SlugCleanMixin,so we don't need to create clean_slug method,it's automatically works during the data cleaning process
    class Meta: # don't need to define save() method,here automatically do this,save() method create or update an obj in database
        model = Startup
        fields = '__all__'
        # fields = ['name','slug','description']

'''
class TagForm(forms.Form): # extend from Form,must mirror the model fields,if we use ModelForm then just define fields
    name = forms.CharField(max_length=31) # instead of models.Fieldname we use forms.FieldName
    slug = forms.SlugField(max_length=31,help_text='A label for URL config') # a model field knows how to represent data in database but a form field is associated with a django widget,which is nothing more than an HTML field

    def save(self): # here using save method for saving the form,we can do this also in views file
        # save method is act of returning new object,it's manipulate new data in other locations like view
        new_tag = Tag.objects.create(  # create a new instance of class using model
            name=self.cleaned_data['name'],  # using cleaned_data which one secure for validation,don't use self.name
            slug=self.cleaned_data['slug']  # here store the name,slug value from form cleaned_date(validate data)
        )
        return new_tag

    def clean_name(self): # a user can type the tag name is all caps,then we have to do lowercase for other purposes
        return self.cleaned_data['name'].lower() # all lowercase tag name store in database

    def clean_slug(self):
        new_slug = (self.cleaned_data['slug'].lower()) # here we create lower form of slug for store into database
        if new_slug == 'create':  # we don't need to create slug,
            raise ValidationError('Slug may not be "create".')
        return new_slug
'''