from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.db.models import Q

import mimetypes
from rinex.models import RinexMetadata
from zipfile import ZipFile 

from .forms import CustomUserCreationForm, UploadFileForm, SearchFileForm
from .util.utils import handle_uploaded_file

def index(request):
    return render(request,'accounts/index.html')

def about(request):
    return render(request,'about.html')

def licenses(request):
    return render(request, 'licenses.html')

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sign_up.html'

@login_required
def menu(request): 
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        print("HERE")
        if form.is_valid():
            metadata = handle_uploaded_file(request.FILES['file'])
            license_selection = request.POST['licence']
            rinex_meta = RinexMetadata(min_lon=metadata['min_lon'], 
                        min_lat=metadata['min_lat'], 
                        max_lon=metadata['max_lon'], 
                        max_lat=metadata['max_lat'], 
                        receiver_info=metadata['receiver_info'],
                        antenna_info=metadata['antenna_info'],
                        start_time=metadata['start_time'],
                        finish_time=metadata['finish_time'],
                        system_info=metadata['system_info'],
                        number_sys_info=metadata['number_sys_info'],
                        dual_frequency=metadata['dual_frequency'],
                        file_rinex=file.name,
                        licence=license_selection)
            print(license_selection)
            rinex_meta.save()
            with open("uploads/"+str(rinex_meta.id)+"-"+rinex_meta.file_rinex, "wb+") as zp:
                for chunk in file.chunks(): #This line let you read the UploadFile
                    zp.write(chunk)

            rinex_meta.save()
            return HttpResponseRedirect('/menu')
        else:
            
            print("ERROR", form.__dict__)
            return render(request,'accounts/menu.html', {'form': form }) 

    else:
        form = UploadFileForm()
    return render(request,'accounts/menu.html', {'form': form }) 

@login_required
def search(request):
    if request.method == 'POST':
        result = "No results"
        form = SearchFileForm(request.POST)
        if form.is_valid():
            metadata = form.clean()
            print(metadata)
            print(request.POST)

            # longitude
            if (metadata['min_lon']!= None) :
                result = RinexMetadata.objects.filter(Q(min_lon__gte=metadata['min_lon']))
                if (metadata['max_lon']!=None): 
                    result = RinexMetadata.objects.filter(Q(min_lon__lte=metadata['max_lon']))

            elif (metadata['max_lon']!=None): 
                result = RinexMetadata.objects.filter(Q(min_lon__lte=metadata['max_lon']))

            #latitude
            if (metadata['min_lat']!= None) :
                result = RinexMetadata.objects.filter(Q(min_lon__gte=metadata['min_lat']))
                if (metadata['max_lat']!=None): 
                    result = RinexMetadata.objects.filter(Q(min_lon__lte=metadata['max_lat']))
            
            elif (metadata['max_lat']!=None): 
                    result = RinexMetadata.objects.filter(Q(min_lon__lte=metadata['max_lat']))
            
            # receiver information
            if (metadata['receiver_info'] != ''):
                result = RinexMetadata.objects.filter(receiver_info__contains=metadata['receiver_info'])

            # antenna information 
            if (metadata['antenna_info'] != ''):
                result = RinexMetadata.objects.filter(antenna_info__contains=metadata['antenna_info'])
            
            # time bound
            if (metadata['start_time'] != None):
                result = RinexMetadata.objects.filter(start_time__gte=metadata['start_time'])
                if (metadata['finish_time'] != None):
                    result = RinexMetadata.objects.filter(finish_time__lte=metadata['finish_time'])

            elif (metadata['finish_time'] != None):
                result = RinexMetadata.objects.filter(finish_time__lte=metadata['finish_time'])

            # system information
            if (metadata['system_info'] != ''):
                result = RinexMetadata.objects.filter(system_info__contains=metadata['system_info'])

            # number system information
            if (metadata['number_sys_info'] != None):
                result = RinexMetadata.objects.filter(number_sys_info=metadata['number_sys_info'])


            print(result)
        
        return render(request, 'accounts/search.html', {'result' : result, 'is_result': True if result != "No results" else False, 'is_post': True})
    else: 
        form = SearchFileForm()
        return render(request, 'accounts/search.html', {'form' : form, 'is_post': False})

@login_required
def download_file(request, id):
    try:
        file_rinex = RinexMetadata.objects.get(id=id).file_rinex
        # fill these variables with real values
        fl_path = 'uploads/'
        filename = str(id)+'-'+file_rinex
        fl = open(fl_path+filename, "rb")
        mime_type, _ = mimetypes.guess_type(fl_path+filename)
        response = HttpResponse(fl, content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response
    except FileNotFoundError:
        print("File related to id {0} not found".format(id))
        return render(request, "404.html")
    except ValueError:
        print("File related to id {0} not found".format(id))
        return render(request, "404.html")

@login_required
def uploadRinex(request): 
    ## rinex/<id> in questa pagina carico uno zip file poi su questo faccio tutte le operazioni necessarie
    return render(request,'accounts/upload.html')