from django.conf.urls import url
from django.urls import path
from .views import PostList, post_detail, PostCreate

urlpatterns =[
    path('', PostList.as_view(),  # here using a dictionary to override the base template of our view
         name='blog_post_list'), # as_view() method is provided by the inheritance of the View superclass and ensures that the proper method in our Class Based View is called,,as_view() will direct Django to get() method
    url(r'^(?P<year>\d{4})/' r'(?P<month>\d{1,2})/' r'(?P<slug>[\w\-]+)/$', # year has 4 digits,a month has 1 or 2 digits,and finally our slug is set of alphanumeric(w),underscore(-) or dash charchters
        post_detail,name='blog_post_detail'), # pass the parameter year,month and slug to view function,& this one came from user input,,year,month,slug value which one user given pass onto view function
    path('create/',PostCreate.as_view(),name='blog_post_create'),
]

# as_view() returns a view(a method on the instance of PostList),its main purpose is to define a function that acts as
# an intermediary view,it receives all the data,figures out which CBV method to call,and then passes all the data to
# that method
