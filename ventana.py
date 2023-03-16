import tkinter as tk
import re
from PIL import ImageTk, Image
import threading
from playsound import playsound

def reproducir_audio():
    playsound('bop.mp3')


def dividir_texto(texto):
    num = 35
    patron = r'[.,!?]'
    nuevo_texto = re.sub(patron, '\\g<0>ð', texto)
    texto_dividido1 = nuevo_texto.split("ð")
    texto_dividido2 = []

    for linea in texto_dividido1:
        if len(linea) > num:
            palabras = linea.split()
            nueva_linea = palabras[0]
            for palabra in palabras[1:]:
                if len(nueva_linea) + len(palabra) + 1 > num:
                    texto_dividido2.append(nueva_linea)
                    nueva_linea = palabra
                else:
                    nueva_linea += " " + palabra
            texto_dividido2.append(nueva_linea)
        else:
            texto_dividido2.append(linea)

    return texto_dividido2

def ventana(texto):

    # Crear una ventana
    ventana = tk.Tk()

    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    ventana.geometry("300x400+{}+{}".format(screen_width-300, screen_height-390))

    # Agregar un título a la ventana
    ventana.title("Mi aplicación")

    # Cargar la imagen
    imagen = Image.open("image.jpg")

    imagen = imagen.resize((300, 300), Image.LANCZOS)  # Cambiar tamaño de la imagen

    imagen = ImageTk.PhotoImage(imagen)

    # Agregar una etiqueta para mostrar la imagen
    etiqueta_imagen = tk.Label(ventana, image=imagen)
    etiqueta_imagen.pack()
   
    # Dividir el texto

    texto_dividido2=dividir_texto(texto)


            
    # Agregar una etiqueta para mostrar el texto
    etiqueta_texto = tk.Label(ventana, text=texto_dividido2[0], font=("Arial", 18),
                              wraplength=280,
                              anchor="center",
                              justify="center",
                              background="lightgrey",
                              relief=tk.RAISED)
    etiqueta_texto.pack()

    # Establecer la ventana siempre encima de otras ventanas
    ventana.attributes("-topmost", True)

    ventana.overrideredirect(True)

    # Definir la función que cambia el texto
    indice_texto = 0
    def cambiar_texto():
        nonlocal indice_texto
        if indice_texto < len(texto_dividido2) - 1:

            
            etiqueta_texto.config(text=texto_dividido2[indice_texto])

            
            
            if "." in texto_dividido2[indice_texto] or "!" in texto_dividido2[indice_texto] or "?" in texto_dividido2[indice_texto]:
                sep_timer=1100
                mult=10
                
            elif "," in texto_dividido2[indice_texto]:
                sep_timer=600
                mult=5

            else:
                sep_timer=600
                mult=1
            
            time = len(texto_dividido2[indice_texto])*mult+sep_timer
            
           
            # Llamar a la función cambiar_texto después de x segundos
            ventana.after(time, cambiar_texto)
            indice_texto += 1

        else:
            thread = threading.Thread(target=reproducir_audio)
            thread.start()
            ventana.destroy()

    # Llamar a la función cambiar_texto después de 2 segundos
    thread = threading.Thread(target=reproducir_audio)
    thread.start()


    time = len(texto_dividido2[0])*20+1000
    ventana.after(time, cambiar_texto)

    # Mostrar la ventana
    ventana.mainloop()


def close_window():
    root.destroy()

def get_input():
    global API
    input_text = input_entry.get()
    API=input_text
    close_window()
    

def ventana_inicio():
    global input_entry, root,API

    root = tk.Tk()
    root.title("Ventana")

    width, height = 300, 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.iconbitmap("icon.ico")
    # Agregar un widget de entrada
    input_label = tk.Label(root, text="Ingrese API:")
    input_label.pack(pady=10)
    input_entry = tk.Entry(root, width=30)
    input_entry.pack()

    # Agregar un botón para obtener la entrada y cerrar la ventana
    button = tk.Button(root, text="Aceptar", command=get_input)
    button.pack(pady=10)

    root.mainloop()

    return API

    

  
