from espeak import espeak
from subprocess import call
import re

def VoiceSpeak(paragraph):
    cmd_beg= 'espeak'
    cmd_voice = 'en+f1'
    cmd_speed = '-s110 '

    pauseBlank = 1
    sentences = re.split(r'(?<=[.!?])\s+|\n', paragraph)  # Split paragraph into sentences and line breaks using regular expressions
    ssml_sentences = []
    print(sentences)

    for sentence in sentences:
        ssml_sentence = f'{sentence}<break time="{pauseBlank}s"/>'
        ssml_sentences.append(ssml_sentence)
    
    ssml_paragraph = '<speak>' + ' '.join(ssml_sentences) + '</speak>'
    call(['espeak', '-m', cmd_speed, ssml_paragraph, '-v', cmd_voice])
