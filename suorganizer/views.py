from django.http import HttpResponseRedirect
from django.shortcuts import redirect


def redirect_root(request): # in home url the view goes into blog url
    return redirect('blog_post_list') # instead of using HtttpResponseRedirect we use django shortcut redirect(),to bettr adhere to DRY principle,list view url name is 'blog_post_list'
    # return HttpResponseRedirect('/blog/') # redirect() shortcut also allows the developer to pass in an abs url path

'''
def redirect_root(request):
    url_path = reverse('blog_post_list')
    return HttpResponseRedirect(url_path) # redirect is more efficent then HttpResponseRedirect,the redirect() shortcuts 
# uses the reverse() method on the name of the url pattern and then uses this value to redirect the page via a HttpRespo
-nseRedirect
'''
