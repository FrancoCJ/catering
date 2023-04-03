from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
from django.db import connection
from django.template import *
from datetime import *
from .forms import *
from .models import *
import hashlib
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
#from .forms import LoginForm
from django.contrib.auth.models import User
import time

import time
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['user_id'] = user.id
                return redirect('formulario/')
        # if authentication fails, display an error message
        messages.error(request, 'Usuario y/o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def formulari(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        if request.method == "POST":
            formulariomenu = Form1(request.POST)
            if formulariomenu.is_valid():
                info = formulariomenu.cleaned_data
                nombre = request.user.username
                if formularios.objects.filter(Nombre=nombre).exists():
                    messages.error(request, f"Ya existe pedido de comida para '{nombre}'")
                else:
                    dataformulario = formularios(
                        Nombre=nombre,
                        Lunes=info["Lunes"],
                        Martes=info["Martes"],
                        Miercoles=info["Miercoles"],
                        Jueves=info["Jueves"],
                        Viernes=info["Viernes"]
                    )
                    dataformulario.save()
                    nombre = request.user.username
                    messages.success(request, f"El formulario ha sido enviado correctamente para '{nombre}'")

        else:
           formulariomenu = Form1()
        
        # Get messages from the current session and add them to the template context
     
        return render(request, "Formulario.html", {"Formulario": formulariomenu})




@user_passes_test(lambda u: u.is_staff, login_url='/', redirect_field_name=None)

def descarga(request):
    if request.method == 'POST':
        # queries ejecutadas por cada dia y guardar los resultados en un diccionario
        queries = {
            'Lunes': 'SELECT Lunes, COUNT(*) AS count FROM myapp_formularios GROUP BY Lunes;',
            'Martes': 'SELECT Martes, COUNT(*) AS count FROM myapp_formularios GROUP BY Martes;',
            'Miercoles': 'SELECT Miercoles, COUNT(*) AS count FROM myapp_formularios GROUP BY Miercoles;',
            'Jueves': 'SELECT Jueves, COUNT(*) AS count FROM myapp_formularios GROUP BY Jueves;',
            'Viernes': 'SELECT Viernes, COUNT(*) AS count FROM myapp_formularios GROUP BY Viernes;'
        }
        results = {}
        for day, query in queries.items():
            df = pd.read_sql(query, connection)
            df['Day'] = day
            results[day] = df

        # Obtener los usuarios que no han enviado el formulario
        usernames = set(User.objects.values_list('username', flat=True))
        formularios_usernames = set(formularios.objects.values_list('Nombre', flat=True))
        falta_enviar_usernames = list(usernames - formularios_usernames)
        falta_enviar_df = pd.DataFrame(falta_enviar_usernames, columns=['username'])

        # Agrara la tabla myapp_formularios en un DataFrame
        formularios_query = 'SELECT Nombre, Lunes, Martes, Miercoles, Jueves, Viernes FROM myapp_formularios ORDER BY Nombre ASC;'
        formularios_df = pd.read_sql(formularios_query, connection)

        # Guarda los resultados
        response = HttpResponse(content_type='text/xlsx')
        response['Content-Disposition'] = 'attachment; filename=MenusElegidosSemana.xlsx'

        with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
            formularios_df.to_excel(writer, sheet_name='Elecciones Semana', index=False)
            for day, df in results.items():
                sheet_name = f'Total Menus {day}'
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            falta_enviar_df.to_excel(writer, sheet_name='Falta enviar', index=False)
            
        return response
    else:
        return render(request, 'admin/descarga.html')



@user_passes_test(lambda u: u.is_staff, login_url='/', redirect_field_name=None) 
def Delete(request):

    if request.method == "GET":

        formu = Form1(request.GET)

        if formu.is_valid:
                
                Dataformulario = formularios.objects.all()
                
                Dataformulario.delete()
               
                return redirect('/admin')
        else:
            return render(request, '/admin')
        
@user_passes_test(lambda u: u.is_staff, login_url='/', redirect_field_name=None)
def subirimagen(request):
    if request.method == 'POST':
        #Borra la imagen "OpcionesMenuSemana" ya presente
        for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            if default_storage.exists('menu_images/OpcionesMenuSemana'+ext):
                default_storage.delete('menu_images/OpcionesMenuSemana'+ext)
        
        
        image_file = request.FILES.get('image')
        if image_file is None:
            error_message = 'No se ha subido ninguna imagen'
            return render(request, '/subirimagen.html', {'error_message': error_message})
        
        #Guarda la nueva imagen subida como "OpcionesMenuSemana"
        filename = 'OpcionesMenuSemana' + ext
        path = default_storage.save('menu_images/' + filename, ContentFile(image_file.read()))
        
        
        success_message = 'Imagen subida correctamente'
        return render(request, 'subirimagen.html', {'success_message': success_message})
    else:
        return render(request, 'subirimagen.html')

@user_passes_test(lambda u: u.is_staff, login_url='/', redirect_field_name=None)
def admin(request):
    password = 'Ingreso757'
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    context = {'password_hash': password_hash}
    return render(request, 'admin.html', context)



@user_passes_test(lambda u: u.is_staff, login_url='/', redirect_field_name=None)
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            is_admin = form.cleaned_data['is_admin']
            user = User.objects.create_user(username=username, password=password)
            if is_admin:
                user.is_staff = True
            user.save()
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})





