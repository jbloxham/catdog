import sys
import os

num = 0
for filename in os.listdir('orig_data/dog'):
    print(filename)
    #os.rename('orig_data/dog/' + filename, 'orig_data/dog/' + str(num) + '.m4a')
    cmd = 'ffmpeg -i orig_data/dog/' + str(num) + '.m4a -f wav data/dog/' + str(num) + '.wav'
    print(cmd)
    os.system(cmd)
    num += 1

num = 0
for filename in os.listdir('orig_data/cat'):
    print(filename)
    #os.rename('orig_data/cat/' + filename, 'orig_data/cat/' + str(num) + '.m4a')
    cmd = 'ffmpeg -i orig_data/cat/' + str(num) + '.m4a -f wav data/cat/' + str(num) + '.wav'
    print(cmd)
    os.system(cmd)
    num += 1
    
