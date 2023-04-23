# Split long text into sentences is good for generating audio files for each sentence. But it is not good for generating video subtile

# Import the necessary modules
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

TOO_SHORT = 20

# Text to sentences, nltk is not working for Chinese
def text_to_sentences(text):
    # Split text into sentences
    sentences = sent_tokenize(text)
    # Join sentences if they are too short
    sentences = join_short_sentences(sentences)
    return sentences

# Join short sentences
def join_short_sentences(sentences):
    if len(sentences) < 2:
        return sentences
    # Join sentences if they are too short
    new_setences = []
    joined_sentence = ''
    for s in sentences:
        joined_sentence += s
        if len(joined_sentence) < TOO_SHORT and len(joined_sentence) < 200:
            continue
        else:
            new_setences.append(joined_sentence)
            joined_sentence = ''
    if joined_sentence:
        new_setences.append(joined_sentence)
    return new_setences

