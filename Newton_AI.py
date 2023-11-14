import pyttsx3
import pyjokes 
import speech_recognition as sr
import datetime
import time
import wikipedia
import webbrowser
import os
import smtplib
import pyautogui
import requests
import random
import openai

username = os.getenv('USERNAME') or os.getenv('USER')


if os.path.isfile('email_config.txt'):
    with open('email_config.txt', 'r') as config_file:
        email, password = config_file.read().strip().split('\n')
else:
    email = input("Enter your email address: ")
    password = input("Enter your email password: ")
    with open('email_config.txt', 'w') as config_file:
        config_file.write(f"{email}\n{password}")

file_path = "api_key_openweathermap.txt"
try:
    with open(file_path, 'r') as file:
        api_key_open = file.read().strip()
except FileNotFoundError:
    api_key_open = input("Enter your API key for openweathermap : ")
    with open(file_path, 'w') as file:
        file.write(api_key_open)

print(f"Using API key: {api_key_open}")



file_path = "api_key_gpt.txt"
try:
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
except FileNotFoundError:
    api_key = input("Enter your API key ChatGPT : ")
    with open(file_path, 'w') as file:
        file.write(api_key)

print(f"Using API key: {api_key}")

file_path = "your_city.txt"
try:
    with open(file_path, 'r') as file:
        city = file.read().strip()
except FileNotFoundError:
    city = input("Enter your city : ")
    with open(file_path, 'w') as file:
        file.write(city)

print(f"Setting your city to : {city}")


openai.api_key = api_key
model_engine= "text-davinci-003"



engine = pyttsx3.init('sapi5') 
voices = engine.getProperty('voices')
rate = engine.getProperty('rate')
engine.setProperty("rate",150)
engine.setProperty('voice', voices[0].id)

def chat_gpt(query):
    completion = openai.Completion.create(
    engine= model_engine,
    prompt= query,
    max_tokens=1024,
    n=1,
    stop= None,
    temperature = 0.5
    ) 
    response =completion.choices[0].text
    return response

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning! sir")

    elif hour>=12 and hour<18:
        speak("Good Afternoon! sir")

    else:
        speak("Good Evening! sir")

    speak('how can i help you')




    
def takeCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold=1500
        audio = r.listen(source)


    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in') 
        print(f"User said: {query}\n")

    except Exception as e:  
        print("Say that again please...")
        return "None"
    return query






def sendEmail(to, content):


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email, password)
    server.sendmail(email, to, content)
    server.close()


def weather_for_cast():
    complete_api_link = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key_open}"
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()
    temp_city = ((api_data['main']['temp']) - 273.15)
    weather_desc = api_data['weather'][0]['description']
    hmdt = api_data['main']['humidity']
    wind_spd = api_data['wind']['speed']

    speak("Current temperature is: {:.2f} degree Celcius".format(temp_city))
    speak("Current weather description  :{}".format(weather_desc))
    speak("Current Humidity      :{} %".format(hmdt))
    speak("Current wind speed    :{:.2f} kilometer per hour".format(wind_spd))
def wind_speed():
    complete_api_link = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key_open}"
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()
    wind_spd = api_data['wind']['speed']
    speak("Current wind speed    :{:.2f} kilometer per hour".format(wind_spd))
def temp_present():
    complete_api_link = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key_open}"
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()
    temp_city = ((api_data['main']['temp']) - 273.15)
    speak("Current temperature is: {:.2f} degree Celcius".format(temp_city))
def humidity_level():
    complete_api_link = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key_open}"
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()
    hmdt = api_data['main']['humidity']
    speak("Current Humidity      :{:.2f} %".format(hmdt))

