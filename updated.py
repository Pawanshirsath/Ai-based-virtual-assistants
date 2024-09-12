import os
import webbrowser
import pyautogui
import requests
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import openai 
import speedtest
import smtplib
import pyjokes
import json

EMAIL_ADDRESS = 'pavanshirsath3@gmail.com'
EMAIL_PASSWORD = '-------'
WEATHER_API_KEY = '-----' # Your weather API key
NEWS_API_KEY = '-------'       # Your news API key

listener = sr.Recognizer()
machine = pyttsx3.init()

openai.api_key = 'sk-proj-XKipKj---'  # Replace 'your_openai_api_key' with your actual OpenAI API key
model_engine = "gpt-3.5-turbo"

def talk(text):
    machine.say(text)
    machine.runAndWait()
    print("Assistant:", text)

def chatGPT(query):
    try:
        response = openai.Completion.create(
            engine=model_engine,
            prompt=query,
            max_tokens=50
        )
        response_text = response.choices[0].text.strip()
        print("AI Response:", response_text)
        return response_text
    except Exception as e:
        if "quota exceeded" in str(e).lower():
            error_message = f"Error: Quota exceeded for ChatGPT. Consider reducing usage or upgrading your OpenAI plan."
            print(error_message)
            return "I'm unable to answer that right now due to limitations. Try rephrasing your question or I can help you with something else."
        else:
            # Handle other exceptions
            error_message = f"Error occurred during chatGPT: {e}"
            print(error_message)
            return "Sorry, I'm having trouble responding to that right now."

def get_news():
    """Function to fetch latest news headlines."""
    try:
        url = f'https://newsapi.org/v2/top-headlines?country=in&apiKey=acb75e46254b4e0197208fdc6202f296'
        response = requests.get(url)
        data = response.json()
        articles = data['articles']
        for idx, article in enumerate(articles[:5]):
            talk(f"News {idx + 1}: {article['title']}")
    except Exception as e:
        error_message = f"Error occurred while fetching news data: {e}"
        print(error_message)

def input_instruction():
    try:
        with sr.Microphone() as origin:
            print("Listening...")
            speech = listener.listen(origin)
            print("Recognizing...")
            instruction = listener.recognize_google(speech)
            print("You said:", instruction)
            return instruction.lower()
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except Exception as e:
        print("Error occurred: {0}".format(e))
    return "" 

def alarm(query):
    timehere = open("Alarmtext.txt","a")
    timehere.write(query)
    timehere.close()
    os.startfile("alarm.py")

def send_email(recipient, subject, message):
    try:
        sent_from = EMAIL_ADDRESS
        to = recipient
        email_text = f"""\
        From: {sent_from}
        To: {to}
        Subject: {subject}

        {message}
        """
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(sent_from, to, email_text)
        server.close()
        print("Email sent successfully!")
        talk("Email sent successfully!")
    except Exception as e:
        error_message = f"Error occurred while sending email: {e}"
        print(error_message)

