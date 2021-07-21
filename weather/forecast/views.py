from django.shortcuts import render,redirect
import requests
from . models import *
from .forms import *

# Create your views here.

def index(request):
    url='{{your api key}}'
    err_msg=''
    message=''
    message_class=''

    if request.method=='POST':
        form=CityForm(request.POST)
        if form.is_valid():
            new_city=form.cleaned_data['name']
            existing_city_count=City.objects.filter(name=new_city).count()
            if existing_city_count==0:
                r=requests.get(url.format(new_city)).json()

                print(r)
                if r['cod']==200:
                    form.save()
                else:
                    err_msg="Wrong name . City does not exist"
                
            else:
                err_msg="City already exists in database"
        if err_msg:
            message=err_msg
            message_class='is-danger'
        else:
            message='City added'
            message_class='is-success'



    print(err_msg)
    form=CityForm()

    cities=City.objects.all()
    weather_data=[]
    for city in cities:
        r=requests.get(url.format(city)).json()
    

        city_weather={
        'city':city,
        'temperature':r['main']['temp'],
        'description':r['weather'][0]['description'],
        'icon':r['weather'][0]['icon']
        }
        weather_data.append(city_weather)
    print(weather_data)

    context={'weather_data':weather_data,'form':form,'message':message,'message_class':message_class}

    return render(request,"forecast/forecast.html",context)
def delete_city(request,city_name):
    City.objects.get(name=city_name).delete()

    return redirect("home")

