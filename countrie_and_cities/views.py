from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
from rest_framework import status
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.template.response import TemplateResponse


class IndexView(APIView):

    def get(self, request):
        country = Country.objects.all().order_by('country_title')
        city = City.objects.all().order_by('city_title')

        country_serializer = CountrySerializer(country, many=True, context={"request": request})
        city_serializer = CitySerializer(city, many=True, context={"request": request})

        # return Response({'all_countries': country_serializer.data, 'all_cities': city_serializer.data})
        return TemplateResponse(request, 'countrie_and_cities/index.html',
                                {'all_countries': country_serializer.data, 'all_cities': city_serializer.data})

    def post(self, request):
        serializer = CitySerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CityCreate(CreateView):
    model = City
    fields = ['country', 'city_title', 'city_info']

    def get_initial(self):
        initial = super(CityCreate, self).get_initial()
        initial['country'] = self.kwargs['pk']
        return initial


class CityUpdate(UpdateView):
    model = City
    fields = ['country', 'city_title', 'city_info']
    template_name = 'countrie_and_cities/city_post_form_update.html'


class CityDelete(DeleteView):
    model = City
    template_name = 'countrie_and_cities/city_post_form_delete.html'

    success_url = reverse_lazy('index')


def logout_user(request):
    logout(request)
    return redirect('index')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                return redirect('index')
            else:
                return render(request, 'countrie_and_cities/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'countrie_and_cities/login.html', {'error_message': 'Invalid login'})
    return render(request, 'countrie_and_cities/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                return redirect('index')
    context = {
        "form": form,
    }
    return render(request, 'countrie_and_cities/registration_form.html', context)
