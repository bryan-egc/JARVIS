import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import requests
import json
import webbrowser
import os
import pywhatkit as kit
import smtplib

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

#print(voices)
engine.setProperty('voice', voices[0].id)
#print(voices[0].id)

author = "Bryan"
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('Your Email', 'Password')
    server.sendmail('Your Email', to, content)
    server.close()

def wishMe():
    hour = int (datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak(f"Buenos Días {author}")
    elif hour >= 12 and hour < 18:
        speak(f"Buenas Tardes {author}")
    else:
        speak(f"Buenas Noches {author}")
    
    speak(f"Hola {author} soy Jarvis. Por favor, dime, ¿comó puedo ayudarte?")

def takeCommend():
    '''
    take microphone input from the user and return string 
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        r.pause_threshold = 1.5
        audio = r.listen(source)
    try:
        print("Reconociendo...")
        query = r.recognize_google(audio, language='en-EN')
        print(f"Usuario dice: {query} \n")
    except Exception as e:
        print(f"Lo siento {author}, dilo de nuevo")
        return "Nada"
    return query


if __name__ == "__main__":
    #speak(f"Bienvenido {author}, soy Jarvis")
    wishMe()
    #takeCommend()
    if 1:
        query = takeCommend().lower()
        if 'wikipedia' and 'who' in query:
            speak("Buscando en Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 2)
            speak("De acuerdo a Wikipedia")
            print(results)
            speak(results)

        elif 'news' in query:
            speak("News Headlines")
            query = query.replace("news", "")
            url = "https://newsapi.org/v2/top-headlines?country=mx&apiKey=62d56a99c83940ee9f9d3882c2c4172a"
            news = requests.get(url).text
            news = json.loads(news)
            art = news['articles']
            for article in art:
                print(article['title'])
                speak(article['title'])

                print(article['description'])
                speak(article['description'])
                speak("Yendo a la siguiente noticia")
        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'search browser' in query:
            speak("¿Qué debo buscar?")
            um = takeCommend().lower()
            webbrowser.open(f"{um}")

        elif 'ip address' in query:
            ip = requests.get('http://api.ipify.org').text
            print(f"Tu IP es {ip}")
            speak(f"Tu IP es {ip}")

        elif 'open command prompt' in  query:
            os.system("start cmd")

        elif 'open excel' in  query:
            codepath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
            os.startfile(codepath)

        elif 'open visual' in  query:
            codepath = "C:\\Users\\bryan\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codepath)

        elif 'play music' in query:
            music_dir = 'C:\\Users\\bryan\\Desktop\\Projects\\JARVIS\\music'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
        
        elif 'play youtube' in query:
            speak("¿Qué deseas buscar en Youtube?")
            cm = takeCommend().lower()
            kit.playonyt(f"{cm}")

        elif 'send message' in query:
            speak("¿A quien quiere envirle un mensaje?")
            num = input("Por favor, ingresa el número: \n")
            speak("¿Qué deseas enviarle?")
            msg = takeCommend().lower()
            speak("Por favor, ingresa la hora")
            H = int(input("Ingresa la hora \n"))
            M = int(input("Ingresa los minutos \n"))
            kit.sendwhatmsg(num, msg, H, M)

        elif 'send email' in query:
            speak("¿Qué debo enviar?")
            content = takeCommend().lower()
            speak("¿A quién debo enviar el email? Ingresa la dirección de email")
            to = input("Ingresa la dirección de email: \n")
            sendEmail(to, content)