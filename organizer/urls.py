from django.conf.urls import url
from .views import StartupCreate,TagCreate,homepage, tag_detail,tag_list, startup_list, startup_detail,tag_create
from django.urls import path

urlpatterns = [
    path('tag/',tag_list,name='organizer_tag_list'),
    # path('tag/create/',tag_create,name='organizer_tag_create'), # we must give precedence tag_create over tag_detail url,if we use tag_create before tag_detail then running server requisting tag/create/ will call tag_detail view and shows http 404 error('create' tag does not exist)
    path('tag/create/',TagCreate.as_view(),name='organizer_tag_create'),
    url(r'^tag/(?P<slug>[\w\-]+)/$',tag_detail,name='organizer_tag_detail'), # here (?P<name>pattern),use '+' character to match at least one character,'\w' will match alphanumeric characters and the underscore(-), ^=start symbol,$=end symbol
    path('startup/',startup_list,name='organizer_startup_list'),
    url(r'^startup/(?P<slug>[\w\-]+)/$',startup_detail,name='organizer_startup_detail'),
    path('startup/create/',StartupCreate.as_view(),name='organizer_startup_create'),
]

