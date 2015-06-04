import os

import alsaaudio, wave, numpy

base = raw_input('Enter corpus directory: ')

path = 'corpora/' + base + '/'
if not os.path.exists(path):
    os.makedirs(path)

index = {}

last = ''

while True:
    filename = raw_input("Enter transcription: ")
    if filename == '' and last != '':
        filename = last
    if not filename in index:
        index[filename] = 0

    begin = raw_input('Hit enter to begin recording.')
    
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
    inp.setchannels(1)
    inp.setrate(44100)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    inp.setperiodsize(1024)
    
    w = wave.open(path + filename + '_' + str(index[filename]) + '.wav', 'w')
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
    print filename + '_' + str(index[filename]) + '.wav recorded!'
    print ''
    
    index[filename] += 1
    last = filename

