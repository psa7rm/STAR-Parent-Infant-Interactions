# -*- coding: utf-8 -*-
"""Data Cleaning Capstone.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KxBLoKYI4CpsSNjMbm6XkplilJIhA3fK
"""

from google.colab import drive
drive.mount('/content/drive')

import numpy as np
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras import layers, models
import glob

import torch
print(torch.__version__)
import torch.nn.functional as F
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader, random_split
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from functools import partial

import librosa
from datetime import datetime
from datetime import timedelta
import shutil

pwd

"""# Loading in Labeled Excel Files"""

#Change path to where the coded files are stored in you Drive

path = "/your_path/ReCodedFiles/"

xlfiles = glob.glob(path + "*.xlsx")

xlfiles

"""# Data Manipulation Functions"""

def convert_to_timedelta(time_str):
    # Split the string on the colon
    parts = time_str.split(':')

    # Parse minutes and seconds from the parts
    minutes = int(parts[0])
    seconds = int(parts[1]) if len(parts) > 1 else 0

    # Create a timedelta object
    time_delta = timedelta(minutes=minutes, seconds=seconds)

    return time_delta

def save_fig(file, file_name, save_path):
    frame_size = 2048
    hopsize = 512
    y_axis = "linear"

    y = np.abs(file) ** 2
    y_log = librosa.power_to_db(y)
    plt.figure(figsize = (25,9))
    plt.axis('off')
    _ = librosa.display.specshow(y_log, sr = sample_rate, hop_length = hopsize,
                            x_axis = "time", y_axis = y_axis, )
    plt.savefig(save_path + file_name + ".jpg", bbox_inches = "tight", pad_inches = 0)
    plt.close()

def gen_excel_data(file):
  print(str((file.split("/")[-1].split(".mp3")[0])))
  #Read in file
  df = pd.read_excel(file, usecols=[0, 1, 2], engine='openpyxl')
  # Drop rows where any cell is NA
  df_clean = df.dropna()
  data_as_list = df_clean.values.tolist()

  # List to store the new intervals
  new_intervals = []

  # Generate three-second intervals
  for row in data_as_list:
    if type(row[0]) == datetime.time:
      t1 = row[0]
      current_time = timedelta(hours=t1.hour, minutes=t1.minute, seconds=t1.second)
    else:
      current_time = convert_to_timedelta(row[0])
    if type(row[1]) == datetime.time:
      t2 = row[1]
      end_time = timedelta(hours=t2.hour, minutes=t2.minute, seconds=t2.second)
    else:
      end_time = convert_to_timedelta(row[1])
    classification = row[2]
    while current_time < end_time:
        # Calculate the next time point, without exceeding the end time
        next_time = min(current_time + pd.Timedelta(seconds=3), end_time)
        # Append the new interval to the list
        new_intervals.append([current_time, next_time, classification])
        current_time = next_time

  return new_intervals

def process_data(file, custom_intervals, save_path_img):
    file_name = file.split("/")[-1].split(".mp3")[0]
    print("Processing: "+ file_name)
    # Load the entire audio file
    audio, sr = librosa.load(file, sr = 16000)
    frame_size = 2048
    hopsize = 512
    y_axis = "linear"

    # Process each custom interval
    for i, interval in enumerate(custom_intervals):
        # Extract timedelta objects and convert to total seconds
        start_sec, end_sec = [t.total_seconds() for t in interval[:2]]

        # Convert start and end times in seconds to samples
        start_sample = int(start_sec * sr)
        end_sample = int(end_sec * sr)

        # Ensure the interval does not exceed the audio length
        if end_sample > len(audio):
            print(f"End sample for interval {i} exceeds audio length. Skipping this interval.")
            continue

        # Extract the interval
        audio_interval = audio[start_sample:end_sample]

        # Perform the STFT on the current interval
        D = librosa.stft(audio_interval)
        D_magnitude = np.abs(D)
        D_db = librosa.amplitude_to_db(D_magnitude, ref=np.max)

        # Save as Image file
        plt.figure(figsize = (25,9))
        plt.axis('off')
        _ = librosa.display.specshow(D_db, sr = sr, hop_length = hopsize,
                            x_axis = "time", y_axis = y_axis, )
        plt.savefig(save_path_img + file_name + "(" + str(start_sec) + " to " + str(end_sec) + ") " + interval[2] + ".jpg", bbox_inches = "tight", pad_inches = 0)
        plt.close()

        # # Save the interval to a CSV file
        # interval_filename = f'{file}_interval_{i}.csv'
        # np.savetxt(interval_filename, D_db, delimiter=',')

        # Optional: Store the interval in a dictionary with a label if needed
        # train_mat_dict[interval_filename] = [D_db, "parent"]

        print(f"Processed interval {i} ({start_sec}s to {end_sec}s) of file {file}, {interval[2]}")

