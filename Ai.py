import pygame, os, nltk, speech_recognition as sr, re, requests
from Actions import *
from gtts import gTTS
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

TextInp = True
r = sr.Recognizer()
mic = sr.Microphone()

actions = {
    "weather": GetWeather
}
#Face
#Body
#S
#M
def get_relevant_sentence(paragraph, topic):
  # Tokenize the paragraph into sentences
  sentences = sent_tokenize(paragraph)

  # Convert the topic and sentences to lowercase
  topic = topic.lower()
  sentences = [sentence.lower() for sentence in sentences]

  # Remove stopwords from the topic and sentences
  stop_words = set(stopwords.words('english'))
  topic_words = [word for word in word_tokenize(topic) if word not in stop_words]
  sentences = [[word for word in word_tokenize(sentence) if word not in stop_words] for sentence in sentences]

  # Stem the topic words
  stemmer = PorterStemmer()
  topic_words = [stemmer.stem(word) for word in topic_words]

  # Stem the words in each sentence
  sentences = [[stemmer.stem(word) for word in sentence] for sentence in sentences]

  # Join the stemmed words in each sentence back into a single string
  sentences = [' '.join(sentence) for sentence in sentences]

  # Create a TfidfVectorizer and fit it to the stemmed sentences
  vectorizer = TfidfVectorizer()
  vectors = vectorizer.fit_transform(sentences)

  # Get the Tfidf scores of the stemmed topic words
  scores = vectorizer.transform([topic]).toarray()[0]

  # Find the sentence with the highest Tfidf score for the topic words
  max_index = scores.argmax()
  if len(sentences) < max_index:
    max_index = 1
  else:
    relevant_sentence = sentences[max_index]

  # Return the relevant sentence in its original form (not lowercase and without stopwords)
  return sent_tokenize(paragraph)[max_index]


def remove_non_text(input_string):
  # Use a regular expression to match any character that is not a letter or a space
  pattern = re.compile(r'[^a-zA-Z\s\.]')
  # Replace all non-letter and non-space characters with an empty string
  output_string = pattern.sub('', input_string)
  return output_string


def get_summary(query):
  # Make a GET request to the Google search page
  res = requests.get(f'https://www.google.com/search?q={query}')

  # Parse the HTML content of the page
  soup = BeautifulSoup(res.text, 'html.parser')
  # Find the first search result on the page
  result = soup.find('div', id="main")

  # Extract the description of the page
  description = result.text
  description = remove_non_text(description)
  description = get_relevant_sentence(str(description), query)

  return description

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
        Speak(actions[action.lower()]())
    else:
        # Action is not recognized
        Speak("Sorry, I don't know how to perform that action.")

def scrape_info(topic):
    return(get_summary(topic))

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
                return "No info Found"
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
    text = scrape_info(question)
    text = remove_non_text(text)
    Speak(text)
    return text

def Respond_To_Question(question):
    qs = detect_subject(question)
    if qs[1]:
        if qs[0] == []:
            return fallback_response(question)
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

# if TextInp:
#     while True:
#         Respond_To_Question(input("Input: "))
# else:
#     while True:
#         # Listen for audio
#         with mic as source:
#             print("Listening")
#             r.adjust_for_ambient_noise(source)
#             audio = r.listen(source)
#         # Transcribe the audio to text
#         transcription = r.recognize_google(audio)

#         tr = transcription.split()
#         for i in tr:
#             if i.lower() == "friday":
#                 Speak("yes?")
#                 with mic as source:
#                     r.adjust_for_ambient_noise(source)
#                     audio = r.listen(source)
#                 transcription = r.recognize_google(audio)
#                 Respond_To_Question(transcription)

#         # Print the transcription
#         print(transcription)
