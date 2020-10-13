import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import FormView
from .forms import PostAdForm
from .models import PostAd

data = {}
list = ()

with open('spells.txt') as json_file:
    data = json.load(json_file)
    index = 0
    for key in data:
        list += (('SP' + str(index), key),)
        index += 1

class PostAdPage(FormView):
    template_name = 'post_ads.html'
    # success_url = '/awesome/'
    form_class = PostAdForm

    # def get_name(request):
    #     # if this is a POST request we need to process the form data
    #     if request.method == 'POST':
    #         # create a form instance and populate it with data from the request:
    #         form = PostAdForm(request.POST)
    #         # check whether it's valid:
    #         if form.is_valid():
    #             # process the data in form.cleaned_data as required
    #             # ...
    #             # redirect to a new URL:
    #             # return HttpResponseRedirect('/thanks/')
    #             return HttpResponse(form.cleaned_data['category'])
    #
    #     # if a GET (or any other method) we'll create a blank form
    #     else:
    #         form = PostAdForm()
    #
    #     # return render(request, 'post_ads.html', {'form': form})
    #     return HttpResponse(form.cleaned_data['category'])

    def form_valid(self, form):
        return HttpResponse(self.request.accepts())
