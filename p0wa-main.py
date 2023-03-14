import openai
import speech_recognition as sr
from datetime import datetime
from ventana import ventana
from nltk.corpus import stopwords
import webbrowser
import re
import pywhatkit as kit

openai.api_key = ""

fecha_hora_actual = datetime.now()
fecha_hora_str = fecha_hora_actual.strftime("%d-%m-%Y %H:%M:%S")

contexto = "Contexto: La fecha y hora actual es: "+fecha_hora_str+"  Tu nombre ahora es pOwa, este nombre proviene de el nombre de la aplicacion ""Pocket Waifu Assistant"" y eres una asistente virtual.\n"
personaje = " \nInstrucciones: hacer uso uwu, owo,:3,(^w^)  y otros emoticones similares. Si te piden poner o reproducir una cancion debes buscar la cancion en youtube no envíes links y responde a la solicitud indicando el titulo de la cancion y el autor entre los caracteres --- y con separacion de _. Ejemplo ---louder_Roselia---, si te piden buscar la cancion mas nueva del artista solo incluye el nombre del artista en el resultado, ejemplo ---Roselia---.Solo si el mensaje del usuario dice la parabra adios o una palabra que signifique una despedida, respondes con ""chao lo`h vimo""\n"
registro= ""

def reduce_prompt(texto):
    lineas = texto.split('\n')
    if len(lineas) > 1700:
        del lineas[:10]
    return '\n'.join(lineas)



def limpiar(a, b):
    res = []
    resp = ""
    for i in b:
        i = i.strip("\n")
        #print(i)
        if i not in a:
            res.append(i)
    for i in res:
        resp = resp + " " + i
    return resp

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
        
    respuesta = openai.Completion.create(engine="text-davinci-002", prompt=prompt, n=1, max_tokens=2048)
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


f = open("stopwords.txt", "r")
stopwords = f.read()
f.close()

init()

while True:
    
    ChatIn = vozIn()
    ChatIn = ChatIn.strip("\n")
    #ChatIn = ChatIn.to__json()
    Respuesta_p0wa=consulta(ChatIn,1)
    print(Respuesta_p0wa)


    if "---"in Respuesta_p0wa:
        music = Respuesta_p0wa.split('---')[1]
        kit.playonyt(music)
        
    ventana(Respuesta_p0wa[6:])
    #speaker.Speak(Respuesta_p0wa[6:])

    registro_nuevo = "Usuario: " + ChatIn + " " + Respuesta_p0wa

    registro_nuevo= registro_nuevo.split(" ")

    #print(registro_nuevo)

    registo_sin_stopwords = limpiar(stopwords, registro_nuevo)

    registro_nuevo = registo_sin_stopwords

    #print(registro_nuevo)
    
    registro=registro+registro_nuevo

    registro=reduce_prompt(registro_nuevo)

    #print(registro)




    if "vimo" in Respuesta_p0wa:
        bye(registro)  
        break
    
    
