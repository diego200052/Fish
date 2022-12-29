"""
Script to creat a CSV annotation files for all the images in a given folder
and given text file.
The text file here is TrainIJCNN2013/gt.txt, so the code is according to that.
"""

import pandas as pd
import os
import lxml.etree as ET

# Enter the path to the directory that labels are
LABELS_PATH = "./Annotations/"
CLASSES_PATH = "./classes.txt"
CSV_OUTPUT_PATH = "./labels.csv"

def read_text_file_line_by_line(file_path):
    with open(file_path, 'r') as f:
        # read the lines of the file
        lines = f.readlines()

    return lines

def txts_to_csv(LABELS_FILENAMES, CLASSES_DICTIONARY):

    print("Total files:", len(LABELS_FILENAMES))
    AllDfs = []

    for label_filename in LABELS_FILENAMES:

        xml_list = []
        tree = ET.parse(LABELS_PATH + label_filename)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                    int(root.find('size')[0].text),
                    int(root.find('size')[1].text),
                    member[0].text,
                    int(member[4][0].text),
                    int(member[4][1].text),
                    int(member[4][2].text),
                    int(member[4][3].text)
                    )
            xml_list.append(value)
        print(xml_list)

        column_name = ['file_name', 'width', 'height', 
            'class_name', 'x_min', 'y_min', 'x_max', 'y_max']
        xml_df = pd.DataFrame(xml_list, columns=column_name)
        AllDfs.append(xml_df)

    print("Total Dfs:", len(AllDfs))
    df_combined = pd.concat(AllDfs)
    df_combined = df_combined.reset_index()
    df_combined = df_combined.drop(columns="index")
    print(df_combined)
    df_combined.to_csv(CSV_OUTPUT_PATH, index=False)
    print("CSV file saved! Done.")

def createDictionary(CLASSES_LIST):
    DICT = {}
    for i in range(len(CLASSES_LIST)):
        DICT[i] = CLASSES_LIST[i].strip("\n")
    return DICT

# MAIN

LABELS_FILENAMES = os.listdir(LABELS_PATH)
CLASSES_LIST = read_text_file_line_by_line(CLASSES_PATH)
CLASSES_DICTIONARY = createDictionary(CLASSES_LIST)

txts_to_csv(LABELS_FILENAMES, CLASSES_DICTIONARY)