from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import ChatOpenAI
import pyttsx3
import speech_recognition as sr
import datetime
import pywhatkit
import pyautogui


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
            content = "너가 판단하기에 뒤에 말에 어떠한 사이트를 열어달라는 말이면 searching과 그 내용을 출력하고 \
                       뭔가 적어달라는 말이면 type과 적을 내용을 출력하고 \
                       어떤 노래를 유튜브를 통해 듣고 싶은 말이면 play와 듣고 싶은 노래 제목을 출력해줘. \
                       출력 예시로는 만약 날씨에 대한 정보를 찾으려고 한다면 searching weather를 출력하고 \
                       Hello word를 작성해줘 라고 하면 type Hello word를 출력하고 \
                       나 Celebrity 노래 듣고 싶어 라고 하면 play Celebrity를 출력해줘 : "
            chat_model = ChatOpenAI()
            result = chat_model.predict(content + query)
            
            if 'searching' in result:
                result = result.replace('searching','')
                print(f"DEMI: Confirm, searching {result}\n")
                speak('Confirm, searching' + result)
                pywhatkit.search(result)
            
            if 'play' in result:
                result = result.replace('play','')
                print(f"DEMI: Confirm, Playing {result}\n")
                speak('Confirm, Playing' + result)
                pywhatkit.playonyt(result)
                        
            if 'type' in result:
                result = result.replace('type','')
                print("DEMI: Writing\n")
                speak("Writing")
                pyautogui.write(result)
                
            if 'turn off' in query:
                print("DEMI: Alright. I'm Leaving Sir, BYE BYE!\n")
                speak("Alright. I'm Leaving Sir, BYE BYE!")
                engine.runAndWait()
                break
            
        except Exception as Error:
            engine.runAndWait()
        
greeting()
takecommand()