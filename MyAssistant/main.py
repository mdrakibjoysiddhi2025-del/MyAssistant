import eel
import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import wikipedia
import pyjokes
import time
import pyautogui
import random
import requests
import screen_brightness_control as scr
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

# pycaw এর জন্য (Volume Control)
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

eel.init('web')

# ================== টক ফাংশন ==================
@eel.expose
def talk(text):
    try:
        alexa = pyttsx3.init()
        voices = alexa.getProperty('voices')
        alexa.setProperty('voice', voices[0].id)
        alexa.setProperty('rate', 160)
        alexa.say(text)
        alexa.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")
    return text

# ================== কমান্ড প্রসেসিং ==================
@eel.expose
def process_command(command):
    command = command.lower().strip()
    response = "Sorry, I didn't understand that."

    try:
        # টাইম
        if 'time' in command:
            current_time = datetime.datetime.now().strftime('%I:%M:%S %p')
            response = f"Current time is {current_time}"

        # প্লে গান
        elif 'play' in command:
            song = command.replace('play', '').strip()
            response = f"Playing {song}"
            pywhatkit.playonyt(song)

        
# === নতুন যুক্ত করা কিবোর্ড আপ/ডাউন কমান্ড ===
        elif any(word in command for word in ['up', 'u p']):
            response = "Pressing up key"
            pyautogui.press('pageup') # 'up' এর বদলে 'pageup' ব্যবহার করা ভালো

        elif any(word in command for word in ['down', 'dwn', 'dawn', 'done']):
            response = "Pressing down key"
            # প্রথমে যেখানে মাউস আছে সেখানে একটি ক্লিক করে উইন্ডো ফোকাস করে নেবে
            pyautogui.click() 
            time.sleep(0.1)
            # 'down' কী-র বদলে 'pagedown' বা মাউস স্ক্রল ব্যবহার করুন
            pyautogui.scroll(-800) # -৮০০ দিলে নিচের দিকে স্ক্রল হবে


        # উইকিপিডিয়া
        elif 'about' in command:
            lookfor = command.replace('about', '').strip()
            lookfor = lookfor.replace('\\', '')
            if lookfor:
                try:
                    info = wikipedia.summary(lookfor, sentences=2)
                    response = info
                except:
                    response = f"Sorry, I could not find anything about {lookfor}"
            else:
                response = "Please tell me what you want to know about."

        # জোকস
        elif 'joke' in command:
            response = pyjokes.get_joke()

        # আরদিন সম্পর্কে
        elif any(word in command for word in ['how are din' , 'how aredin' , 'ardin']):
            response = "ওর নাম মোন্তাসির ভূঁইয়া আরদিন। 🧒 ওর বয়স এখন মাত্র ৪ বছর এবং সে প্লে-গ্রুপে পড়ছে। 📚 ওর বাবার নাম সবুজ ভূঁইয়া এবং মায়ের নাম রুমি আক্তার। 👪 সম্পর্কে ও আমার বস রাকিব ভাইয়ের ছোট মামাতো ভাই। 👦🏻 ছেলেটা দেখতে যেমন কিউট, স্বভাবগতভাবে ঠিক তেমনই চঞ্চল! 🏃‍♂️💨 সারাক্ষণ ওর দুষ্টুমি আর ছোটাছুটিতে ঘর মেতে থাকে। ✨"
            print(response)
            talk("His name is Montasir Bhuiyan Ardin. He is 4 years old and studies in Playgroup. His mother's name is Mst. Rumi Akter, and his father's name is Sabuj Bhuiyan. He is the younger maternal cousin of my boss, Rakib. He is very restless and energetic by nature.")

        # আরফান সম্পর্কে
        elif any(word in command for word in ['how are fun' , 'how are fan' , 'how arefan' , 'irfan']):
            response = "ওর পুরো নাম মুরসালিন ভূঁইয়া আরফান। 👦 বর্তমানে ও ২০২০ সালে জম্ম গ্রহন করেন এবং সে নার্সারিতে পড়ছে। 📚 ওর বাবা সবুজ ভূঁইয়া এবং মা রুমি আক্তার। 👪 ওরা দুই ভাই (মোন্তাসির ও মুরসালিন)। সম্পর্কে ও আমার বস রাকিব ভাইয়ের মামাতো ভাই। 🤝 ছেলেটা স্বভাবগতভাবে বেশ সরল ও শান্ত প্রকৃতির। ✨"
            print(response)
            talk("His full name is Mursalin Bhuiyan Arfan. He is currently 6 years old and studies in Nursery. His father is Sabuj Bhuiyan and his mother is Mst. Rumi Akter. They are two brothers. He is also the maternal cousin of my boss, Rakib Bhai. By nature, he is very simple and calm.")

        # আরাফ সম্পর্কে
        elif any(word in command for word in ['araf' , 'ara' , 'how ara' , 'how araf']):
            response = "আমাদের সবার প্রিয় এই ছোট্ট মিষ্টি ছেলেটির নাম মো: আরাফ ভূঁইয়া। 👶✨ মাত্র ২ বছর বয়সেই সে পুরো ঘর মাতিয়ে রাখে!\n সে তার বাবা মামুন ভূঁইয়া এবং মা মোছা: সেপা আক্তার দম্পতির একমাত্র নয়নমণি। তাদের ভালোবাসার পুরোটা জুড়েই রয়েছে ছোট্ট আরাফ। ❤️ \n আরাফ আমার শ্রদ্ধেয় বস রাকিব ভাইয়ের ছোট মামাতো ভাই। 🤝 \n আরাফ বেশ চঞ্চল প্রকৃতির এবং সবসময় হাসিখুশি থাকতে পছন্দ করে। তার এই চপলতা যে কারো মন ভালো করে দেওয়ার জন্য যথেষ্ট! 🏃‍♂️💨"
            print(response)
            talk("The name of our beloved and sweet little boy is Md. Araf Bhuiyan. At only 2 years old, he fills the entire house with life and joy. He is the only child of Mamun Bhuiyan and Mst. Sepa Akter. Little Araf is the center of his parents' world and the apple of their eyes. Araf is the younger maternal cousin of my respected boss, Rakib. Araf is quite energetic and lively by nature. He loves to stay cheerful at all times, and his playful spirit is enough to brighten anyone's mood.")

        # মায়ান সম্পর্কে
        elif any(word in command for word in ['mayan' , 'mayn' , 'may', 'how mayan']):
            response = "আমাদের সবার প্রিয় এই মিষ্টি ছেলেটির নাম মো: মায়ান ভূঁইয়া। মাত্র ১ বছর বয়সেই ওর হাসিখুশি আর চঞ্চলতায় পুরো ঘর সবসময় মুখরিত থাকে। 🏠🌟 \n মায়ান তার বাবা মুকলেস ভূঁইয়া ও মা মোছা: তানিয়া আক্তার দম্পতির একমাত্র নয়নমণি। 💖 \n সে আমার শ্রদ্ধেয় বস রাকিব ভাইয়ের ছোট মামাতো ভাই। 🤝 \n মায়ান দেখতে মাশাল্লাহ বেশ গোলগাল (হালকা মোটা) এবং ভীষণ চটপটে। সারাক্ষণ ওর অমায়িক হাসি যে কারো মন ভালো করে দেওয়ার জন্য যথেষ্ট! 😍"
            print(response)
            talk("Our beloved and sweet boy is named Md. Mayan Bhuiyan. At just 1 year old, his cheerful and lively nature keeps the entire house vibrant and full of joy. Mayan is the only child and the apple of the eye of his parents, Mokhles Bhuiyan and Mst. Tania Akter. He is the younger maternal cousin of my respected boss, Rakib. By the grace of God (Mashallah), Mayan is quite healthy and chubby with an active personality. His constant, charming smile is enough to brighten anyone's mood!")

        # আবুহুরাইরা সম্পর্কে
        elif any(word in command for word in ['how abu', 'abo', 'hau aboho', 'hau abohorayra']):
            response = "আমাদের সবার প্রিয় আবুহুরাইরা একজন বিনয়ী মাদরাসা ছাত্র। 📖🌙 ২০১৬ সালে জন্ম নেওয়া এই মেধাবী শিশুটি তার পরিবারের সকলের চোখের মণি। \n তার বাবা মো: মোশাররফ পেশায় একজন চিকিৎসক, যিনি মানুষের সেবায় নিয়োজিত। আবুহুরাইরা তার বাবা-মায়ের আদরের ১ ভাই ও ২ বোনের মধ্যে অন্যতম। 💖👨‍👩‍👧‍ \n একজন মাদরাসা ছাত্র হিসেবে সে ধর্মীয় শিক্ষায় নিজেকে গড়ে তুলছে। তার সুন্দর ভবিষ্যৎ এবং সুস্থতার জন্য দোয়া রইল। 🤲✨"
            print(response)
            talk("Our beloved Abu Huraira is a polite and disciplined Madrasa student. Born in 2016, this talented child is the apple of his family's eye. His father, Md. Mosharraf, is a physician by profession, dedicated to serving people. Abu Huraira is one of the three children of his parents, having one brother and two sisters. As a Madrasa student, he is nurturing himself through religious education. We offer our best wishes and prayers for his bright future and good health.")

        # তাহমিদ সম্পর্কে
        elif any(word in command for word in ['how ta' , 'how tha' , 'how tamil' , 'hoh tamid']):
            response = "তাহমিদ ২০১৩ সালে এশিয়া মহাদেশের সবচেয়ে বড় গ্রাম বানিয়াচংয়ে জন্মগ্রহণ করে।"
            print(response)
            talk("Tahmid was born in 2013 in Baniyachung, the largest village in Asia.")

        # জাকিরোল সম্পর্কে
        elif any(word in command for word in ['how zakir ul', 'zakir ul', 'ul', 'zakir']):
            response = "জাকিরোল ২০০৯ সালে হবিগঞ্জের একটি গ্রামে জন্মগ্রহণ করে।"
            print(response)
            talk("Zakirol was born in 2009 in a village in Habiganj.")

        # আবুহানিফ সম্পর্কে
        elif any(word in command for word in ['how hanif', 'how hani', 'hanif', 'hani']):
            response = "মো: আবুহানিফ। তিনি ইটনা থানার জয়সিদ্ধি গ্রামে জন্মগ্রহণ করেন।"
            print(response)
            talk("Md. Abu Hanif. He was born in Joysiddhi village.")

        # সাকিব সম্পর্কে
        elif any(word in command for word in ['shakib' , 'sha kib' , 'how sakib' , 'how ski' , 'saki' , 'sha', 'sucky']):
            response = "সাকিব, যার পুরো নাম মোহাম্মদ সাকিব মিয়া।"
            print(response)
            talk("Mohammad Sakib Mia was born in 2010 in the historic village of Joysiddhi.")

        # রিফাত সম্পর্কে
        elif any(word in command for word in ['how rif' , 'how rifa' , 'how rifat' , 'rifat' ,'how ri']):
            response = "তার পুরো নাম মোহাম্মদ রিফাত। সে ২০১১ সালে জন্মগ্রহণ করে।"
            print(response)
            talk("His full name is Mohammad Rifat. He was born in 2011.")

        # অনিক সম্পর্কে
        elif any(word in command for word in ['how anik' , 'how anic' , 'anik' , 'anic' , 'onik' , 'how onik' , 'oni' , 'how oni' ,'how many']):
            response = "তার নাম মোঃ অনিক হুসেন। সে জয়সিদ্ধি গ্রামে জন্মগ্রহণ করে।"
            print(response)
            talk("His name is Md. Anik Hosen. He was born in Joysiddhi village.")

        # অর্ণব সম্পর্কে
        elif any(word in command for word in ['how arnob' , 'how arno' , 'how aro' , 'how ornod' , 'arnab' , 'arn', 'how or no']):
            response = "তার নাম অর্ণব রায়। সে ২০১২ সালে জন্মগ্রহণ করে।"
            print(response)
            talk("His name is Arnab Ray. He was born in 2012.")

        # গৌরব সম্পর্কে
        elif any(word in command for word in ['gaurav', 'gau', 'haw gaurav', 'how rav' , 'nod' , 'how gau' , 'go rob']):
            response = "তার নাম গৌরব রায়। সে ২০১২ সালে জন্মগ্রহণ করে।"
            print(response)
            talk("His name is Gaurav Ray. He was born in 2012.")

        # সিয়াম সম্পর্কে
        elif any(word in command for word in [' how siam', 'siam', 'how sia' , 'how cm' , 'halcyon']):
            response = "তার পুরো নাম মোহাম্মদ সিয়াম আব্দুল্লাহ।"
            print(response)
            talk("His full name is Mohammad Siam Abdullah.")

        # নিপা সম্পর্কে
        elif any(word in command for word in ['nipa' , 'nepa' , 'how nipa' , 'how nepa' , 'nepali' ]):
            response = "উনার পুরো নাম মোছা: নিপা আক্তার। ২০০৭ সালে জন্মগ্রহণ করেন।"
            print(response)
            talk("Her full name is Mst. Nipa Akter. She was born in 2007.")

        # আরিফ মামা সম্পর্কে
        elif any(word in command for word in ['arif mama' , 'arif' , 'how arif mama']):
            response = "তিনি কিশোরগঞ্জের ঐতিহ্যবাহী জয়সিদ্ধি গ্রামে জন্মগ্রহণ করেন।"
            print(response)
            talk("He was born in the traditional village of Joysiddhi, located in Kishoreganj.")

        # আকরাম মামা সম্পর্কে
        elif any(word in command for word in ['akram mama' , 'akra' , 'akra mama' , 'acram']):
            response = "তার পুরো নাম মো : আকরাম ভূঁইয়া।"
            print(response)
            talk("His name is Md. Akram Bhuiyan.")

        # বসের কাজ
        elif any(word in command for word in ['what do you do' , 'what do u do']):
            response = "আমার প্রিয় বস রাকিব ভাই বর্তমানে ভীষণ ব্যস্ত, তবুও তিনি তার স্কুলের জন্য ওয়েবসাইট তৈরি করছেন। তিনি মাত্র ১৩ বছর বয়সে আমাকে তৈরি করেছেন!"
            print(response)
            talk("My dear boss, Rakib Bhai, created me when he was just 13 years old!")

        # বটের নাম
        elif any(word in command for word in ['what is your name' , 'your name' , 'is your name']):
            response = "আমার নাম এলএক্সা 😎😎"
            print(response)
            talk("my name is alxca")

        # বসের নাম
        elif any(word in command for word in ['what is your boss name' , 'your boss name' , 'is your boss name' , 'whoat is your boss name' , 'what is your boss']):
            response = "আমাকে জিনি বানিয়েছেন বা আমার বস এর নাম রাকিব ??🙂🙂"
            print(response)
            talk("my boss name is rakib")
        
        # কে তৈরি করেছে
        elif any(word in command for word in ['made you' , 'mad you' , 'how made you']):
            response = "আমার বসের নাম রাকিব। তিনি বর্তমানে অষ্টম শ্রেণিতে পড়াশোনা করছেন। ২০১২ সালে শিবপাশায় তার জন্ম। বর্তমানে তিনি তার মামার বাড়িতে থেকে পড়াশোনা চালিয়ে যাচ্ছেন। 📚✨\n আপনারা জেনে খুশি হবেন যে, আমাকে তৈরি করতে তিনি পাইথন (Python) প্রোগ্রামিং ভাষা ব্যবহার করেছেন। আমি আশা করি, ভবিষ্যতে তিনি আমাকে আরও উন্নত ও দক্ষ করে তুলবেন। 💻🤖\n তিনি ব্যক্তিগত জীবনে ইসলাম ধর্মের অনুসারী। আপনারা সবাই আমার বসের জন্য দোয়া করবেন, যেন তিনি জীবনে অনেক বড় হতে পারেন এবং তার লক্ষ্য পূরণ করতে পারেন। 🤲 আমিন। ❤️"
            print(response)
            talk("My boss's name is Rakib. He is currently a student in Grade 8. He was born in 2012 in Shibpasha. At present, he is continuing his studies while staying at his maternal uncle's house. You will be happy to know that he used the Python programming language to create me. I hope that in the future, he will make me even more advanced and efficient. In his personal life, he is a follower of Islam. Please pray for my boss so that he can achieve greatness in life and fulfill his goals. Amin.")

        


        #
        
        
        
        
        # ওয়েদার
        elif 'weather' in command:
            city = command.replace('weather', '').strip() or 'dhaka'
            api_key = '003fd2899f360beff4cb215d34f698f1'
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            try:
                res = requests.get(url)
                data = res.json()
                temp = data['main']['temp']
                desc = data['weather'][0]['description']
                response = f"The temperature in {city} is {temp}°C with {desc}"
            except:
                response = "Sorry, I could not find the weather."

        # ভলিউম
        elif 'volume' in command:
            lvl = [int(s) for s in command.split() if s.isdigit()]
            if lvl:
                v_level = min(max(lvl[0] / 100, 0), 1)
                devices = AudioUtilities.GetDeviceEnumerator()
                interface = devices.GetDefaultAudioEndpoint(0, 0)
                volume_interface = interface.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(volume_interface, POINTER(IAudioEndpointVolume))
                volume.SetMasterVolumeLevelScalar(v_level, None)
                response = f"Volume set to {lvl[0]} percent"
            else:
                response = "Please tell me the volume level"

        # স্ক্রিনশট
        elif 'screenshot' in command:
            screenshot = pyautogui.screenshot()
            screenshot.save(r'C:\Users\MD RAKIB MIA\PycharmProjects\PythonProject rakib\pycharm2\my_screenshot.png')
            response = "Screenshot saved successfully!"

        # বিদায়
        elif 'goodbye' in command or 'bye' in command:
            response = "Goodbye! Take care! ❤️"
            eel.show_response(response)
            talk(response)
            eel.close_window()
            return response

        else:
            response = "I am listening... Tell me more."

    except Exception as e:
        print(f"Error occurred: {e}")
        response = "Something went wrong."

    eel.show_response(response)
    talk(response)
    return response

# ================== লিসেন ফাংশন ==================
@eel.expose
def listen():
    try:
        listener = sr.Recognizer()
        with sr.Microphone() as source:
            eel.show_listening(True)
            # নয়েজ এডজাস্টমেন্ট সময় কমিয়ে ০.৫ সেকেন্ড করা হয়েছে
            listener.adjust_for_ambient_noise(source, duration=0.5)
            # timeout এবং phrase_time_limit দিয়ে দ্রুত রেসপন্স নিশ্চিত করা হয়েছে
            audio = listener.listen(source, timeout=3, phrase_time_limit=5)
            text = listener.recognize_google(audio)
            eel.show_listening(False)
            return text.lower()
    except Exception as e:
        eel.show_listening(False)
        return "Sorry, I couldn't hear you."

# ================== ইউআই শুরু ==================
if __name__ == "__main__":
    eel.start('index.html', size=(950, 700))