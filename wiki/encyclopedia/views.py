from django.shortcuts import render
import markdown      # to convert from MD to HTML
from django.http import Http404
from django.shortcuts import redirect
from django import forms
from random import choice
import re

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    if (entry_content := util.get_entry(title)):
        # generate HTML from MD and store in a string
        entry_content_html = markdown.markdown(entry_content)
        # return also title. useful for edit_entry redirect
        return render(request, "encyclopedia/entry.html", {"entry_content": entry_content_html, "entry_title": title})
    else:
        raise Http404("Entry not found")  # error page


def search(request):
    query = request.GET["q"]

    if any(query.lower() == entry.lower() for entry in util.list_entries()):
        return redirect("entry", query)   # call entry function

    else:
        results = []
        for entry in util.list_entries():
            if query.lower() in entry.lower():
                results.append(entry)
        return render(request, "encyclopedia/search.html", {"results": results})


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': "Write a title"}
    ))
    content = forms.CharField(
        label="Content",
        widget=forms.Textarea(
            attrs={'class': 'form-control',
                   'placeholder': "Write a description"}
        ))


def new_entry(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if any(title.lower() == entry.lower() for entry in util.list_entries()):
            # duplicated title, error message
            return render(request, "encyclopedia/new_entry.html", {
                "form": NewEntryForm(),
                "error": "Title already exists. Please choose a different title."
            })
        else:
            # save title and content
            util.save_entry(title, content)
            return redirect("entry", title)

    else:  # GET request
        return render(request, "encyclopedia/new_entry.html", {"form": NewEntryForm()})


def edit_entry(request, title):
    if request.method == "GET":
        entry_content = util.get_entry(title)
        return render(request, "encyclopedia/edit_entry.html", {"entry_content": entry_content, "entry_title": title})

    else:  # POST
        content = request.POST.get("content")
        # dont check for duplicates, we are editing, so just override
        # when saving, \n increase. Don't know why exactly. Just clean data
        content = content.replace('\r\n', '\n')
        content = re.sub(r'\n{3,}', '\n\n', content)  # maximum 2 new lines
        # remove new lines at the beginning and end
        content = content.strip('\n')

        util.save_entry(title, content)
        return redirect("entry", title)


def random_entry(request):
    title_list = util.list_entries()
    random_title = choice(title_list)
    return redirect("entry", random_title)
