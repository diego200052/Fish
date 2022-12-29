"""
Script to create a training and validation CSV file.
"""

import pandas as pd
import shutil
import os

def train_valid_split(all_images_folder=None, all_annots_csv=None, split=0.15):
    all_df = pd.read_csv(all_annots_csv)
    # Shuffle the CSV file rows.
    all_df.sample(frac=1)
    print(all_df)
    len_df = len(all_df)
    train_split = int((1-split)*len_df)

    train_df = all_df[:train_split]
    valid_df = all_df[train_split:]
    #print(train_df)
    #print(valid_df)

    os.makedirs('../input/train', exist_ok=True)
    os.makedirs('../input/test', exist_ok=True)

    # Copy training images.
    train_images = train_df['file_name'].tolist()
    for image in train_images:
        shutil.copy(
            f"../input/images/{image}", 
            f"../input/train/{image}"
        )
        wE = image[:-4]
        shutil.copy(
            f"./Annotations/{wE}.xml",
            f"../input/train/{wE}.xml",
        )
    train_df.to_csv('../input/train_labels.csv', index=False)

    # Copy validation images.
    valid_images = valid_df['file_name'].tolist()
    for image in valid_images:
        shutil.copy(
            f"../input/images/{image}", 
            f"../input/test/{image}"
        )
        wE = image[:-4]
        shutil.copy(
            f"./Annotations/{wE}.xml",
            f"../input/test/{wE}.xml",
        )
    valid_df.to_csv('../input/test_labels.csv', index=False)

train_valid_split(all_images_folder='../input/images', all_annots_csv='../input/labels/labels.csv', split=0.2)