import subprocess
from helpers import *
from globals import *
import os
from pydub import AudioSegment
import csv
import statistics

# for english
import syllables

g = GLOBALS()

language = "santhali"
text_path = "santali_0651-0698.txt"
wav_dir_path = "santali_0651-0698"
traverse_from = "wav" # text

textfile_path = os.path.join(language, text_path)
wav_dir_path = os.path.join(language, wav_dir_path)
output_file = os.path.join(wav_dir_path + ".csv")

f = open(output_file, 'w')
writer = csv.writer(f)
header = ['id', 'text', 'Syllable Count', 'duration', 'Syllable rate', "file path"]
writer.writerow(header)

sylrate_list = []
not_found = []

def findSyllable(text, wav_file_path):
    
    print("audio : ", wav_file_path)
    print("text : ", text)

    syllable_count = 0

    if(language == "english"):
        syllable_count = syllables.estimate(text)

    else:
        #single textline
        words = text.split(' ')
        for wrd in words:
            command = ["python", "uparser.py", wrd, "0", "0", "0"]
            with open('syl_rate_output.txt', 'a') as output_file:
                subprocess.run(command, stdout=output_file)
            # Read the entire file content
            with open('parser_output.txt', 'r') as file:
                content = file.read()
                zero_count = content.count('0')    #syllable count
            syllable_count += zero_count

    print("Syllable Count: ", syllable_count)

    audio = AudioSegment.from_wav(wav_file_path)
    duration_ms = len(audio)
    duration = duration_ms / 1000.0
    print(f"Duration: {duration} second")
    
    syllable_rate = syllable_count/duration
    sylrate_list.append(syllable_rate)
    print(f"Syllable Rate: {syllable_rate} syllable/seconds",'\n')

    return syllable_count, syllable_rate, duration

def check_ids(notfoundin):
    if not_found:
        print("Not Found id in ", notfoundin )
        for item in not_found:
            print(item) 

def find_stats():
    print("=="*10)
    if sylrate_list:
        mean = statistics.mean(sylrate_list)
        print(f"Mean: {round(mean, 2)}")
        median = statistics.median(sylrate_list)
        print(f"Median: {round(median, 2)}")
        variance = statistics.variance(sylrate_list)
        print(f"Variance: {round(variance, 2)}")

        print("Result is saved in ", output_file)
    else:
        print("Syllable list is empty")





if traverse_from == "wav":
    print("traversing from... ", wav_dir_path , "\n")
    lines = open(textfile_path, encoding='utf-8-sig').readlines()

    for root, dirs, files in os.walk(wav_dir_path):
        for file in files:
            # Get the full path to the file
            file_path = os.path.join(root, file)
            name, extension = os.path.splitext(file)
            found = False
            for line in lines:
                if name in line:
                    text_split = line.split('\t')
                    id = text_split[0].strip()
                    text = text_split[1].strip()

                    syllable_count, syllable_rate, duration = findSyllable(text, file_path)
                    writer.writerow([id, text, syllable_count, duration, syllable_rate, file_path])
                    found = True
            if(found == False):
                not_found.append(name)

    check_ids(textfile_path)

        
# find syllable rate based on text file
elif traverse_from == "text":
    print("traversing from... ", textfile_path, "\n")
    with open(textfile_path, 'r', encoding='utf-8-sig') as file:
        for line in file:
            text_split = line.split('\t')
            id = text_split[0].strip()
            text = text_split[1].strip()
            file_path = (os.path.join(wav_dir_path , id + '.wav'))

            if os.path.isfile(file_path):
                syllable_count, syllable_rate, duration = findSyllable(text, file_path)
                writer.writerow([id, text, syllable_count, duration, syllable_rate, file_path])

            else:
                not_found.append(id)

    check_ids(wav_dir_path)       

# find mean median and Variance
find_stats()