"""# Loading in .mp3 Files"""

# Path to the directory containing CSV files
directory_path = "/your_mp3_file_path/"

# Get a list of all CSV files in the directory
mp3_files = glob.glob(directory_path + "*.mp3")



len(mp3_files)

test_files = [directory_path + '138 T1 part 1 child audio.mp3',
              directory_path + '199 T1 child audio.mp3',
              directory_path + '209 T2 part 3 child audio.mp3',
              directory_path + '262 T2 part 2 child audio.mp3',
              directory_path + '287 T2 part 2 child audio.mp3',
              directory_path + '301 T1 part 2 child audio.mp3',
              directory_path + '522 T1 part 4 child audio.mp3',
              directory_path + '554 T1 part 2 child audio.mp3',
              directory_path + '110 T2 part 2 child audio.mp3',
              directory_path + '531 T2 part 2 child audio.mp3']

"""
138 T1 part 1 child audio Output"""

filename = test_files[0]
print(filename.split("/")[-1].split(".mp3")[0])
excel_file = gen_excel_data(xlfiles[5])

#Set output path

spath = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/Test1/"

process_data(filename, excel_file, spath)

"""199 T1 child audio Output"""

filename2 = test_files[1]
print(filename2.split("/")[-1].split(".mp3")[0])
excel_file2 = gen_excel_data(xlfiles[6])

#Set output path

spath2 = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/Test2/"

process_data(filename2, excel_file2, spath2)

"""110 T2 part 2 child audio Output"""

filename = test_files[8]
print(filename.split("/")[-1].split(".mp3")[0])
excel_file = gen_excel_data(xlfiles[4])

len(excel_file)

#Set output path

spath = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/Test3/"

process_data(filename, excel_file, spath)

"""531 T2 part 2 child audio Output"""

filename = test_files[9]
print(filename.split("/")[-1].split(".mp3")[0])
excel_file = gen_excel_data(xlfiles[2])

#Set output path

spath = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/Test4/"

process_data(filename, excel_file, spath)

"""
554 T1 part 2 child audio Output"""

filename = test_files[7]
print(filename.split("/")[-1].split(".mp3")[0])
excel_file = gen_excel_data(xlfiles[1])

#Set output path

spath = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/Test4/"

process_data(filename, excel_file, spath)

"""522 T1 part 4 child audio Output"""

filename = test_files[6]
print(filename.split("/")[-1].split(".mp3")[0])
excel_file = gen_excel_data(xlfiles[0])

#Set output path

spath = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/Test5/"

process_data(filename, excel_file, spath)

"""262 T2 part 2 child audio Output"""

filename = test_files[3]
print(filename.split("/")[-1].split(".mp3")[0])
excel_file = gen_excel_data(xlfiles[9])

len(excel_file)

#Set output path

spath = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/Test6/"

process_data(filename, excel_file, spath)

"""Issues with 209, 287 , 301"""

xlfiles[7]

"""287 T2 part 2 child audio Output"""

