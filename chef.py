import subprocess

files = ['dataBuild','skynetTrain','useSkynet']

print("START")
for i, el in enumerate(files):
    subprocess.call(["python", files[i] + '.py'])
print("FINISH")