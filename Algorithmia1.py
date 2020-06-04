#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 07:01:42 2020

@author: artemponomarev
"""

import Algorithmia
#import pandas as pd
#import sys
import pickle
#import csv
#import numpy as np

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

def extract_email_address(s, excluded):
    left=right=''
    if '@' in s:
        position_of_at=s.index('@')
        if position_of_at>0:
            left=s[0 : position_of_at+1]
            
        idx=0
        if "\'" in left:
            idx=left.lastindexof("\'")
            left=left[idx :]
        
        right=s[position_of_at+1 :]
        idx=len(right)
        if ":" in right:
            idx=right.index(":")
            right=right[:idx]  
        
        if excluded==None:
            return left+right
        else:
            if right in excluded:
                return None
            else:
                return left+right
    else:
        return None

def apply(input):
    result=[]
# Open file and load model
# prediction = model.predict(np_data) # future model execution
#return list(prediction)

#    file_path = 'data://artemAlgo/email_addresses/excluded_email_providers_list.txt'
#    algorithmia_path = client.file(file_path).getFile().name
#    excluded=None
#    with open(algorithmia_path, 'r') as f:
#        excluded = f.read().split("\n")
        
    count=0
    emails=[]
    file_path = ['data://artemAlgo/email_addresses/clean_email_list-2.csv']
    for fp in file_path:
        algorithmia_path = client.file(fp).getFile().name
        with open(algorithmia_path, 'r') as f1:
            lines=f1.readlines()
            for l in lines:
                if input == l[l.index('@')+1:-1]:
                    emails.append(l[1:-1])
                    count+=1
                    if count>=10:
                        break
    result=emails
    return result