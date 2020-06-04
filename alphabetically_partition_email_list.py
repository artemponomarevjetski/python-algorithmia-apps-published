#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 10:21:25 2020

@author: artemponomarev
"""

import glob
import time
import pandas as pd
import numpy as np

def clean_emails(entries_per_co):
    """
    partition long email list into smaller chunks: aaa.csv, aab.csv, ... zzz.csv for faster look-up
    """
    print('Start...')
    with open('errors.txt', 'w') as err_f:
        err_f.close()
    with open('combined.csv', 'w') as f_out:
        f_out.close()
    files = glob.glob('/Users/artemponomarev/Desktop/Projects/Nikon/LinkedIn_Kk82Nh/x*.csv')
    print('input files = ', files)
    for file in files:
        try:
            print('\ninput file = ', file)
            df = pd.read_csv(file, names=range(11), engine="python")
            print('\n\ndf=\n', df.iloc[:10])

            print('\nwait for a long time...\n')
#            print('\nconvert domains and emails to low case...\n')
#            for columns in df.columns:
#                print(columns, df.columns)
#                df[columns] = df[columns].str.lower()
            print('\nsort domains ...\n')
            df1 = df.sort_values(by=[0], ascending=[True])
            print('domains sorted = ', df1.iloc[10:100])

            print('\naggregating emails in given domains...\n')
            dict_ = {}
            length = len(df1)
            print('dataframe length = ', length)
            l = 0
            print('aggregating emails in given domains progress: %', 0.0)
            for row in df1.iterrows():
                if row:
                    l += 1
                    if l%100000 == 0:
                        print('aggregating emails in given domains progress: %', 100.0*l/length)
                    domain = row[1][0]
                    temp = []
                    for i in range(10):
                        if row[1][i+1] and row[1][i+1] is not np.nan and row[1][i+1] == row[1][i+1]:
                            temp.append(row[1][i+1].lower())
                    dict_.setdefault(domain.lower(), []).append(temp)
            dict1 = {}
            for key in dict_.keys():
                dict1[key] = sum(dict_[key], [])
            print('aggregating emails in domains progress: %', 100.0)
            print('\npurging long lists of emails in all domains...\n')

            nlines = len(dict1)
            nl = 0
            print('purging long lists of emails in all domains progress: %', 0.0)
            for domain, emails in dict1.items():
                nl += 1
                if nl%10000 == 0:
                    print('purging long lists of emails in all domains progress: %',\
                          100.0*nl/nlines)
                if len(emails) >= entries_per_co:
                    dict1[domain] = emails[:entries_per_co]
            print('purging long lists of emails in all domains progress: %', 100.0)

            print('\nwriting combined .csv file ... \n')
            nlines = len(dict1)
            print(nlines)
            nl = 0
            with open('combined.csv', 'a') as f_out1:
                for key in sorted(dict1.keys()):
                    nl += 1
                    if nl%100 == 0:
                        print('writing .csv file progress: %', 100.0*nl/nlines)
                    string = key+','+','.join(dict1[key])+'\n'
                    f_out1.write(string)
                f_out1.close()
            print('writing .csv file progress: %', 100.0)

        except Exception:
            print("HERE")
            time.sleep(60)
            with open('errors.txt', 'a') as err_f:
                err_f.write('\n\nfile %s was not processed corretly...' % file)

    df = pd.read_csv('combined.csv', names=range(11), engine="python")
    print('\n\ndf=\n', df.iloc[:10])

    print('\nwriting .h5 file...\n')
    print('\n\ndf=\n', df.iloc[:10])
    df.to_hdf('combined.h5', key='data', complevel=7)

    df2 = pd.read_hdf('combined.h5')
    print('\n\ndf2=\n', df2.iloc[:10])

    print('\n', len(dict_), ' is the number of domains in the clean email list...\n')
    print('done...')

clean_emails(10)
