from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.db.models import Q

from rinex.models import RinexMetadata
from zipfile import ZipFile 

from .forms import CustomUserCreationForm, UploadFileForm, SearchFileForm
from .util.utils import handle_uploaded_file

def index(request):
    return render(request,'accounts/index.html')

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sign_up.html'

@login_required
def menu(request): 
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = request.FILES['file']
        if form.is_valid():
            metadata = handle_uploaded_file(request.FILES['file'])
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
                        file_rinex=file.name)
            
            with open("uploads/"+file.name, "wb+") as zp:
                for chunk in file.chunks(): #This line let you read the UploadFile
                    zp.write(chunk)

            rinex_meta.save()
            return HttpResponseRedirect('/menu')
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
def uploadRinex(request): 
    ## rinex/<id> in questa pagina carico uno zip file poi su questo faccio tutte le operazioni necessarie
    return render(request,'accounts/upload.html')