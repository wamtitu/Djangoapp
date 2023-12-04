from hashlib import new
from pathlib import Path
import mimetypes

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .azure_file_controller import ALLOWED_EXTENTIONS, download_blob, upload_file_to_blob
from .models import CreateUserFrom
from . import models
from azure.cosmos import CosmosClient
from django.conf import settings
import uuid


def index(request):
    return render(request, "files/index.html", {})

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        ext = Path(file.name).suffix
        new_file = upload_file_to_blob(file)
        if not new_file:
            messages.warning(request, f"{ext} not allowed only accept {', '.join(ext for ext in ALLOWED_EXTENTIONS)} ")
            return render(request, "files/upload_file.html", {}) 
        
          # Store metadata in Azure Cosmos DB
        cosmos_client = CosmosClient(
            settings.COSMOSDB['ENDPOINT'], settings.COSMOSDB['PRIMARY_KEY']
        )
        database = cosmos_client.get_database_client(
            settings.COSMOSDB['DATABASE_NAME']
        )
        container = database.get_container_client(
            settings.COSMOSDB['CONTAINER_NAME']
        )
        new_file.file_name = file.name
        new_file.fileType = ext
        new_file.save()

        metadata = {
             'id': str(uuid.uuid4()),
            'file_name': file.name,
            'fileType': ext,
            'file_url': new_file.file_url,
        }
        container.upsert_item(metadata)
        messages.success(request, f"{file.name} was successfully uploaded")
        return render(request, "files/upload_file.html", {}) 

    return render(request, "files/upload_file.html", {})

def list_files(request):
    files = models.File.objects.filter(deleted=0)
    context = {"files": files}
    return render(request, "files/list_files.html", context=context)

def registerpage(request):
    form = CreateUserFrom()

    if request.method == 'POST':
        form = CreateUserFrom(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'registration successfull')
            return redirect('login')
        else:
            messages.info(request, 'username or password is incorrect')
    context = {'form':form}
    return render(request, "files/register.html", context)

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'username or password is incorrect')
    context = {}
    return render(request, "files/login.html", context)

def download_file(request, file_id):
    file = models.File.objects.get(pk=file_id)
    file_name = file.file_name
    file_type, _ = mimetypes.guess_type(file_name)
    url = file.file_url
    blob_name = url.split("/")[-1]
    blob_content = download_blob(blob_name)
    if blob_content:
        response = HttpResponse(blob_content.readall(), content_type=file_type)
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        messages.success(request, f"{file_name} was successfully downloaded")
        return response
    return Http404


def delete_file(request,file_id):
    file = models.File.objects.get(pk=file_id)
    file.deleted = 1
    file.save()
    return redirect("list_files")