"""
Author: Leon Yin, Surya Mattu

These are functions that help clean up and extract data
from mbox files from Google takeout.

They are used in:
notebooks/1-data-preprocessing.ipynb
"""


import re
from urlexpander import get_domain
import hashlib
from bs4 import BeautifulSoup

def find_email(x, pat=r'(?<=\<).+?(?=\>)'):
    """Strips emails from messy strings"""
    hits =  re.findall(pat, str(x))
    if hits:
        return hits[0].lower()
    else:
        return x
    
def find_name(x):
    """Strips name from an Email header"""
    email= find_email(x)
    x = x.replace(email, '')
    x = re.sub('[!@#$<>"]', '', x)
    return x.strip()

def find_tld_from_email(x):
    # isolates the website
    x = x.split('@')[-1]
    
    # gets tld
    if x:
        x = get_domain(x)
    return x

def is_primary(row : dict):
    """
    Determines if a row is in the Primary inbox. 
    These are emails that are in the Inbox, 
    but aren't in Spam, Promotions, or Trash. 
    """
    try:
        if (
           not row.get('Spam') and 
           not row.get('Category Promotions') and
           not row.get('Trash') and
           row['Inbox']
        ):
            return 1
    except Exception as e:
        print(e)
        print(row)
    return 0

def get_email_id(row):
    """
    Creates a unique identifier for each email based on the 
    date received and a header ID
    """
    text = row['X-GM-THRID'] + str(row['Date'])
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def create_category_id(row):
    """
    Creates a unique identifier for each email sender, 
    uses our email alias and the newsletter category.
    This is only needed because of the House signup mishap.
    """
    return hashlib.md5((
        row['To_Email'] + row['Category']
    ).encode('utf-8')).hexdigest()

def get_text(_message):
    """Returns the text of an email"""
    data = {
        'text' : None,
        'script' : None,
        'style' : None 
    }
    
    if _message.is_multipart():
        content = [part.get_payload(decode=True) for part in _message.get_payload()]
        d = []
        for sent in content:
            if sent:
                try:
                    d.append(sent.decode())
                except:
                    pass
        content = ''.join(d)
        
    else:
        content = _message.get_payload(decode=True).decode()
    
    if content:    
        soup = BeautifulSoup(content, 'lxml')

        # kill all script and style elements
        for _type in ['script','style']:
            for script in soup([_type]):
                data['script'] = script
                script.decompose()    # rip it out

        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        data['text'] = '\n'.join(chunk for chunk in chunks if chunk)
    
    return data