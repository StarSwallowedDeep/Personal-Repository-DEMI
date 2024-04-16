from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import ChatOpenAI
import pyttsx3
import speech_recognition as sr
import datetime
import pywhatkit
import pyautogui
import subprocess
import webbrowser


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

# 음성 속도 조절
engine.setProperty('rate', 200)

# 사용 가능한 음성 목록 확인 후 영어 음성으로 설정
voices = engine.getProperty('voices')
desired_voice = None
for voice in voices:
    if voice.name == "Microsoft Zira Desktop - English (United States)":
        desired_voice = voice
        break
    
if desired_voice:
    engine.setProperty('voice', desired_voice.id)
else:
    print("Desired English voice not found. Using default voice.")


# 입력을 텍스트로 가져오고 오디오로 출력합니다.
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
# DEMI를 시작합니다.
def greeting():
    hour = int(datetime.datetime.now().hour)
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    if hour>=0 and hour<12:
        print(f"DEMI: Good Morning, it's {current_time}. I am DEMI sir, Please tell me how may I help you.")
        speak(f"Good Morning, it's {current_time}. I am DEMI sir, Please tell me how may I help you.")
    elif hour>=12 and hour<17:
        print(f"DEMI: Good Afternoon, it's {current_time}. I am DEMI sir, Please tell me how may I help you.")
        speak(f"Good Afternoon, it's {current_time}. I am DEMI sir, Please tell me how may I help you.")
    elif hour>=17 and hour<21:
        print(f"DEMI: Good Evening, it's {current_time}. I am DEMI sir, Please tell me how may I help you.")
        speak(f"Good Evening, it's {current_time}. I am DEMI sir, Please tell me how may I help you.")
    else:
        print(f"DEMI: Good Night, it's {current_time}. I am DEMI sir, Please tell me how may I help you.")
        speak(f"Good Night, it's {current_time}. I am DEMI sir, Please tell me how may I help you.")

# DEMI에게 명령을 수행합니다.    
def takecommand():
    r =  sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Listening....")
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Recognizing....\n")
            query = r.recognize_google(audio, language="en-in")
            print(f"You said: {query}")
            query = query.lower()
            
            if 'open' in query:
                # OpenAI를 활용합니다
                content = "open 빼고 내가 뒤에 어떤 말을 하던 사이트 주소만 답해줘: "
                chat_model = ChatOpenAI()
                result = chat_model.predict(content + query)
                              
                print(f"DEMI: Opening {result} Application sir...\n")
                speak("Opening Web Application sir...")
                webbrowser.open(result)
            
            if 'play' in query:
                query = query.replace('play','')
                print(f"DEMI: Confirm, Playing {query}\n")
                speak('Confirm, Playing' + query)
                pywhatkit.playonyt(query)
                
            if 'searching' in query:
                query = query.replace('searching','')
                print(f"DEMI: Confirm, searching {query}\n")
                speak('Confirm, searching' + query)
                pywhatkit.search(query)
                
            if 'note' in query:
                print("DEMI: Opening Note Application sir...\n")
                speak("Opening Note Application sir...")
                subprocess.Popen(['notepad.exe'])
                        
            if 'type' in query:
                query = query.replace('type','')
                print("DEMI: Writing\n")
                speak("Writing")
                pyautogui.write(query)
                
            if 'turn off' in query:
                print("DEMI: Alright. I'm Leaving Sir, BYE BYE!\n")
                speak("Alright. I'm Leaving Sir, BYE BYE!")
                engine.runAndWait()
                break
            
            else:
                # OpenAI ChatBot
                chat_model = ChatOpenAI()
                result = chat_model.predict(query)
                print(f"DEMI: {result}\n")
                speak(result)
            
        except Exception as Error:
            engine.runAndWait()
        
greeting()
takecommand()