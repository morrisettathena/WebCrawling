"""
Taken from tutorial here:
https://medium.com/analytics-vidhya/topic-modeling-using-gensim-lda-in-python-48eaa2344920
"""

import re
import numpy as np
import pandas as  pd
from pprint import pprint# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel# spaCy for preprocessing
import spacy# Plotting tools
import pyLDAvis
import pyLDAvis.gensim
import matplotlib.pyplot as plt

file_path = "./enr-processed.jsonl"

jsonObj = pd.read_json(file_path, lines=True)
print(jsonObj.head())
print(jsonObj.columns)
print(jsonObj.shape)