def play_assistant():
    def greet():
        current_time = datetime.datetime.now()
        hour = current_time.hour
        if 0 <= hour < 12:
            talk("Good morning! How can I assist you today?")
        elif 12 <= hour < 18:
            talk("Good afternoon! How can I assist you today?")
        else:
            talk("Good evening! How can I assist you today?")

    greet()  # Call greet function at the beginning
    while True:  # Loop indefinitely until termination command
        instruction = input_instruction()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
        for site in sites:
            if f"Open {site[0]}".lower() in instruction:
                talk(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                print(f"Opening {site[0]}")
    
        if "play" in instruction:
            song = instruction.replace('play', "")
            talk("playing..... " + song)
            pywhatkit.playonyt(song)
            print("Playing song:", song)

        elif 'time' in instruction:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            talk(f"Sir time is {hour} bajke {min} minutes")
            print(f"Current time: {hour}:{min}")

        elif 'date' in instruction:
            date = datetime.datetime.now().strftime('%d /%m /%Y')
            talk("Today's date is " + date)
            print("Today's date:", date)

        elif 'how are you' in instruction:
            talk('I am fine, how about you')
            print("Assistant: I am fine, how about you")

        elif 'what is your name' in instruction:
            talk('I am your personal assistant, you can call me aaba saheb')
            print("Assistant: I am your personal assistant, you can call me aaba saheb")

        elif 'who is' in instruction:
            human = instruction.replace('who is', "")
            info = wikipedia.summary(human, 1)
            talk(info)
            print("Assistant:", info)

        elif "pause" in instruction:
            pyautogui.press("k")
            talk("Video paused")
            print("Assistant: Video paused")

        elif "internet speed" in instruction:
            wifi  = speedtest.Speedtest()
            upload_net = wifi.upload()/1048576         #Megabyte = 1024*1024 Bytes
            download_net = wifi.download()/1048576
            talk(f"Wifi download speed is {download_net}")
            talk(f"Wifi upload speed is {upload_net}")
            print(f"Wifi download speed is {download_net} MBps")
            print(f"Wifi upload speed is {upload_net} MBps")

        elif "alarm" in instruction:
            print("Input time example:- 10 and 10 and 10")
            talk("Set the time")
            a = input("Please tell the time: ")
            alarm(a)
            talk("Done, sir")
            print("Alarm set for:", a)

        elif 'news' in instruction:
            talk("Sure, here are the latest news headlines.")
            get_news()

        elif 'chat' in instruction:
            talk("Sure, what do you want to chat about?")
            query = "give me roadmap of full stack webdevelopment"
            response = chatGPT(query)
            talk(response)

        elif 'author pawan' in instruction:
            talk("Pawan Shirsath, a dedicated and ambitious student currently pursuing a B.Sc in Computer Science and B.Tech in Robotics With a strong passion for technology, innovation, and tackling challenging tasks, I am constantly expand my knowledge and skills. As a learner, I thrive on exploring new areas and pushing my limits. Content creation, coding, web and WordPress development, video editing, graphics design, and digital marketing are my areas of interest and expertise. ")
            print("Assistant: Pawan Shirsath's bio displayed")

        elif 'hod' in instruction:
            talk("professor vishnu kale sir  is Asst. Prof. & HOD of  Automation & Robotics Department, MET's Institute of Technology- B Tech, Nashik. also Working as ML Engineer with 3 yrs of experience in finance and automobile domain. Possess knowledge in Python, ML Algo, Pandas, Scikitlearn, SQL, Matplotlib, Data Analysis..")
            print("Assistant: Information about Professor Vishnu Kale sir displayed")

        elif 'professor pathak sir' in instruction:
            talk("He is Training and Placement Officer at MET Institute of Technology (P)- B Tech Bhujbal Knowledge City, Nashik")
            print("Assistant: Information about Professor Pathak displayed")

        elif "whatsapp" in instruction:
            phone_number = "+919373591927"  # Replace with the recipient's phone number
            talk("Sure, please tell me what message you want to tell.")
            message = input_instruction()
            hour = 13  # Replace with the hour
            minute = 43  # Replace with the minute

            message1 = pywhatkit.sendwhatmsg(phone_number, message, hour, minute)
            talk(message1)

        elif "search" in instruction:
            talk("Sure, I can perform a search. What would you like me to look up?")
            query = input_instruction()
            pywhatkit.search(query)

        elif 'tell a joke' in instruction:
            tell_joke()

        elif 'take a screenshot' in instruction:
            folder_path ='C:\\Users\\Pawan Shirsath\\Documents'  # Change to the desired folder path
            take_screenshot(folder_path)

        elif 'take a note' in instruction:
            talk("Sure, please speak your note.")
            note = input_instruction()
            with open("notes.txt", "a") as file:
                file.write(note + "\n")
            talk("Note saved successfully.")
            print("Assistant: Note saved")

        elif 'read my notes' in instruction:
            try:
                with open("notes.txt", "r") as file:
                    notes = file.readlines()
                    for note in notes:
                        talk(note.strip())
            except FileNotFoundError:
                talk("You don't have any saved notes.")
                print("Assistant: No saved notes found")

        elif 'email' in instruction:
            talk("Sure, i will send the email to pawan.")
            recipient = "pavanshirsath16@gmail.com"
            talk("What is the subject of the email?")
            subject = input()
            talk("What is the message you want to send?")
            message = input()
            send_email(recipient, subject, message)

        elif 'weather' in instruction:
            location = "nashik"  # Replace with your location
            weather_data = get_weather_data(location)
            summary = generate_weather_summary(weather_data)
            talk(summary)

        elif 'open' in instruction:
            words = instruction.split()
            app_name = " ".join(words[words.index('open') + 1:])
            launch_application(app_name)

        elif 'quit' in instruction or 'exit' in instruction:
            talk("Goodbye!")
            print("Assistant: Goodbye!")
            break

        else:
            talk('Please repeat')
            print("Assistant: Please repeat")

def take_screenshot(folder_path):
    try:
        screenshot = pyautogui.screenshot()
        file_path = os.path.join(folder_path, "screenshot.png")
        screenshot.save(file_path)
        print("Screenshot saved successfully at:", file_path)
    except Exception as e:
        print("Error occurred while taking screenshot:", str(e))

def tell_joke():
    joke = pyjokes.get_joke()
    talk("Here's a joke for you:")
    talk(joke)

def get_weather_data(location):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?unitGroup=us&key={WEATHER_API_KEY}&contentType=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch weather data")
        return None

def generate_weather_summary(weather_data):
    if not weather_data:
        return "Failed to fetch weather data"

    # Extracting today's weather information
    today_weather = weather_data.get("days", [])[0]
    date = today_weather.get("datetime", "")
    conditions = today_weather.get("conditions", "")
    temp_max = today_weather.get("tempmax", "")
    temp_min = today_weather.get("tempmin", "")

    # Generating summary for today's weather
    summary = f"Weather for {date}: {conditions}, Max Temp: {temp_max}°F, Min Temp: {temp_min}°F"
    
    return summary

def launch_application(application_name):
    application_paths = {
        "vlc": "C:\\Users\\Public\\Desktop\\VLC media player.lnk",
        "chrome": "C:\\Users\\Public\\Desktop\\Google Chrome.lnk",
        "notepad": "C:\\Windows\\system32\\notepad.exe"  # Example path for Notepad
        # Add more applications and their paths as needed
    }

    application_path = application_paths.get(application_name.lower())
    if application_path:
        try:
            os.startfile(application_path)
            print(f"{application_name.capitalize()} launched successfully.")
            talk(f"{application_name.capitalize()} launched successfully.")
        except Exception as e:
            print(f"Error occurred while launching {application_name}: {str(e)}")
            talk(f"Error occurred while launching {application_name}.")
    else:
        print(f"Application '{application_name}' not found.")
        talk(f"Sorry, I couldn't find the application '{application_name}'.")

if __name__ == "__main__":
    play_assistant()
