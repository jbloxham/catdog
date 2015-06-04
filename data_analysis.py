from features import mfcc
import scipy.io.wavfile as wav
from hmmlearn.hmm import GMMHMM
import os, sys

train_cutoff = 45

base = raw_input('Enter corpus directory: ')

path = 'corpora/' + base + '/'
if not os.path.exists(path):
    print 'Corpus not found at path: ' + path
    print 'Exiting'
    sys.exit()
    
words = set()
for f in os.listdir(path):
    word = f.split('_')[0]
    words.add(word)
    
print 'Found words:'
for word in words:
    print word

print 'Specify words to be removed. Enter "DONE" when finished'
word = raw_input('')
while word != 'DONE':
    words.remove(word)
    
data = {}
models = {}
for word in words:
    data[word] = []
    
    for i in range(50):
        (rate,sig) = wav.read(path + word + "_" + str(i) + ".wav")
        data[word].append(mfcc(sig,rate))

    models[word] = GMMHMM(n_components=5, n_mix=5)
    models[word].fit(data[word][:train_cutoff])
    

testdata = []
for word in words:
    testdata += data[word][train_cutoff:]
                     
for test in testdata:
    scores = {}
    maxscore = 0
    maxword = ''
    for word in words:
        scores[word] = models[word].score(test)
        #print scores[word]
        if (scores[word] > maxscore or maxscore == 0):
            maxword = word
            maxscore = scores[word]
        
    print maxword
    #print maxscore

import alsaaudio, wave, numpy
import time

while True:
    if os.path.isfile('tmp.wav'):
        os.remove('tmp.wav')
    
    begin = raw_input('Hit enter to begin recording.')
    
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
    inp.setchannels(1)
    inp.setrate(44100)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(1024)
    
    w = wave.open('tmp.wav', 'w')
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(44100)
    
    print 'Now recording. Hit Ctrl-C to stop.'
    
    try:
        while True:
            l, data = inp.read()
            w.writeframes(data)
    except:
        pass

    print ''
    
    (rate,sig) = wav.read("tmp.wav")
    feat = mfcc(sig,rate)

    maxscore = 0
    maxword = ''
    for word in words:
        scores[word] = models[word].score(feat)
        print word + ": " + str(scores[word])
        if (scores[word] > maxscore or maxscore == 0):
            maxword = word
            maxscore = scores[word]

    print ''
    print maxword

    os.remove('tmp.wav')
