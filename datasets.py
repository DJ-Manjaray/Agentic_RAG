import pandas as pd
import numpy as np
import json
import re
from typing import List, Dict, Any, Tuple
from openai import OpenAI
import time
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import seaborn as sns

df = pd.read_csv("hf://datasets/keivalya/MedQuad-MedicalQnADataset/medDataset_processed.csv")

## Data 1: reading the Comprehensive Medical Q&A Dataset

## Data has 16407 rows, hence we will sample 500 rows for experimentation
df_qa = df.sample(500, random_state=0).reset_index(drop=True)
print(df_qa.shape)


df_medical_device = pd.read_csv("medical_device_manuals_dataset.csv")
print(df_medical_device.shape)
## Data has 2694 rows, hence we will sample 500 rows for experimentation
df_medical_device = df_medical_device.sample(500, random_state=0).reset_index(drop=True)
print(df_medical_device.shape)


# Preparing the Dataframe for Vector DB by combining the Text
df_qa['combined_text'] = (
    "Question: " + df_qa['Question'].astype(str) + ". " +
    "Answer: " + df_qa['Answer'].astype(str) + ". " +
    "Type: " + df_qa['qtype'].astype(str) + ". "
)



# Preparing the Dataframe for Vector DB by combining the Text
df_medical_device['combined_text'] = (
    "Device Name: " + df_medical_device['Device_Name'].astype(str) + ". " +
    "Model: " + df_medical_device['Model_Number'].astype(str) + ". " +
    "Manufacturer: " + df_medical_device['Manufacturer'].astype(str) + ". " +
    "Indications: " + df_medical_device['Indications_for_Use'].astype(str) + ". " +
    "Contraindications: " + df_medical_device['Contraindications'].fillna('None').astype(str)
)