filename = test_files[4]
print(filename.split("/")[-1].split(".mp3")[0])
excel_file = gen_excel_data_dt(xlfiles[7])

len(excel_file)

#Set output path

spath = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/Test7/"

process_data(filename, excel_file, spath)

"""301 T1 part 2 child audio Output"""

filename = test_files[5]
print(filename.split("/")[-1].split(".mp3")[0])
excel_file = gen_excel_data(xlfiles[9])

len(excel_file)

#Set output path

spath = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/Test8/"

process_data(filename, excel_file, spath)

"""209 T2 part 3 child audio Output

Had to modify function for format of this excel file
"""

def gen_excel_data_dt(file):
  print(str((file.split("/")[-1].split(".mp3")[0])))
  #Read in file
  df = pd.read_excel(file, usecols=[0, 1, 2], engine='openpyxl')
  # Drop rows where any cell is NA
  df_clean = df.dropna()
  data_as_list = df_clean.values.tolist()

  format_string = "%H:%M:%S"

  # List to store the new intervals
  new_intervals = []

  # Generate three-second intervals
  for row in data_as_list:
    if type(row[0]) == datetime.time:
      t1 = row[0]
      current_time = timedelta(hours=t1.hour, minutes=t1.minute, seconds=t1.second)
    else:
      dt0 = datetime.strptime(row[0], format_string).time()
      current_time = timedelta(hours=dt0.hour, minutes=dt0.minute, seconds=dt0.second)
    if type(row[1]) == datetime.time:
      t2 = row[1]
      end_time = timedelta(hours=t2.hour, minutes=t2.minute, seconds=t2.second)
    else:
      dt1 = datetime.strptime(row[1], format_string).time()
      end_time = timedelta(hours=dt1.hour, minutes=dt1.minute, seconds=dt1.second)
    classification = row[2]
    while current_time < end_time:
        # Calculate the next time point, without exceeding the end time
        next_time = min(current_time + pd.Timedelta(seconds=3), end_time)
        # Append the new interval to the list
        new_intervals.append([current_time, next_time, classification])
        current_time = next_time

  return new_intervals

filename = test_files[2]
print(filename.split("/")[-1].split(".mp3")[0])
excel_file = gen_excel_data_dt(xlfiles[3])

#Set output path

spath = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/Test9/"

process_data(filename, excel_file, spath)

"""# Organizing Image Files"""

#Change path to where the coded files are stored in you Drive

path = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/Test1/"

image_files = glob.glob(path + "*.jpg")

len(image_files)

for i in range(2, 10):
  path = f"/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/Test{i}/"
  new_files = glob.glob(path + "*.jpg")
  image_files.extend(new_files)
  print(i, len(new_files))

len(image_files)

import os

# Specify the directory you want to search
directory = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/Test1/"

# List all entries in the directory
entries = os.listdir(directory)

# Count files (ignoring subdirectories)
file_count = sum(os.path.isfile(os.path.join(directory, entry)) for entry in entries)

print(f'There are {file_count} files in the directory.')

"""# Organize Files to the Same Folder"""

destination_folder = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/FullData/"

for file in image_files:
  shutil.copy(file, destination_folder)

# for file in image_files:
#   !mv "/content/drive/My Drive/your_source_folder/your_file.txt" "/content/drive/My Drive/your_destination_folder/your_file.txt"

# Specify the directory you want to search
directory = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/FullData/"

# List all entries in the directory
entries = os.listdir(directory)

# Count files (ignoring subdirectories)
file_count = sum(os.path.isfile(os.path.join(directory, entry)) for entry in entries)

print(f'There are {file_count} files in the directory.')

#Change path to where the coded files are stored in you Drive

path = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/FullData/"

imagefiles = glob.glob(path + "*.jpg")

len(imagefiles)

from sklearn.model_selection import train_test_split

"""Train splits"""

i_files = []
a_files = []
b_files = []
o_files = []

