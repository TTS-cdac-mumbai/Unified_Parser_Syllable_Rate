import subprocess
from helpers import *
from globals import *
import os
from pydub import AudioSegment
import csv

# for english
# import syllables

g = GLOBALS()

language = "santhali"
text_path = "Santali_txt 00001-04040.txt"
wav_path = "santhali_2703"

textfile_path = os.path.join(language, text_path)

wav_path = os.path.join(language, wav_path)

f = open(os.path.join(wav_path + ".csv"), 'w')
writer = csv.writer(f)
header = ['filename', 'text', 'Syllable Count', 'duration', 'Syllable rate', "file path"]

writer.writerow(header)


# find syllable rate based on audio file

lines = open(textfile_path, encoding='utf-8-sig').readlines()

for root, dirs, files in os.walk(wav_path):
    for file in files:
        # Get the full path to the file

        file_path = os.path.join(root, file)
        print(file_path)

        name, extension = os.path.splitext(file)
        # print(name)
        for line in lines:
            if name in line:
                print(line)

                text_split = line.split('\t')
                #print(text_split)
                wav_name = text_split[0].strip()
                #print(wav_name)
                text = text_split[1]
                #print(text)
                
                #single textline
                syllable_count = 0
                words = text.split(' ')
                #print(words)
                for wrd in words:
                    command = ["python", "uparser.py", wrd, "0", "0", "0"]
                    with open('syl_rate_output.txt', 'a') as output_file:
                        subprocess.run(command, stdout=output_file)
                    # Read the entire file content
                    with open('parser_output.txt', 'r') as file:
                        content = file.read()
                        zero_count = content.count('0')    #syllable count
                    syllable_count += zero_count

                print(f"Syllable Count: {syllable_count}") 

                file_path = (os.path.join(wav_path , wav_name +'.wav'))
                audio = AudioSegment.from_wav(file_path)
                duration_ms = len(audio)
                duration = duration_ms / 1000.0
                print(f"Duration: {duration} second")
                
                syllable_rate = syllable_count/duration
                print(f"Syllable Rate: {syllable_rate} syllable/seconds",'\n')

                writer.writerow([wav_name, text, syllable_count, duration, syllable_rate, file_path])

            


exit()


# find syllable rate based on text file
with open(textfile_path, 'r', encoding='utf-8-sig') as file:
    for line in file:
        #print(line)
        print(line.strip())
        text_split = line.split('\t')
        #print(text_split)
        wav_name = text_split[0].strip()
        #print(wav_name)
        text = text_split[1]
        #print(text)
        
        #single textline
        syllable_count = 0
        words = text.split(' ')
        #print(words)
        for wrd in words:
            command = ["python", "uparser.py", wrd, "0", "0", "0"]
            with open('syl_rate_output.txt', 'a') as output_file:
            	subprocess.run(command, stdout=output_file)
            # Read the entire file content
            with open('parser_output.txt', 'r') as file:
            	content = file.read()
            	zero_count = content.count('0')    #syllable count
            syllable_count += zero_count

            #print(f"Syllable Count: {zero_count}")     
            #with open('syl_rate_output.txt', 'a') as output_file:
                #subprocess.run(command, stdout=output_file)
                #print(g.syllableCount)
                #syllable_count += g.syllableCount
        
        #Duration of audio file


        # for English
        # syllable_count = syllables.estimate(text)

        print(f"Syllable Count: {syllable_count}") 

        file_path = (os.path.join(wav_path , wav_name +'.wav'))
        audio = AudioSegment.from_wav(file_path)
        duration_ms = len(audio)
        duration = duration_ms / 1000.0
        print(f"Duration: {duration} second")
        
        syllable_rate = syllable_count/duration
        print(f"Syllable Rate: {syllable_rate} syllable/seconds",'\n')

        writer.writerow([wav_name, text, syllable_count, duration, syllable_rate, file_path])
        
      

        

