#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 15:08:41 2020

@author: artemponomarev
"""

import Algorithmia
import json
import pandas as pd
#import sys
#import pickle
#import csv
import numpy as np

#from sklearn.datasets import load_boston
#from sklearn.ensemble import RandomForestRegressor

client = Algorithmia.client()

def load_model(): # future model
    # Get file by name
    # Open file and load model
    file_path = 'data://YOUR_USERNAME/scikit_learn_demo/scikit-demo-boston-regression.pkl'
    model_path = client.file(file_path).getFile().name
    # Open file and load model
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
        return model

# Load model outside of the apply function so it only gets loaded once
# model = load_model() # future model initialization

def apply(input):
# Open file and load model
# prediction = model.predict(np_data) # future model execution
#return list(prediction)

#    file_path = 'data://artemAlgo/email_addresses/excluded_email_providers_list.txt'
#    algorithmia_path = client.file(file_path).getFile().name
#    excluded=None
#    with open(algorithmia_path, 'r') as f:
#        excluded = f.read().split("\n")
        
    domains=input.strip().replace(" ", "").split(',')
    emails=[]
    h5=True
    file_path = []
    algorithmia_path = None
    
    if h5:
   #     algorithmia_path1 = client.file('data://artemAlgo/email_addresses/filelist.txt').getFile().name
  #      with open(algorithmia_path1) as fl:
   #         for l in fl:
 #               file_path.append('data://artemAlgo/email_addresses/'+l[:-1]+'.h5')
    #        fl.close()
        file_path.append('data://artemAlgo/email_addresses/combined.h5')
    else:
        file_path = ['data://artemAlgo/email_addresses/clean_email_list.csv']
    #,'data://artemAlgo/email_addresses/clean_email_list1.csv']

    for d in domains:
        count=0
        for fp in file_path:
            try:
                algorithmia_path = client.file(fp).getFile().name
                if h5:
                    df = pd.read_hdf(algorithmia_path)
                    for row in df.iterrows():
                        dom=row[1][0]
                        if d == dom.lower(): 
                            for i in range(10):
                                if row[1][i+1] and row[1][i+1] is not np.nan and row[1][i+1]==row[1][i+1]:
                                    emails.append({'email':(row[1][i+1]).lower(), 'link':d})
                                    count+=1 # this accumulates per domain
                                if count>=10:
                                    break # from emails in a line
                            if count>=10:
                                break # from lines in a file loop
                else:
                    with open(algorithmia_path, 'r') as f:
                        lines=f.readlines()
                        for line in lines:
                            l=line.split(',')
                            if d == l[0]:  
                                for string in l[1:]:
                                    e=string.lower()
                                    emails.append({'email':string.lower(), 'link':d})
                                    count+=1 # this accumulates per domain
                                    if count>=10:
                                        break # from emails in a line
                            if count>=10:
                                break # from lines in a file loop
                        f.close()
                if count>=10: 
                    break # from file loop
            except Exception:
                pass
    result=[]
    result = json.dumps(emails, sort_keys=True)
    return result