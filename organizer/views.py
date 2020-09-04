from django.shortcuts import render, render_to_response
from django.http.response import HttpResponse, Http404, HttpResponseNotFound
from .models import Tag,Startup
from django.template import Context,loader,RequestContext
from django.shortcuts import get_object_or_404,redirect
from .forms import TagForm,StartupForm,NewsLinkForm
from django.views.generic import View


def homepage(request):
    return render(request,'organizer/tag_list.html',{'tag_list':Tag.objects.all()}) # using render automatically use RequestContext object


def tag_list(request):
    queryset = Tag.objects.all()
    context = {
        "tag_list": queryset
    }
    return render(request, "organizer/tag_list.html",context)


def tag_detail(request,slug): # this slug parameter value come from url file when a user try to access a page using slug
    tag = get_object_or_404(Tag, slug__iexact=slug) # using this in place of try catch block,the value of the slug variable came from url passing through the parameter of this function, iexact field use the slug field to be case insensitive,search this row in database with case insensitive format,get() method returns a single object,retrieve the tag using slug
    return render(request,'organizer/tag_detail.html',{'tag':tag}) # using render in place of render_to_response,here using 'template_variable':python_variable


def startup_list(request):
    queryset = Startup.objects.all()
    context = {
        "startup_list": queryset
    }
    return render(request,'organizer/startup_list.html',context)


def startup_detail(request,slug): # this parameter value came from url which one user type
    startup = get_object_or_404(Startup,slug__iexact=slug) # take the startup which one match the user given slug
    context = {
        "startup": startup
    }
    return render(request,'organizer/startup_detail.html',context)
'''
# Pseudocode of create a html form
if HTTP method is POST:
    bind data to form
    if the data is valid:
        create new object from data
        show webpage for new object
    else: # if the data is empty or invalid
        show bound HTML form(with errors)
else: # if the HTTP method is GET or other, but not POST
    show unbound HTML form        

'''


def tag_create(request):  # we don't call this function based method,in place we call Class based tag_create method
    if request.method == 'POST': # django also stores any POST data sent to the server as the POST attribute of the HttpRequest obj
        form = TagForm(request.POST) # POST attribute is a dictionary,which means we can directly use the value to instantiate and bind our form
        if form.is_valid():
            new_tag = form.save() # save the form and store the value in new_tag variable
            return redirect(new_tag) # redirect automatically implement get_absolute_url means which is detail page
        # else: # you don't need to use else option,if the form is invalid then it goes to else and shows the form,here when the data is invalid then return the template and also get request it returns the template,those are identical
         #   return render(request,'organizer/tag_form.html',{'form':form}) # when the form is invalid then show just form page,use render() over render_to_response() because render() uses RequestContext allowing django to inject data into our templates,the use of RequestContext is mandatory because of our use of the csrf_token
    else:
        form = TagForm() # when using get method or PUT/OPTIONS method, just display the form
    return render(request,'organizer/tag_form.html',{'form':form}) # always it returns the temp(form is get/post/invalid


class TagCreate(View): # here create class based view(not generic) in place of function based view
    form_class = TagForm # if we use GCBV(like CreateView) than we can use model directly
    template_name = 'organizer/tag_form.html' # the form_class is the form we will use to create an update this data,template_we will load and render with our form_class

    def get(self,request): # get method is using for display the form,here we use form_class attribute for form to instantiate an unbound form and then render it in our template(with a RequestContext for the csrf_token)
        form = self.form_class()  # form_class is TagForm, if anyone use PUT,OPTIONS method then it display http 405 error(method not found)
        context = {'form': form}
        return render(request,self.template_name,context)

    def post(self,request):  # for post method,which is using for submitting the data
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid(): # if data is valid,we create a new Tag and then redirect to its detail page,redirect implement get_absolute_url method and this method holds detail view
            new_tag = bound_form.save()
            return redirect(new_tag) # redirect to get_absolute_url method which holds detail view,here pass 'new_tag' as a slug parameter to this method,and shows the detail view of this tag
        else: # if the data is invalid,then we display form with errors using dictionary
            return render(request,self.template_name,{'form': bound_form})


