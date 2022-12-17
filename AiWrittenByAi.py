import nltk

def process_input(input_str):
  # Tokenize the input string
  tokens = nltk.word_tokenize(input_str)
  
  # Tag the tokens with their part of speech
  pos_tags = nltk.pos_tag(tokens)
  
  # Determine the intent of the input
  intent = None
  if "greet" in pos_tags:
    intent = "greeting"
  elif "thank" in pos_tags:
    intent = "thanking"
  elif "goodbye" in pos_tags:
    intent = "goodbye"
  
  # Execute the appropriate action based on the intent
  response = ""
  if intent == "greeting":
    response = "Hello! How can I help you today?"
  elif intent == "thanking":
    response = "You're welcome! Is there anything else I can do for you?"
  elif intent == "goodbye":
    response = "Goodbye! Have a great day."
  
  return response

# Test the process_input function
input_str = "Hi, I just wanted to say thank you for your help."
output = process_input(input_str)
print(output) # "Hello! How can I help you today?"
