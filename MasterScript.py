#!/bin/python
import pywikibot
import time
import re
import os, glob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import numpy as np
import fnmatch



def pywiki(article,text):
    wiki = list(pywikibot.Page(pywikibot.Site('en', 'wikipedia'),article).revisions(content=True))      
    currentwiki = pywikibot.Page(pywikibot.Site('en', 'wikipedia'),article).latest_revision_id

    
    x = 0
    
    #for i in wiki :    
    for x in range(len(wiki)):
       files = open(text % x,'w')
       files.write(str(wiki[x]))
       files.close()
       if wiki[x] == currentwiki:
           break
      

    files.close()




def iteratively_all_files(path):
    """ tiny generator to return all files in a directory recursively """
    for basedir, dirs, files in  os.walk(path):
        #print(basedir)
        for fname in files:
            yield os.path.join(basedir, fname)

def remove_special_chars_in_file(fname):
    """ remove certain characters in a file 
        This script is very basic it assues, that
        the encire contents of a file fits into memory 
        and that interrupting the script may corrupt the source file
        without an eas recovery option (no backups are made)
    """
    
    with open(fname, 'rb') as fin:
        lines = fin.readlines()

        

    to_remove = re.compile('[' + re.escape(r'@/\[]<>*-_.|:(){}="",#&$1234567890?') + ']+')
    
    
    
    with open(fname, 'wb') as fout:
        for line in lines:
            fixed_line = re.sub(to_remove, '', line)
            fixed = fixed_line.replace('\n', '') 
             #if fixed_line != line:
            #    print("--%r\n++%r" % (line, fixed_line))
            
            fout.write(fixed)
            
            

def Main(YOUR_PATH):
    for fname in iteratively_all_files(YOUR_PATH):
         remove_special_chars_in_file(fname)
def tfidf(path):
    configfiles = [os.path.join(dirpath, f)
       for dirpath, dirnames, files in os.walk(path)
       for f in fnmatch.filter(files, '*.txt')]
    
    print configfiles 
    
    h = []
    for i in configfiles:
       f = open(i ,'r')
       g = f.readlines()
       print g
       h.append(g[0]) # each instance of g in the for loop gets appended to the list


    engstop = ENGLISH_STOP_WORDS

    count = CountVectorizer(stop_words=engstop)
   
    fitted = count.fit(h)

    freq_term_matrix = fitted.transform(h)
    print freq_term_matrix

    tfidf = TfidfTransformer(norm="l2")

    tf = TfidfVectorizer()

    tfm = tf.fit_transform(h)
     
    
   
    return np.savetxt('tfidf.txt',tfm.todense(),delimiter=',')



if __name__ == '__main__':
   pywiki('blank',' blank%i.txt') #include presidents here
   Main('home/blank/blank') #directory as parameter
   tfidf('home/blank/blank')#directory as parameter
