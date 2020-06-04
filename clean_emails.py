#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 13:42:11 2020

@author: artemponomarev

email parsing...

"""
from typing import List
import glob
import pandas as pd
import time

def create_hdf_from_csv(csv_path: str, hdf_path: str):
    """
    This func is Kartik's work:
    save an h5 file from a given csv file.
    """
    df = pd.read_csv(csv_path)
    df = df[['domain', 'industry', 'size range', 'country']].\
    rename(columns={'size range': 'size_range'})
    df.to_hdf(hdf_path, key='data', mode='w', complevel=7, format='table', data_columns=['domain'])

def lookup_domains(domains: List[str], file_path: str) -> List[dict]:
    """
    This func is Kartik's work
    """
    companies = []

    for domain in domains:
        rows = pd.read_hdf(file_path, key='data', where=f"domain=='{domain}'")
        for _, row in rows.iterrows():
            companies.append({'url': domain, 'company_information':\
                              {'industry': row['industry'],\
                               'size': row['size_range'],\
                               'country': row['country']}})

    return companies
#    companies = lookup_domains(args['domain'].split(','), 'data.h5')

def extract_email_address(s):
    """
    Artem's work:
    find @ and add strings on the left and the right corresponding to emails
    """
    left = right = ''
    if '@' in s:
        position_of_at = s.index('@')
        if position_of_at > 0:
            left = s[0 : position_of_at+1]

        idx = 0
#        if "\'" in left:
#            idx = left.rfind("\'")

        idx1 = 0
        if " " in left:
            idx1 = left.rfind(" ")
            
#        if idx or idx1:
        left = left[max(idx, idx1)+1 :]

        right = s[position_of_at+1 :]

        idx = len(right)
        if "\'" in right:
            idx = right.index("\'")

        idx1 = len(right)
        if ":" in right:
            idx1 = right.index(":")

        right = right[:min(idx, idx1)]
        domain = right

        return (domain, left+right)
    else:
        return (None, None)

def extract_domain(e):
    """
    look for domain after @
    """
    if e:
        start = e.index('@')+1
        return e[start:]
    else:
        return None

def clean_emails(entries_per_co):
    """
    filter emails per instructions
    """
    print('Start...')
    files = glob.glob('/Users/artemponomarev/Desktop/Projects/Nikon/LinkedIn_Kk82Nh/x*')
    for file in files:
        try:
            print('\ninput file = ', file)
            print('\nloading good domains to keep...\n')
            file_path = '/Users/artemponomarev/Desktop/Projects/Nikon/top-1m.csv'
            included_domains = None
            with open(file_path, 'rb') as f:
                reader = pd.read_csv(f)
                f.close()
                print('\ncsv reader = \n', len(reader), reader)
                included_domains = reader.iloc[:, 1:2]
                # Python does not slice inclusive of the ending index
            included_domains_arr = included_domains.to_numpy().flatten()
            print('\nincluded domains = \n', len(included_domains_arr),\
                  included_domains_arr, included_domains_arr.shape)

            print('\nloading exlcuded domains...\n')
            file_path =\
'/Users/artemponomarev/Desktop/Projects/Nikon/LinkedIn_Kk82Nh/excluded_email_providers_list.txt'
            excluded_domains = None
            with open(file_path, 'r') as f1:
                excluded_domains = f1.read()
                f1.close()
            print('\nexcluded domains = \n', excluded_domains[:100])

            print('\nwait for a long time...\n')
            selected_domains = [d for d in included_domains_arr if d not in excluded_domains]

            nlines = 0
            file_path = file
            with open(file_path, 'r') as f2:
                nlines = sum(1 for _ in f2)
                f2.close()
            print('\nnumber of lines in the file:', nlines)
            nl = 0
            list1 = []
            with open(file_path, 'r') as f3:
                for line in f3:
                    nl += 1
                    if nl%10000 == 0:
                        print('raw data progress: %', 100.0*nl/nlines)
                    if line:
                        (domain, email) = extract_email_address(line)
                        if (domain, email) != (None, None):
                            print(line)
                            time.sleep(60)
                            list1.append((domain, email))
                print('\nclosing input file...')
                f3.close()
            print('raw data progress final: %', 100.0*nl/nlines)

            print('\nwait for a long time...\n')
            list1 = sorted(list1)
            print('raw domains sorted = ', list1[:10])
            print('\nwait for a long time...\n')
            selected_domains = sorted(selected_domains)
            print('selected_domains sorted = ', selected_domains[:10])

            print('\n\npurging bad domains ...\n')
            print('purging bad domains progress: %', 0.0)
            list_ = []
            old_dom = new_dom = None
            length = len(list1)
            l = 0
            good_dom = False
            for i in range(length):
                l += 1
                if l%100000 == 0:
                    print('purging bad domains progress: %', 100.0*l/length)
                new_dom = list1[i][0].lower()
                if new_dom != old_dom:
                    good_dom = False
                    old_dom = new_dom
        #            print("\nHERE", new_dom, selected_domains[0], new_dom < selected_domains[0])
                    if new_dom == selected_domains[0]:
        #                print('\nHERE1 selected_domains = ', new_dom, selected_domains[0],\
        #                      new_dom == selected_domains[0], selected_domains[:10])
                        good_dom = True
                        list_.append(list1[i])
                        selected_domains.pop(0)
                        if not selected_domains:
                            break
                    elif new_dom > selected_domains[0]:
                        while new_dom > selected_domains[0]:
                            selected_domains.pop(0)
                            if not selected_domains:
                                break
                        if not selected_domains:
                            break
#                print("\nHERE2", new_dom, selected_domains[0], new_dom > selected_domains[0])
#                print('HERE2a selected_domains = ', selected_domains[:10])
                        if new_dom == selected_domains[0]:
                            good_dom = True
                            list_.append(list1[i])
                            selected_domains.pop(0)
        #                    print('\nHERE3 selected_domains = ', selected_domains[:10])
                            if not selected_domains:
                                break
                else:
                    if good_dom:
                        list_.append(list1[i])
            print('purging bad domains progress: %', 100.0*l/length)

            print('\naggregating emails in given domains...\n')
            nlines = len(list_)
            dict_ = {}
            nl = 0
            print('aggregating emails in given domains progress: %', 0.0)
            for domain, email in list_:
                nl += 1
                if nl%10000 == 0:
                    print('aggregating emails in given domains progress: %', 100.0*nl/nlines)
                dict_.setdefault(domain, []).append(email)
            print('aggregating emails in domains progress: %', 100.0)

            print('\npurging long lists of emails in all domains...\n')
            nlines = len(dict_)
            nl = 0
            print('purging long lists of emails in all domains progress: %', 0.0)
            for domain, emails in dict_.items():
                nl += 1
                if nl%10000 == 0:
                    print('purging long lists of emails in all domains progress: %',\
                          100.0*nl/nlines)
                if len(emails) >= entries_per_co:
                    dict_[domain] = emails[:entries_per_co]
            print('purging long lists of emails in all domains progress: %', 100.0)

            print('\nwriting .csv file ... \n')
            nlines = len(dict_)
            nl = 0
            print(file+'.csv')
            with open(file+'.csv', 'w') as f_out:
                f_out.close()
            with open(file+'.csv', 'a') as f_out1:
                for key in sorted(dict_.keys()):
                    nl += 1
                    if nl%100 == 0:
                        print('writing .csv file progress: %', 100.0*nl/nlines)
                    string = key+','+','.join(dict_[key])+'\n'
                    f_out1.write(string)
                f_out1.close()
            print('writing .csv file progress: %', 100.0)

            string = ''
            for key in sorted(dict_.keys()):
                string += (key+','+','.join(dict_[key])+'\n')
            with open(file+'.txt', "wb") as f4:
                f4.write(string.encode("utf-8"))
            with open(file+'.txt', "rb") as f5:
                str_to_save_to = f5.read().decode("utf-8")
            print('\n\ntext file = ', str_to_save_to[:10])

            df = pd.read_csv(file+'.csv', names=range(11), engine="python")
            print('\n\ndf=\n', df.iloc[:10])

            print('\nwriting .h5 file...\n')
            print('\n\ndf=\n', df.iloc[:10])
            df.to_hdf(file+'.h5', key='data', complevel=7)

            df2 = pd.read_hdf(file+'.h5')
            print('\n\ndf2=\n', df2.iloc[:10])

        #    try:
        #        print('\nwriting .xlsx file ...\n')
        #        #Load dict directly to a Dataframe without loops
        #        df = pd.DataFrame.from_dict(dict_, orient='index')
        #        #Unstack, drop na and sort if you need.
        #        df.unstack().dropna().sort_index(level=1)
        #        print(df)
        #        with pd.ExcelWriter('clean_email_list.xlsx') as writer: #pylint: disable=abstract-class-instantiated
        #            df.to_excel(writer)
        #    except Exception:
        #        print('\nexcel spreadsheet was not written...\n')

            print('\n', len(dict_), ' is the number of domains in the clean email list...\n')
            print('done...')
        except Exception:
            with open('errors.txt', 'a') as err_f:
                err_f.write('\n\nfile %s was not processed corretly...' % file)

clean_emails(10)
