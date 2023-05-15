import subprocess
import os 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

files = [
       # 'dataGet',
         'dataBuild',
         'training',
         'predict']

for i, el in enumerate(files):
    subprocess.call(["python", files[i] + '.py'])