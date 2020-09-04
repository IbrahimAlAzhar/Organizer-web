from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404,render,redirect
from django.views.generic import View
from django.views.decorators.http import require_http_methods
from .forms import PostForm


class PostList(View): # here use class based function not Generic class based view,inherit from View function
    #template_name = 'blog/post_list.html' # using template_name for DRY(don't repeat yourself) principle
    template_name = 'blog/post_list.html' # the template pass in url as_view() function

    def get(self,request, parent_template=None): # python method parameter is self and take request parameter,parent template value come from url file,default is None
        queryset = Post.objects.all() # here the method name is get,so our method will be called only if the user's browser issues an HTTP GET request ot a URL that is matched by our URL pattern,post() method is use on HTTP POST request
        context = {
            'post_list': queryset,
            'parent_template': parent_template # passing parent_template variable to html file,in html file of blog apps,the parent template is 'base_blog.html' file which is define on header in html file
        }
        return render(request,self.template_name,context) # render instantiate an HtttpResponse object,render shortcuts uses a RequestContext instead of Context object,render() is slower than render_to_response()


@require_http_methods(['HEAD','GET']) # here using decorator to set which HTTP methods are allowed on each of our function views,any request with other methods will return an HTTP 405 error(shows method not allowed)
def post_detail(request,year,month,slug,parent_template=None): # this parameter's value come from url file which one input by user,here we using parent_template parameter which value pass from url file,default is None
    post = get_object_or_404(Post,pub_date__year=year, # get the object using this filter like year,month and slug
                             pub_date__month=month, # here first n-1 will call filter and nth will result in a call get
                             slug=slug)
    context = {
        'post': post, # store the value of python variable post to template variable 'post'
        'parent_template': parent_template # the parent template is 'base.html' which is define on urls file,this 'parent_template' variable pass onto template using context dictionary
    }
    return render(request,'blog/post_detail.html',context) # render to load the template,shortcuts then returns an HttpResponse object to the view,which view passes on to django


class PostCreate(View): # here create class based view(not generic) in place of function based view
    form_class = PostForm # pass the form class as a template variable form to html file, the form_class is the form we will use to create an update this data,template_we will load and render with our form_class
    template_name = 'blog/post_form.html' # if we use GCBV(like CreateView) than we can use model directly

    def get(self,request): # in get request,just display the form,get method is using for display the form,here we use form_class attribute for form to instantiate an unbound form and then render it in our template(with a RequestContext for the csrf_token)
        return render(request,self.template_name,{'form':self.form_class()})

    def post(self,request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid(): # if data is valid,we create a new Tag and then redirect to its detail page,redirect implement get_absolute_url method and this method holds detail view
            new_post = bound_form.save()
            return redirect(new_post)  # redirect to get_absolute_url method which holds detail view,here pass 'new_tag' as a slug parameter to this method,and shows the detail view of this tag
        else:
            return render(request,self.template_name,{'form':bound_form})

# here this is function based view,we use Class Based View(not Generic) in place of function based view


def post_create(request):  # we don't call this function based method,in place we call Class based PostCreate method
    if request.method == 'POST': # django also stores any POST data sent to the server as the POST attribute of the HttpRequest obj
        form = PostForm(request.POST) # POST attribute is a dictionary,which means we can directly use the value to instantiate and bind our form
        if form.is_valid():
            new_post = form.save() # save the form and store the value in new_tag variable
            return redirect(new_post) # redirect automatically implement get_absolute_url means which is detail page
        # else: # you don't need to use else option,if the form is invalid then it goes to else and shows the form,here when the data is invalid then return the template and also get request it returns the template,those are identical
         #   return render(request,'organizer/tag_form.html',{'form':form}) # when the form is invalid then show just form page,use render() over render_to_response() because render() uses RequestContext allowing django to inject data into our templates,the use of RequestContext is mandatory because of our use of the csrf_token
    else:
        form = PostForm() # when using get method or PUT/OPTIONS method, just display the form
    return render(request,'blog/post_form.html',{'form':form}) # always it returns the temp(form is get/post/invalid



'''
def post_list(request): # view function accepts HttpRequest object as argument and return Httpresponse object
    queryset = Post.objects.all() # take all object of Post model
    context = {
        "post_list": queryset
    }
    return render(request,'blog/post_list.html',context)
'''
