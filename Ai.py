import pygame, os, nltk, json, speech_recognition as sr, re, requests, nltk, numpy as np, networkx as nx
from Actions import *
from gtts import gTTS
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
from sklearn.feature_extraction.text import CountVectorizer


JSONFILE = ""
r = sr.Recognizer()
mic = sr.Microphone()

def get_input():
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    transcription = r.recognize_google(audio)
    return transcription

def update_JSON():
    global JSONFILE
    with open("Vocab.json", "r") as jf:
        return json.loads(str(jf.read()))

def Speak(text):
    tts = gTTS(text)
    tts.save("speech.mp3")
    pygame.init()
    pygame.mixer.music.load("speech.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass
    pygame.mixer.music.stop()
    pygame.quit()
    os.remove("speech.mp3")

def detect_subject(question):
    subjects = []
    tokens = nltk.word_tokenize(question)
    tagged_tokens = nltk.pos_tag(tokens)
    for token in tagged_tokens:
        if token[1] == "NNP":
            return token[0], False
    for i in question.split():
        for iI in JSONFILE:
            if i == iI:
                subjects.append(iI)
    return subjects, True

def choose_action(action):
    if action.lower() == JSONFILE[action]:
        weather = json.loads(GetWeather())
        print(weather)
        Speak("It is currently {}ing. The tempeture is {} degres Fahrenheit".format(str(weather["weather"][0]["main"]), str(int(round(((weather["main"]["temp"] - 32) * 5/9) / 4, 0)))))
    else:
        Speak("There is no action for that. Please Email evannriley7@gmail.com to add it")

def scrape_info(topic):
    # Set up the list of websites to scrape
    websites = [
        "https://en.wikipedia.org/wiki/{}".format(topic)
    ]

    # Initialize an empty list to store the results
    results = []

    # Iterate over each website
    for website in websites:
        # Make a request to the website and retrieve the HTML content
        html_doc = requests.get(website).text
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html_doc, 'html.parser')
        # Extract the relevant information from the website
        info = soup.get_text()
        # Add the information to the list of results
        results.extend(info)
        results = ''.join(results)
    # Return the list of results
    return results

def remove_non_text(input_string):
  # Use a regular expression to match any character that is not a letter or a space
  pattern = re.compile(r'[^a-zA-Z\s\.]')
  # Replace all non-letter and non-space characters with an empty string
  output_string = pattern.sub('', input_string)
  return output_string

def summarize(text, question):
    x=0
    lq = question.split(' ')
    for i in lq:
        # logic to decide what it is asking

        # what is a () logic
        if i.lower() == "what" and lq[x+1] == "is" and lq[x+2] == "an" or i.lower() == "what" and lq[x+1] == "is" and lq[x+2] == "a":
            pattern = r'(.*\b(an '+lq[x+3]+r' is)\b.*)'
            match = re.search(pattern, text.lower())
            matches = re.findall(pattern, text.lower())
            print(matches)
        x=x+1

def fallback_response(question):
    text = scrape_info("Apple")
    text = remove_non_text(text)
    summary = summarize(text, question)   
    print(summary)

def Respond_To_Question(question):
    qs = detect_subject(question)
    if qs[1]:
        if qs[0] == "":
            fallback_response(question)
        else:
            q = qs[0]
            word_counts = {}
            for word in q:
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1
            most_common_word = max(word_counts, key=word_counts.get)
            max_count = word_counts[most_common_word]
            tied_words = [word for word, count in word_counts.items() if count == max_count]
            if len(tied_words) > 1:
                Speak("Which of the following did you want, {}".format(' '.join(tied_words)))
                f=False
                c=''
                inp = get_input()
                for n in tied_words:
                    if inp == n:
                        f=True
                        c=n
                if(f):
                    choose_action(c)
                else:
                    Speak("That is not A option")
                    Respond_To_Question(question)
            else:
                choose_action(most_common_word)
    else:
        for i in JSONFILE:
            if i == qs:
                choose_action(qs)

update_JSON()
while True:
    # Listen for audio
    with mic as source:
        print("Listening")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    # Transcribe the audio to text
    transcription = r.recognize_google(audio)

    tr = transcription.split()
    for i in tr:
        if i.lower() == "friday":
            Speak("yes?")
            with mic as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            transcription = r.recognize_google(audio)
            Respond_To_Question(transcription)

    # Print the transcription
    print(transcription)
