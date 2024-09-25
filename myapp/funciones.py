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
    #toca verificar que todos los datos en la variable almacenando sea de tipo numerico y que sea double 
    Gmax=almacenando.max(axis=0)
    Gmin=almacenando.min(axis=0)
    print("-----Gmax-----")
    print((Gmax.shape))
    print("-----Gmin-----")
    print((Gmin.shape))
    print("-----GA1-----")
    #GA1=Gmax-Gmin
    #print(GA1.shape)
    #print(GA1)