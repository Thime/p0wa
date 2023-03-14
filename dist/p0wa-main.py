import openai
import win32api
import speech_recognition as sr
from datetime import datetime
import win32com.client
import tkinter as tk
import re
from PIL import ImageTk, Image

speaker = win32com.client.Dispatch("SAPI.SpVoice")


openai.api_key = "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"

fecha_hora_actual = datetime.now()
fecha_hora_str = fecha_hora_actual.strftime("%d-%m-%Y %H:%M:%S")

contexto = "Contexto: La fecha y hora actual es: "+fecha_hora_str+"  Tu nombre ahora es pOwa, este nombre proviene de el nombre de la aplicacion ""Pocket Waifu Assistant"" y eres una asistente virtual.\n"
personaje = " \nInstrucciones: hacer uso uwu, owo,:3,(^w^)  y otros emoticones similares. Solo si el mensaje del usuario dice la parabra adios o una palabra que signifique una despedida, respondes con ""chao lo`h vimo""\n"
registro= ""

# Importar la biblioteca Tkinter y la biblioteca Pillow para manejar imágenes


def ventana(texto):
    
    # Crear una ventana
    ventana = tk.Tk()

    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    ventana.geometry("300x350+{}+{}".format(screen_width-300, screen_height-350))

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
    patron = r'[.,]'
    nuevo_texto = re.sub(patron, '\\g<0>ð', texto)
    texto_dividido = nuevo_texto.split("ð")


    # Agregar una etiqueta para mostrar el texto
    etiqueta_texto = tk.Label(ventana, text=texto_dividido[0], wraplength=280,anchor="center", justify="center")
    etiqueta_texto.pack()

    # Establecer la ventana siempre encima de otras ventanas
    ventana.attributes("-topmost", True)

    ventana.overrideredirect(True)

    # Definir la función que cambia el texto
    indice_texto = 0
    def cambiar_texto(event):
        nonlocal indice_texto
        if indice_texto < len(texto_dividido) - 1:
            indice_texto += 1
            etiqueta_texto.config(text=texto_dividido[indice_texto])
        else:
            ventana.destroy()

    # Vincular el evento "Button-1" a la función "cambiar_texto"
    ventana.bind("<Button-1>", cambiar_texto)

    # Mostrar la ventana
    ventana.mainloop()


def vozIn():
    r = sr.Recognizer()
    result=""
    print("Yo: ")
    while result=="":

            with sr.Microphone() as source:

                audio = r.listen(source)
                
            try:
                result = r.recognize_google(audio, language='es-ES',show_all=False)
                
            except Exception as e:
                pass

    return result

def leerMinuta():
        
    with open("minuta.txt", "r") as minuta:
            minutaAnterior= minuta.read
    return minutaAnterior


#Envia una consulta en Str a openai. pj determina si la respuesta obtenida es dentro de personaje o no.
def consulta(consulta,pj):
    global contexto
    global personaje
    global registro

    if pj:
        prompt = contexto+"\nEsta es la conversacion que has tenido con hasta ahora con el usuario: "+registro+"\n\nFin Registro\n\n" + "Ahora responde al siguiente mensaje del usuario: "+consulta + personaje
        p0waDice="\np0wa:"

    else:
        prompt=consulta
        p0waDice=""
        
    respuesta = openai.Completion.create(engine="text-davinci-003", prompt=prompt, n=1, max_tokens=2048)
    respuestaStr=format(respuesta.choices[0].text)
    
    return p0waDice + respuestaStr[1:]
 

def init():
    saludo = "Hola, presentate"
    respuesta=consulta(saludo,1)
    print(respuesta)
    ventana(respuesta[6:])
    

#Extrae el contexto elabora una minuta y la guarda en un .txt
def bye(registro):
    global contexto
    global personaje
    
    instruccion= "Acabas de reunirte con el usuario aqui esta la transcripcion de lo que tú ,p0wa, hablaste con el. \n\n"
    instruccion2="\n Decidiste tomar nota en tu cuaderno de los aspectos importantes de la conversacion que te ayuden en tu labor de asistente para poder recordarlo en otras conversaciones, tambien anotaste la fecha. Entregame como respuesta solo lo que esta escrito en tu cuaderno.\n"

    prompt=contexto+instruccion+registro+"\n\n Fin Del Rrgistro\n\n"+instruccion2+personaje

    Resp_minuta=consulta(prompt,1)
    Resp_minuta=Resp_minuta[5:]
    with open("minuta.txt", "a") as minuta:
        minuta.write("\n\n"+Resp_minuta)

init()

while True:
    
    
    ChatIn = vozIn()
    Respuesta_p0wa=consulta(ChatIn,1)
    print(Respuesta_p0wa)
    
    #win32api.MessageBox(0,Respuesta_p0wa, "p0wa Dice:")
    ventana(Respuesta_p0wa[6:])
    #speaker.Speak(Respuesta_p0wa[6:])

    
    registro=registro+"Usuario: "+ChatIn+"\n"+Respuesta_p0wa+"\n\n"
    
    if "vimo" in Respuesta_p0wa:
        bye(registro)
        
        break

    
    
