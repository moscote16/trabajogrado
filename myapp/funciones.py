import os
import pandas as pd
import numpy as np
from io import StringIO
from .models import Pruebas

def procesar(input_values):
    lista=[]
    procesados = set()
    print(f"Valores ingresados: {input_values}")
    for value in input_values:
        if value in procesados:
            print(f"El ID {value} ya ha sido procesado. Se omite este análisis.")
            continue
        pruebas = Pruebas.objects.filter(id=value)
        if pruebas.exists():
                print(f"Se encontraron {pruebas.count()} archivos para ID: {value}")
                procesados.add(value)
                for prueba in pruebas:
                    archivo_path = prueba.archivo.path
                    print(f"Intentando acceder al archivo: {archivo_path}")
                    if os.path.exists(archivo_path):
                        print(f"Archivo encontrado en la ruta: {archivo_path}")
                        try:
                            with open(archivo_path, 'r') as file:
                                contenido = file.read()
                                data = StringIO(contenido)
                                df = pd.read_table(data)
                                
                                if 'Unnamed: 0' in df.columns:
                                    df = df.drop('Unnamed: 0', axis=1)
                                    lista.append(df)
                                        
                                    
                                #print(df)
                                #print(f"{type(df)}")
                        except Exception as e:
                            print(f"Error al leer el archivo para ID {value}: {e}")
                    else:
                        print(f"El archivo no existe en la ruta: {archivo_path}")
        else:
                print(f"No se encontraron archivos para ID: {value}")
    
    print(len(lista))
    almacenando=np.concatenate(lista, axis=1)
    print (almacenando.shape)
    print (type(almacenando))
 
    almacenando = np.char.replace(almacenando.astype(str), ',', '.')
    if almacenando.dtype != np.float64:
        print("")
    try:
        almacenando = almacenando.astype(np.float64)
        print("")
    except Exception as e:
        print("")
    Gmax=almacenando.max(axis=0)
    Gmin=almacenando.min(axis=0)
    print("-----Gmax-----")
    print((Gmax.shape))
    print("-----Gmin-----")
    print((Gmin.shape))
    print("-----Df-----")
    DfGmaxGmin=Gmax-Gmin
    print(DfGmaxGmin.shape)
    print(DfGmaxGmin)
    num_sensores = 8
    datosDf=[]
    for i in range(0, len(DfGmaxGmin), num_sensores):
        datos_sensores = DfGmaxGmin[i:i+num_sensores]
        id_value = input_values[i // num_sensores] if (i // num_sensores) < len(input_values) else None
        pruebas_filtradas = Pruebas.objects.filter(id=id_value)
    
        for prueba_filtrada in pruebas_filtradas:
            diagnostico_valor = prueba_filtrada.diagnostico
            estado_canino = 0 if diagnostico_valor == 0 else 1
            #datos_sensores = np.append(datos_sensores, estado_canino)

            print(f"Sensores {i // num_sensores + 1} para ID {id_value}: {datos_sensores}")
            print(f"Procesando datos para el id: {prueba_filtrada.id} - Estado Canino: {estado_canino}")
        if estado_canino is not None:
            if len(datos_sensores) == num_sensores:
                datos_sensores = np.append(datos_sensores, estado_canino)  
                print(f"sensores {i // num_sensores + 1} para ID {id_value}: {datos_sensores}")       
                datosDf.append(datos_sensores)
            else:
                print(f" {num_sensores} datos de sensores {len(datos_sensores)}.")
        else:
            print(f"No se pudo determinar el estado del canino para ID {id_value}")
        #una consulta por filter pasar la lista {input_values} rrecorrer en el mismo for 
        #se va traer el campo diagnostico y lo guardo en una variable
        #crear un if para clasificar si tiene diagnostico 
        #guardar en una variable un numero ya sea que 0 sean enfermos y 1 sanos 
        #agregar un ultimo elemento a lista datos_sensores debe     quedar una lista con nueve datos
        
        #convertirlo a un numpy array
    datosDf = np.array(datosDf)    
    print(f" {type(datosDf)}")
    print("-----Datos de Sensores------")
    print(datosDf)

    
    