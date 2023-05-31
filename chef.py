import subprocess
import os 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import sys

start=0
if len(sys.argv) > 1:
    start = int(sys.argv[1])

files = [
         'dataGet',
         'dataBuild',
         'training',
         'predict']

files = files[start:]
for i, el in enumerate(files):
    subprocess.call(["python", files[i] + '.py'])