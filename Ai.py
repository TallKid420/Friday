import pygame, os, nltk, speech_recognition as sr, re, requests
from Actions import *
from gtts import gTTS
from bs4 import BeautifulSoup

TextInp = True
r = sr.Recognizer()
mic = sr.Microphone()

actions = {
    "weather": GetWeather
}


def get_input():
    if TextInp:
        return input("Input: ")
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    transcription = r.recognize_google(audio)
    return transcription

def Speak(text):
    tts = gTTS(str(text))
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
        for iI in actions:
            if i == iI:
                subjects.append(iI)
    return subjects, True

def choose_action(action):
    if action.lower() in actions:
        # Execute the function associated with the action
        print(actions[action.lower()]())
    else:
        # Action is not recognized
        print("Sorry, I don't know how to perform that action.")

def scrape_info(topic):
    # Set up the list of websites to scrape
    websites = [
        "https://www.google.com/search?q={}".format(topic)
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
    awnsered = False
    x=0
    lq = question.split(' ')
    for i in lq:
        # logic to decide what it is asking

        # what is a () logic
        if i.lower() == "what" and lq[x+1] == "is" and lq[x+2] == "an" and awnsered == False or i.lower() == "what" and lq[x+1] == "is" and lq[x+2] == "a" and awnsered == False:
            awnsered = True
            pattern = r'(.*\b(an '+lq[x+3]+r' is)\b.*)'
            match = re.search(pattern, text.lower())
            matches = re.findall(pattern, text.lower())
            if matches == []:
                Speak("No info Found")
            else:
                Speak(matches[0])
        elif i.lower() == "is" and lq[x+1] == "an" and awnsered == False or i.lower() == "is" and lq[x+1] == "a" and awnsered == False:
            awnsered = True
            pattern = r'(.*\b(an '+lq[x+2]+r' is)\b.*)'
            match = re.search(pattern, text.lower())
            matches = re.findall(pattern, text.lower())
            if matches == []:
                Speak("No info Found")
            else:
                Speak(matches[0])
        x=x+1

def get_subject(question):
  # Tokenize the question
  tokens = nltk.word_tokenize(question)
  # Perform POS tagging on the tokens
  pos_tags = nltk.pos_tag(tokens)
  # Iterate over the POS tags and find the first noun
  for tag in pos_tags:
    if tag[1] == 'NN':
      return tag[0]
  return None


def fallback_response(question):
    print(question)
    text = scrape_info(get_subject(question).upper())
    text = remove_non_text(text)
    summary = summarize(text, question)   
    print(summary)

def Respond_To_Question(question):
    qs = detect_subject(question)
    if qs[1]:
        print(qs[0])
        if qs[0] == []:
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
        for i in actions:
            if i == qs:
                choose_action(qs)

if TextInp:
    while True:
        Respond_To_Question(input("Input: "))
else:
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
