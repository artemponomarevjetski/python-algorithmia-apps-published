emails = ['John.Smith@google.com', 
          'John_Smith@google.com', 
          'John-Smith@google.com',
          'JohnSmith123@google.com',
          'johnsmith@google.com',
          'Johnsmith123@google.com',
          'jsmith@google.com',
          'jsmith123@google.com',
          'johns@google.com',
          'john@google.com',
          'john123@google.com'
          'js@google.com',
          'johnsmith123@google.com']

first_names=['John', 'Nancy', 'Lori', 'Susan', 'Susanne', 'Mark']
first_names_lowcase=list(map(lambda x:x.lower(), first_names))
last_names=['Smith', 'Johnson', 'Jackson']
last_names_lowcase=list(map(lambda x:x.lower(), last_names))

def is_common_name(s,list_):
    if s in list_:
        return True
    else:
        return False  
    
def has_common_name_part(s, list_):
    for string in list_:
        if string in s:
            return string
    return None

for email in emails:
    s=email[:email.index('@')]
    chunks=[]
    for c in s:
        if c.isupper():
            chunks.append(c)
        elif c=='.' or c=='_' or c=='-':
            chunks.append(c)
        elif c.isdigit():
            if chunks:
                tmp=chunks.pop()
                if tmp[-1].isdigit():
                    chunks.append(tmp+c)
                else:
                    chunks.append(tmp)
                    chunks.append(c)
            else:
                chunks.append(c)
        else:
            if chunks:
                tmp=chunks.pop()
                if is_common_name(tmp, first_names) or\
                is_common_name(tmp, first_names_lowcase) or\
                is_common_name(tmp, last_names) or\
                is_common_name(tmp, last_names_lowcase):
                    chunks.append(tmp)
                    chunks.append(c)
                else:
                    if has_common_name_part(tmp, first_names):
                        tmp1=has_common_name_part(tmp, first_names)
                        chunks.append(tmp[:-len(tmp1)])
                        chunks.append(tmp1)
                    elif has_common_name_part(tmp, first_names_lowcase):
                        tmp1=has_common_name_part(tmp, first_names_lowcase)
                        chunks.append(tmp[:-len(tmp1)])
                        chunks.append(tmp1)
                    elif has_common_name_part(tmp, last_names):
                        tmp1=has_common_name_part(tmp, last_names)
                        chunks.append(tmp[:-len(tmp1)])
                        chunks.append(tmp1)
                    elif has_common_name_part(tmp, last_names_lowcase):
                        tmp1=has_common_name_part(tmp, last_names_lowcase)
                        chunks.append(tmp[:-len(tmp1)])
                        chunks.append(tmp1)
                    else:
                        chunks.append(tmp+c)
            else:
                chunks.append(c)
    if chunks:
        tmp=chunks.pop()
        if has_common_name_part(tmp, first_names):
            tmp1=has_common_name_part(tmp, first_names)
            if tmp[:-len(tmp1)]:
                chunks.append(tmp[:-len(tmp1)])
                chunks.append(tmp1)
            else:
                chunks.append(tmp)
        elif has_common_name_part(tmp, first_names_lowcase):
            tmp1=has_common_name_part(tmp, first_names_lowcase)
            if tmp[:-len(tmp1)]:
                chunks.append(tmp[:-len(tmp1)])
                chunks.append(tmp1)
            else:
                chunks.append(tmp)
        elif has_common_name_part(tmp, last_names):
            tmp1=has_common_name_part(tmp, last_names)
            if tmp[:-len(tmp1)]:
                chunks.append(tmp[:-len(tmp1)])
                chunks.append(tmp1)
            else:
                chunks.append(tmp)
        elif has_common_name_part(tmp, last_names_lowcase):
            tmp1=has_common_name_part(tmp, last_names_lowcase)
            if tmp[:-len(tmp1)]:
                chunks.append(tmp[:-len(tmp1)])
                chunks.append(tmp1)
            else:
                chunks.append(tmp)
        else:
            chunks.append(tmp)
          
    print(chunks, email)
