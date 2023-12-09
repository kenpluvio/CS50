import os
from django.conf import settings
from django import forms
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse
import markdown2, random
from . import util


class NewSearchForm(forms.Form):
    SearchFor = forms.CharField(label="search")

class NewCreateForm(forms.Form):
    TextTitle = forms.CharField(label="TextTitle:")
    TextArea = forms.CharField(widget=forms.Textarea())

class NewEditForm(forms.Form):
    TextTitle = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}),label="TextTitle:")
    TextArea = forms.CharField(widget=forms.Textarea())

def index(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            # Access the cleaned data
            search_query = form.cleaned_data['SearchFor']
            if search_query in util.list_entries():
                # Redirect to another view with the cleaned data
                return redirect('encyclopedia:showMD', query=search_query)
            elif any(search_query in s for s in util.list_entries()):
                return render(request, "encyclopedia/Search_list.html", {
                    "result_list" : [s for s in util.list_entries() if search_query in s]
                })
            else:
                return render(request, "encyclopedia/RequestNotFound.html")
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": NewSearchForm()
        })

def showMD(request, name):
    # Path to your Markdown file
    # markdown_file_path = f'entries/{name}.md'

    # Read Markdown content from the file
    # with open(markdown_file_path, 'r') as file:
    #     markdown_content = file.read()
    if name == "random":
        entry_list = util.list_entries()
        random_number = random.randrange(0, len(util.list_entries()), 1)
        name = entry_list[random_number]
    markdown_content = util.get_entry(name)


    # Convert Markdown to HTML using the markdown library
    if markdown_content != None:
        html_content = markdown2.markdown(markdown_content)
        # Pass the HTML content to the template
        context = {'html_content': html_content,
                'name': name}
        return render(request, 'encyclopedia/markdown_template.html', context)
    else:
        return render(request, "encyclopedia/RequestNotFound.html")
    
def create(request):
    if request.method == "POST":
        New_md = NewCreateForm(request.POST)
        if New_md.is_valid():
            md_title = New_md.cleaned_data['TextTitle']
            if md_title in util.list_entries():
                return HttpResponse("Error: Page Exist")
            else: 
                md_content = New_md.cleaned_data['TextArea']
                # Specify the file path within MEDIA_ROOT
                file_path = os.path.join(settings.MD_ROOT, f'{md_title}.md')
                with open(file_path, "w") as file:
                    file.write(md_content)
                return redirect('encyclopedia:showMD', name=md_title)

    formField = NewCreateForm()
    return render(request, "encyclopedia/create_newPage.html", {
        "form_field" : formField
    })

def edit(request, name):
    if request.method == "POST":
        edit_result = NewEditForm(request.POST)
        if edit_result.is_valid():
            md_title = edit_result.cleaned_data['TextTitle']
            md_content = edit_result.cleaned_data['TextArea']
            util.save_entry(md_title, md_content)
            return redirect('encyclopedia:showMD', name=md_title)
    else:
        file_path = os.path.join(settings.MD_ROOT, f'{name}.md')
        try:
            with open(file_path, "r") as file:
                page_content = file.read()
        except FileNotFoundError:
            # Handle the case where the file is not found
            return HttpResponseNotFound("Page not found")
        except IOError as e:
            # Handle other file reading errors
            return HttpResponseServerError(f"Error reading the file: {e}")
        
        form = NewEditForm(initial={'TextTitle': name, 'TextArea' : page_content})
        return render(request, "encyclopedia/edit.html", {
            "title": name,
            "form_field": form
        }) 

    