class StartupCreate(View): # this class is same as TagCreate class,all documantation right above there
    form_class = StartupForm
    template_name = 'organizer/startup_form.html'

    def get(self,request):
        return render(request,self.template_name,{'form':self.form_class()}) # store the dictionary in template

    def post(self,request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_startup = bound_form.save() # if form is valid then create a new obj and redirect(means take get_absolute_url method which refers detail view of Startup)
            return redirect(new_startup)
        else:
            return render(request,self.template_name,{'form':bound_form}) # if form is invalid then display the form with error


class NewsLinkCreate(View):  # this one is same as TagCreate class view,all docs write over there
    form_class = NewsLinkForm
    template_name = 'organizer/newslink_form.html'

    def get(self,request):
        return render(request,self.template_name,{'form':self.form_class()})

    def post(self,request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid(): # if the form is valid then save it and return it
            new_newslink = bound_form.save() # save it to a new variable
            # return redirect(new_newslink)
            return redirect(new_newslink.startup) # rediret means use get_absolute_url which defines detail view,in detail view we need a slug,there are no slug in newslink,so we pass startup attribute of a newslink which has a slug
        else:
            return render(request,self.template_name,{'form':bound_form})


'''
def homepage(request):
    tag_list = Tag.objects.all() # take all of the tags store into tag_list
    template = loader.get_template('organizer/tag_list.html') # load the templates,passing in a path relative to templates/ directory
    # context = RequestContext(request, {'tag_list': tag_list}) # it's not working django 2.0, sometimes django needs to make changes to the values within the context objects,to enable django to make changes to data that render a template,we must use RequestContext instead of a Context obj
    context = {'tag_list': tag_list} # create a dictionary where passing the tag_list, context = Context({'template_variable':python_variable}),here you don't need to use 'Context' in django 2 version
    output = template.render(context) # render Template with the Context by calling render()
    return HttpResponse(output) # pass text output of the function to HttpResponse
    
    #return render_to_response('organizer/tag_list.html',{'tag_list': Tag.objects.all()}) # here using django shortcut render_to_response in place of all codes which one we commented
'''

'''
def tag_detail(request,slug):
    tag = get_object_or_404(Tag,slug__iexact=slug)  # using this in place of try catch block
    template = loader.get_template('organizer/tag_detail.html')
    # context = RequestContext(request,{'tag':tag}) # if we change the value inside the context we should use RequestContext,RequestContext needs the HttpRequest object
    context = {'tag': tag} # pass the python variable tag to html variable tag using context
    return HttpResponse(template.render(context))

    # return render_to_response('organizer/tag_detail.html',{'tag':tag}) # this is shortcut in place of all codes
    
    # try:
    #    tag = Tag.objects.get(slug__iexact=slug)  # the value of the slug variable came from url passing through the parameter of this function, iexact field use the slug field to be case insensitive,search this row in database with case insensitive format,get() method returns a single object,retrieve the tag using slug
    # except Tag.DoesNotExist: # if a slug is not in database then shows exception(then the tag is not in database)
            # return HttpResponseNotFound('<h1>Tag not found!</h1>') # in production 404 error return automatically
    #        raise Http404
'''


'''
def homepage(request):
    tag_list = Tag.objects.all()
    output = ", ".join([tag.name for tag in tag_list]) # take the all tag name from tag_list and store into a string,delinating each item with comma and space
    return HttpResponse(output)

def homepage(request):
    tag_list = Tag.objects.all()
    html_output = "<html>\n"
    html_output += "<head>\n"
    html_output += " <title>"
    html_output += "Don't Do this!</title>\n"
    html_output += "</head>\n"
    html_output += "<body>\n"
    html_output += " <ul>\n"
    for tag in tag_list:
        html_output += "  <li>"
        html_output += tag.name.title()
        html_output += "<li>\n"
    html_output += "  <ul>\n"
    html_output += "<body>\n"
    html_output += "<html>\n"
    return HttpResponse(html_output)
'''



