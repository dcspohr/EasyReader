import os
import sys
from gtts import gTTS
import time
import tika
tika.initVM()
from tika import parser
from pydub import AudioSegment
import shutil

def combine_mp3(filename, root_dir, mp3s_dir):
	os.chdir(mp3s_dir)
	files = os.listdir(os.getcwd())
	files.sort(key=os.path.getctime)

	mp3s = []
	for file in files:
		mp3s.append(AudioSegment.from_mp3(file))

	combined = AudioSegment.empty()

	for m in mp3s:
		combined += m
	os.chdir(root_dir)
	combined.export(filename+".mp3", format="mp3")
	
def save_tts(inp, filename):
	tts = gTTS(text=inp, lang='en')
	tts.save(filename[:-4]+".mp3")
	
def parse_txt(filename):
	with open(filename, 'r') as file:
		in1 = file.read()
		return in1
	
def parse_pdf(filename):
	parsed = parser.from_file(filename)
	return parsed["content"]

def chunkify(inp, n=5000): #chunkifies up to n characters (stops at nearest space)
	chunks = []
	print("n = "+str(n))
	chunks += [inp[i:i+n] for i in range(0, len(inp), n)]
	
	subst = ""
	for c in chunks:
		c = subst+c
		for k in range(len(c)-1, 0, -1):
			if c[k] == " ":
				break
		subst = c[k:]
		c = c[:k]
		print(c)
	#save_tts(inp, "tmp/"+filename+"_tmp_"+str(i))
	return chunks

def save_chunks(chunks, filename):
	i=0;
	if os.path.exists("."+filename[:-4]+"_tmp\\"):
		shutil.rmtree("."+filename[:-4]+"_tmp\\")
	os.mkdir("."+filename[:-4]+"_tmp")
	for c in chunks:
		i += 1
		savefile = str(i)+".mp3"
		print("saving part "+str(i))
		save_tts(c, "."+filename[:-4]+"_tmp/"+savefile)
	combine_mp3(filename[:-4], os.getcwd(), os.getcwd()+"\\."+filename[:-4]+"_tmp\\")
	shutil.rmtree("."+filename[:-4]+"_tmp\\")

#def parse_io():
		
#TODO: Support directories
#print("enter filename or directory (end with \\ for a directory):", end='')
filename = input("enter filename: ")
#files_in = []
#if filename[-1] == '\\':
#	for infiles in os.listdir(os.getcwd()+"\\"+filename)
#	files_in = os.listdir(os.getcwd())



inp = ""
if filename[-4:] == ".pdf":
	inp = parse_pdf(filename)
else:
	inp = parse_txt(filename)
inp = inp.replace("\n"," ")

n = 5000
print("\nconverting...")
start = time.time()

save_chunks(chunkify(inp, n), filename)

end = time.time()
print("done\nconversion time", end-start, "seconds")
