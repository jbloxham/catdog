from features import mfcc
import scipy.io.wavfile as wav
from hmmlearn.hmm import GMMHMM

cat = []
dog = []

for i in range(50):
    (rate,sig) = wav.read("data/cat/" + str(i) + ".wav")
    cat.append(mfcc(sig,rate))
    
    (rate,sig) = wav.read("data/dog/" + str(i) + ".wav")
    dog.append(mfcc(sig,rate))

cutoff = 45
    
catmodel = GMMHMM(n_components=5, n_mix=5)
catmodel.fit(cat[:cutoff])

dogmodel = GMMHMM(n_components=5, n_mix=5)
dogmodel.fit(dog[:cutoff])

testdata = cat[cutoff:] + dog[cutoff:]
for i in range(100-2*cutoff):
    catscore = catmodel.score(testdata[i])
    dogscore = dogmodel.score(testdata[i])
    print catscore, dogscore
    if catscore > dogscore:
        print "cat"
    else:
        print "dog"

(rate,sig) = wav.read("help.wav")
feat = mfcc(sig,rate)
print catmodel.score(feat), dogmodel.score(feat)
if (catmodel.score(feat) > dogmodel.score(feat)):
    print "cat"
else:
    print "dog"

for i in range(1,6):
    (rate,sig) = wav.read("connected_data/" + str(i) + ".wav")
    feat = mfcc(sig,rate)
    print i, len(feat)
    dp = [x[:] for x in [[1]*4]*(len(feat)+1)]
    dp[0][0] = 0
    st = [x[:] for x in [[""]*4]*(len(feat)+1)]

    catscores = [x[:] for x in [[0]*len(feat)]*len(feat)]
    dogscores = [x[:] for x in [[0]*len(feat)]*len(feat)]
    for t in range(len(feat)):
        if t % 10 == 0:
            print t, "/", len(feat)
        for tf in range(t+75, min(t+200, len(feat))):
            catscores[t][tf] = catmodel.score(feat[t:tf])
            dogscores[t][tf] = dogmodel.score(feat[t:tf])

    for lvl in range(3):
        for t in range(len(feat)):
            for tf in range(t+75, (min(t+200, len(feat)))):
                catscore = catscores[t][tf]
                dogscore = dogscores[t][tf]
                score = dogscore
                nextst = "dog"
                if catscore > dogscore:
                    score = catscore
                    nextst = "cat"
                if dp[tf][lvl+1] < dp[t][lvl] + score or dp[tf][lvl+1] == 1:
                    dp[tf][lvl+1] = dp[t][lvl] + score
                    st[tf][lvl+1] = st[t][lvl] + nextst

    print st[len(feat)-1][3]
    
import alsaaudio, wave, numpy
import time

while True:
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
    inp.setchannels(1)
    inp.setrate(44100)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(1024)

    str = raw_input("Ready to record?")
    
    w = wave.open('tmp.wav', 'w')
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(44100)

    start = time.time()
    while time.time()-start < 2:
        l, data = inp.read()
        a = numpy.fromstring(data, dtype='int16')
        w.writeframes(data)

    (rate,sig) = wav.read("tmp.wav")
    feat = mfcc(sig,rate)
    print catmodel.score(feat), dogmodel.score(feat)
    if (catmodel.score(feat) > dogmodel.score(feat)):
        print "cat"
    else:
        print "dog"
