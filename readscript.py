# -*- coding: utf-8 -*-
"""readscript.ipynb

Original file is located at
    https://colab.research.google.com/drive/10_siArF4ohhLKKwH6EgO4nn7bh0KYSPP
"""


import json

#each speaker's individual turn
def processTurn(turn, write_file):

    dialogue = " " if turn['speaker'] is None or turn['speaker']['name'] is None else f"{turn['speaker']['name']}: "


    for text_block in turn['text_blocks']:
      dialogue += f"{text_block['text']} "


    dialogue += "\n"

    write_file.write(dialogue)



def process_sections(section, write_file):
  for turn in section['turns']:
    processTurn(turn, write_file)

def process_json_file(filename):
  with open(filename, 'r') as file:

    data = json.load(file)

    transcript = data['transcript']

    write_file_name = transcript['title'].replace('.','_')
    print(f"Writing to {write_file_name}")
    write_file = open(f"{write_file_name}.txt",'a')


    number_of_sections_processed = 0

    for section in transcript['sections']:
      process_sections(section, write_file)
      number_of_sections_processed += 1

    print(f"Processed {number_of_sections_processed} sections")




    write_file.close()

    print(f"Finished Processing file {filename}")

process_json_file('/content/supreme_court_transcripts/oyez/cases/2023.22-1178-t01.json')

process_json_file('/content/supreme_court_transcripts/oyez/cases/1966.914-t01.json')
#also has a t02

process_json_file('/content/supreme_court_transcripts/oyez/cases/2023.23-719-t01.json')