def respond_commands():
    while True:
        query = takeCommand().lower()
        if 'wikipedia' in query:
            try:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                print(e)
                speak("Sorry Boss The Name you said i didn't found on wikipedia..please tell some other name")


        elif 'open youtube' in query:
            webbrowser.open("www.youtube.com")
            speak('opening youtube')

        elif 'open google' in query:
            webbrowser.open("www.google.com")
            speak('opening google')


        elif "search" in query and "about" in query:
            x = query.split()
            a = ''
            for i in x:
                if i == "search" or i == "about":
                    c = x.index(i)
            y = len(x) - c - 1
            for z in range(y):
                c = c + 1
                a = a + ' ' + (x[c])
            ab = a.strip()
            webbrowser.open("http://google.com/?#q=" + ab)
            

        elif 'type what i am saying' in query:
            speak("what i need to type sir")

            def typing_command():

                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Listening...")
                    r.pause_threshold = 1
                    r.energy_threshold = 1500
                    audio = r.listen(source)

                try:
                    print("Recognizing...")
                    query = r.recognize_google(audio, language='en-in')
                    print(f"User said: {query}\n")

                except Exception as e:
                    print("Say that again please...")
                    return "None"
                return query

            while True:
                typing_message = typing_command().lower()
                typing_message = typing_message.replace("type","")
                if typing_message == "done":
                    respond_commands()
                if typing_message == "enter" or typing_message == "press enter":
                    pyautogui.press("enter")
                    break
                for i in typing_message:
                    pyautogui.press(i)



        elif 'open stackoverflow' in query:
            webbrowser.open("www.stackoverflow.com")
            speak('opening stackoverflow')

        elif 'tell me a joke' in query:
            speak(pyjokes.get_joke(language="en", category="neutral") )
            


        elif 'play music' in query:
            try:

                music_dir = 'Music_'
                songs = os.listdir(music_dir)
                print(songs)
                os.startfile(os.path.join(music_dir, songs[0]))
                speak('playing songs')
            except:
                speak("No song found")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open visual studio' in query:
            codePath = f"C:\\Users\\{username}\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)
            speak('opening visual studio')

        elif 'open python interpreter' in query:
            codePath = f"C:\\Users\\{username}\\AppData\\Local\\Programs\\Python\\Python39\\python.exe"
            os.startfile(codePath)
            speak('opening python interpreter')

        elif 'open whatsapp' in query:
            codePath = f"C:\\Users\\{username}\\AppData\\Local\\WhatsApp\\WhatsApp.exe"
            os.startfile(codePath)
            speak('opening whatsapp')

        elif 'open notepad' in query:
            codePath = "C:\\Windows\\notepad.exe"
            os.startfile(codePath)
            speak('opening notepad')

        elif 'open cmd' in query:
            speak('opening cmd')
            pyautogui.keyDown("win")
            pyautogui.press("r")
            pyautogui.keyUp("win")
            pyautogui.press("c")
            pyautogui.press("m")
            pyautogui.press("d")
            pyautogui.press("enter")



        elif ("weather of"in query) or ("weather in" in query):
            try:
                word = query.split("weather of")
                a = word[1].split()[0].strip()
                
            except IndexError:
                pass
            a=a
            complete_api_link = f"https://api.openweathermap.org/data/2.5/weather?q=" + a + f"&appid={api_key_open}"
            api_link = requests.get(complete_api_link)
            api_data = api_link.json()
            temp_city = ((api_data['main']['temp']) - 273.15)
            weather_desc = api_data['weather'][0]['description']
            hmdt = api_data['main']['humidity']
            wind_spd = api_data['wind']['speed']

            speak("Current temperature is: {:.2f} degree Celcius".format(temp_city))
            speak("Current weather description  :{}".format(weather_desc))
            speak("Current Humidity      :{} %".format(hmdt))
            speak("Current wind speed    :{:.2f} kilometer per hour".format(wind_spd))
            
            

        elif 'hello' in query or 'hi' in query:
            speak('hello sir! how can i help you ')



        elif 'exit newton' in query:
            speak('ok sir ')
            exit()



        elif 'email to person' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "his or her email"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry Boss . I am not able to send this email...")



        elif 'newton' in query and 'sleep' in query:
            speak('OK Sir I m going to sleep ')
            response_newton()



        elif 'thank you' in query:
            speak('No Problem sir')



        elif 'switch window' in query:
            speak('switching tab sir')
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            pyautogui.keyUp("alt")



        elif 'take' and 'screenshot' in query:
            x=random.randint(0,99999999999999)
            filename = "my_screenshot"+ str(time.ctime()) + str(x)+".png"
            im1 = pyautogui.screenshot()
            im1.save(filename)
            speak("screenshot saved")



        elif 'close' and 'program' in query:
            speak('closing app sir')
            pyautogui.keyDown("alt")
            pyautogui.press("f4")
            pyautogui.keyUp("alt")
            pyautogui.press("enter")
            



        elif 'weather outside' in query:
            weather_for_cast()



        elif "close the computer" in query:
            pyautogui.keyDown("win")
            pyautogui.press("r")
            pyautogui.keyUp("win")
            pyautogui.press("c")
            pyautogui.press("m")
            pyautogui.press("d")
            pyautogui.press("enter")
            time.sleep(3)
            pyautogui.press("s")
            pyautogui.press("h")
            pyautogui.press("u")
            pyautogui.press("t")
            pyautogui.press("d")
            pyautogui.press("o")
            pyautogui.press("w")
            pyautogui.press("n")
            pyautogui.press("space")
            pyautogui.press("/")
            pyautogui.press("s")
            pyautogui.press("enter")



        elif "restart the computer" in query:
            pyautogui.keyDown("win")
            pyautogui.press("r")
            pyautogui.keyUp("win")
            pyautogui.press("c")
            pyautogui.press("m")
            pyautogui.press("d")
            pyautogui.press("enter")
            time.sleep(1)
            pyautogui.press("s")
            pyautogui.press("h")
            pyautogui.press("u")
            pyautogui.press("t")
            pyautogui.press("d")
            pyautogui.press("o")
            pyautogui.press("w")
            pyautogui.press("n")
            pyautogui.press("space")
            pyautogui.press("/")
            pyautogui.press("r")
            pyautogui.press("enter")

        elif "lock the pc" in query:
            pyautogui.keyDown("win")
            pyautogui.press("r")
            pyautogui.keyUp("win")
            pyautogui.press("c")
            pyautogui.press("m")
            pyautogui.press("d")
            pyautogui.press("enter")
            time.sleep(1)
            pyautogui.press("s")
            pyautogui.press("h")
            pyautogui.press("u")
            pyautogui.press("t")
            pyautogui.press("d")
            pyautogui.press("o")
            pyautogui.press("w")
            pyautogui.press("n")

            pyautogui.press("space")
            pyautogui.press("/")
            pyautogui.press("l")
            pyautogui.press("enter")




        elif 'wind speed' in query:
            wind_speed()



        elif 'temperature' in query:
            temp_present()



        elif 'humidity level' in query:
            humidity_level()



        elif 'minimize' in query or 'minimise' in query:
            pyautogui.keyDown("win")
            pyautogui.press("m")
            pyautogui.keyUp("win")



        elif 'to go' in query:
            complete_api_link = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key_open}"
            api_link = requests.get(complete_api_link)
            api_data = api_link.json()
            temp_city = ((api_data['main']['temp']) - 273.15)
            speak("Current temperature is: {:.2f} degree Celcius".format(temp_city))
            temp_comparison = "{:.2f}".format(temp_city)

            if float(temp_comparison) <= float(28) and float(temp_comparison) >= float(22):
                speak("it's slightly cold out side sir ")

            elif float(temp_comparison) <= float(23) and float(temp_comparison) >= float(15):
                speak(" weather outside is cold sir..you can take something to wear")

            elif float(temp_comparison) >= float(29) and float(temp_comparison) <= float(30):
                 speak("weather is normal sir")

            elif float(temp_comparison) >= float(31) and float(temp_comparison) <= float(40):
                speak("it's hot outside sir")


        else:
            if 'newton' in query:
                query = query.replace("newton","")
                the_gpt=chat_gpt(query)
                speak(the_gpt)
                print("The reply : "+the_gpt)
            else:
                pass

        

def response_newton():
    while True:
        query = takeCommand().lower()
        if query == 'newton':
            speak("yes sir")

            respond_commands()
        elif 'wake up' in query:
            wishMe()
            respond_commands()

        elif 'sleeping' and 'till now' in query:
            speak('sir i am always active and fresh')
            wishMe()
            respond_commands()

        elif 'close' in query or 'exit' in query:
            speak('ok sir ')
            exit()

        elif 'good morning newton' in query:
            speak("good morning sir")
            weather_for_cast()
            respond_commands()

        elif 'hello newton' in query:
            speak("hello sir! how can i help you")
            respond_commands()



if __name__ == "__main__":
    response_newton()





