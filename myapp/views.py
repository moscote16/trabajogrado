from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Pruebas, Canino
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import login, logout
from .funciones import procesar
import mimetypes 
from django.core.paginator import Paginator


def error_404_view(request, exception):
    return render(request, '404.html', status=404)

def hello(request):
    return render(request,'index.html')


def registroview(request):
    if request.method=='GET':
        return render(request, 'registration/registro.html')
    else:
        if request.POST['password']==request.POST['password1']:
            try:
                user=User.objects.create_user(username=request.POST['username'],password=request.POST['password'])
                user.save()
                login(request,user)
                return redirect('login')
            except:
                return render(request, 'registration/registro.html',{
                    "error":'el usuario ya existe'
                })
                
        return  render(request, 'registration/registro.html',{
                "error":'contraseña no coinciden'
            }) 
          
        
@login_required       
def registro1(request):
    if request.method == 'POST':
        id_canino = request.POST.get('id_canino')
        nombre_canino = request.POST.get('nombre_canino')
        nombre_dueño = request.POST.get('nombre_dueño')
        dictamen = request.POST.get('Dictamen')
        cedula = request.POST.get('cedula')
        telefono = request.POST.get('telefono')
        años_canino = request.POST.get('años_canino')
        imagen = request.FILES.get('image_file')

        
        canino = Canino(
            id_canino=id_canino,
            nombre_canino=nombre_canino,
            nombre_dueño=nombre_dueño,
            dictamen=dictamen,
            cedula=cedula,
            telefono=telefono,
            años_canino=años_canino,
            imagen=imagen
        )

       
        canino.save()
        
        return redirect('prueba')  
    return render(request, 'registro1.html')
   
@login_required         
def signout (request):
    logout(request) 
    return redirect('index')   
    
@login_required
def principal(request):
    return render(request, 'principal.html')

@login_required
def listado_paciente(request):
    canino = None
    mensaje_error1 = None
    if request.method == 'GET':
        mensaje_error1 = request.GET.get('mensaje_error1', None)

    return render(request, 'listado_paciente.html', {'canino': canino, 'mensaje_error1': mensaje_error1})



@login_required
def prueba(request):
    if request.method == 'POST':
        id_canino = request.POST.get('id_canino')
        tipo_prueba = request.POST.get('tipo_prueba')
        diagnostico = int(request.POST.get('diagnostico'))
        archivo = request.FILES.get('csv_file')
        dimensiones = request.POST.get('dimensiones')
        
        try:
            canino = Canino.objects.get(id_canino=id_canino)
        except Canino.DoesNotExist:
            messages.error(request, 'El ID del canino no existe.')
            return render(request, 'prueba.html')

        if archivo:
            file_type, encoding = mimetypes.guess_type(archivo.name)
            if file_type != 'text/plain':
                messages.error(request, 'Solo se permiten archivos .txt')
                return render(request, 'prueba.html')

        prueba = Pruebas(
            canino=canino,
            tipo_prueba=tipo_prueba,
            diagnostico=diagnostico,
            archivo=archivo,
            dimensiones=dimensiones,
        )

        prueba.save()
        
        print(f'Archivo subido con ID: {prueba.id}')
        messages.success(request, 'La carga fue exitosa. ¿Quieres ingresar más datos? Por favor llena de nuevo el formulario')
        return redirect('prueba')
    return render(request, 'prueba.html')

@login_required
def loginview(request): 
    return render(request, 'registration/login.html')

@login_required
def Eliminar(request):
    if request.method == 'POST':
        id_canino = request.POST.get('id_canino')
        
        try:
            canino = Canino.objects.get(id_canino=id_canino)
            canino.delete()
            messages.success(request, 'El canino ha sido eliminado exitosamente.')
        except Canino.DoesNotExist:
            messages.error(request, 'No se encontró un canino con el ID proporcionado.')

        return redirect('Eliminar')

    return render(request, 'Eliminar.html')


@login_required
def bancodatos(request):
    if request.method == 'POST':
        tipo_prueba = request.POST.get('tipo_prueba')
        return redirect(reverse('resultadodatos') + f'?tipo_prueba={tipo_prueba}')
    return render(request, 'bancodatos.html')

@login_required
def resultadodatos(request):
    tipo_prueba = request.GET.get('tipo_prueba')
    prueba = Pruebas.objects.filter(tipo_prueba=tipo_prueba) if tipo_prueba else Pruebas.objects.all()

    return render(request, 'resultadodatos.html', {"prueba": prueba})

@login_required
def resultadospacientes(request):
    if request.method == 'POST':
        numero_id = request.POST.get('Numero_Id')
        request.session['numero_id'] = numero_id
        return redirect('resultadospacientes')

    numero_id = request.session.get('numero_id')
    if not numero_id:
        return redirect('listado_paciente')

    try:
        canino = Canino.objects.get(id_canino=numero_id)
    except Canino.DoesNotExist:
        messages.error(request, 'No se encontró un canino con el ID proporcionado.')
        return redirect(reverse('listado_paciente') + '?mensaje_error1=No se encontró un canino con el ID proporcionado.')
    pruebas_list = canino.pruebas_set.all()
    paginator = Paginator(pruebas_list, 10) 
    page_number = request.GET.get('page')
    pruebas = paginator.get_page(page_number)
    
    return render(request, 'resultadospacientes.html', {'canino': canino, 'pruebas': pruebas})

@login_required
def analisis(request):
    if request.method == 'POST':
        datos = request.POST.get('datos')
        
        if datos and datos.isdigit():
            numberOfInputs = int(datos)
            additional_inputs = [{'name': f'numero_{i}', 'placeholder': f'Número {i + 1}'} for i in range(numberOfInputs)]
            request.session['additional_inputs'] = additional_inputs
            return redirect('formulario')
        else:
            messages.error(request, 'Por favor, introduce un número válido en el campo "Datos".')
    
    return render(request, 'analisis.html')

@login_required
def formulario(request):
    additional_inputs = request.session.get('additional_inputs', [])
    
    if request.method == 'POST':
        input_values = [request.POST.get(input['name']) for input in additional_inputs]
        procesar(input_values)
        return redirect('formulario')
    return render(request, 'formulario.html', {'additional_inputs': additional_inputs})

def eliminar_prueba(request, prueba_id):
    if request.method == 'POST':
        prueba = get_object_or_404(Pruebas, id=prueba_id)
        prueba.archivo.delete()  
        prueba.delete()  
        messages.success(request, 'El archivo ha sido eliminado exitosamente.')
    
    return redirect('resultadospacientes')