for file in imagefiles:
  classification = file.split(" ")[-1].split(".")[0]
  if classification == 'i':
    i_files.append(file)
  elif classification == 'a':
    a_files.append(file)
  elif classification == 'b':
    b_files.append(file)
  else:
    o_files.append(file)

len(i_files)

len(a_files)

len(o_files)

len(b_files)

"""Creating Large Dataset"""

image_trainL_a, image_testL_a = train_test_split(a_files, test_size=0.2, random_state=49)
image_trainL_i, image_testL_i = train_test_split(i_files, test_size=0.2, random_state=49)
image_trainL_b, image_testL_b = train_test_split(b_files, test_size=0.2, random_state=49)
image_trainL_o, image_testL_o = train_test_split(o_files, test_size=0.2, random_state=49)

print("number of infant image train data points: ", len(image_trainL_i))
print("number of infant image test data points: ", len(image_testL_i))
print("number of adult image train data points: ", len(image_trainL_a))
print("number of background image test data points: ", len(image_testL_a))
print("number of background image train data points: ", len(image_trainL_b))
print("number of background image test data points: ", len(image_testL_b))
print("number of other image train data points: ", len(image_trainL_o))
print("number of other image test data points: ", len(image_testL_o))

"""# Export Image Files Back to Drive"""

destination_folder = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/TrainLarge/i_train/"

for file in image_trainL_i:
  shutil.copy(file, destination_folder)

destination_folder = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/TestLarge/i_test/"

for file in image_testL_i:
  shutil.copy(file, destination_folder)

destination_folder = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/TrainLarge/a_train/"

for file in image_trainL_a:
  shutil.copy(file, destination_folder)

destination_folder = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/TestLarge/a_test/"

for file in image_testL_a:
  shutil.copy(file, destination_folder)

destination_folder = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/TrainLarge/b_train/"

for file in image_trainL_b:
  shutil.copy(file, destination_folder)

destination_folder = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/TestLarge/b_test/"

for file in image_testL_b:
  shutil.copy(file, destination_folder)

destination_folder = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/TrainLarge/o_train/"

for file in image_trainL_o:
  shutil.copy(file, destination_folder)

destination_folder = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/TestLarge/o_test/"

for file in image_testL_o:
  shutil.copy(file, destination_folder)

"""# Creating Small Dataset"""

import random

a_files_samples = random.sample(a_files, len(i_files))

len(a_files_samples)

b_files_samples = random.sample(b_files, len(i_files))

len(b_files_samples)

b_files_samples

"""Train and Test Split"""

image_train_a, image_test_a = train_test_split(a_files_samples, test_size=0.2, random_state=49)
image_train_i, image_test_i = train_test_split(i_files, test_size=0.2, random_state=49)
image_train_b, image_test_b = train_test_split(b_files_samples, test_size=0.2, random_state=49)

print("number of infant image train data points: ", len(image_train_i))
print("number of infant image test data points: ", len(image_test_i))
print("number of adult image train data points: ", len(image_train_a))
print("number of background image test data points: ", len(image_test_a))
print("number of background image train data points: ", len(image_train_b))
print("number of background image test data points: ", len(image_test_b))

"""# Export Small Dataset Back to Drive"""

destination_folder = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/TrainSmall/i_train/"

for file in image_train_i:
  shutil.copy(file, destination_folder)

destination_folder = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/TestSmall/i_test/"

for file in image_test_i:
  shutil.copy(file, destination_folder)

destination_folder = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/TrainSmall/a_train/"

for file in image_train_a:
  shutil.copy(file, destination_folder)

destination_folder = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/TestSmall/a_test/"

for file in image_test_a:
  shutil.copy(file, destination_folder)

destination_folder = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/TrainSmall/b_train/"

for file in image_train_b:
  shutil.copy(file, destination_folder)

destination_folder = "/content/drive/My Drive/CapstoneNewExcelFiles/ImageFiles/TestSmall/b_test/"

for file in image_test_b:
  shutil.copy(file, destination_folder)