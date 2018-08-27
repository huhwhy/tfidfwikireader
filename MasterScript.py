#!/bin/python
import pywikibot
import time
import re
import os, glob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.decomposition import PCA
import numpy as np
import scipy.sparse
import fnmatch
import pickle
from sklearn import preprocessing
import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib import style
from mpl_toolkits.mplot3d import Axes3D
from sklearn import manifold
import cPickle as pickle

def pywiki(article,text):
    wiki = list(pywikibot.Page(pywikibot.Site('en', 'wikipedia'),article).revisions(content=True))      
    currentwiki = pywikibot.Page(pywikibot.Site('en', 'wikipedia'),article).latest_revision_id

     #for i in wiki :    
    for x in range(len(wiki)): #-1 after wiki when doing subsampling
   #    if x % 20 in (17,18,19,20):
    #              continue
       files = open(text % x,'w')
       files.write(str(wiki[x]))
       files.close()
       
    
    return article, len(wiki)



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
    
    
    h = []
    for i in sorted(configfiles):
       f = open(i ,'r')
       g = f.readlines()
       h.append(g[0])    

        # each instance of g in the for loop gets appended to the list

    engstop = ENGLISH_STOP_WORDS

    count = CountVectorizer(stop_words=engstop)
   
    fitted = count.fit(h)

    freq_term_matrix = fitted.transform(h)

    tf = TfidfVectorizer()

    tfm = tf.fit_transform(h)

    file_name = "tfidf.binary"
    file_Object = open(file_name, "w")
    pickle.dump(tfm,file_Object)
    file_Object.close()

    tfm = tfm.todense()

    return tfm
     # make sure to specfiy which presidents are for which tfidf value, download each prez to a diff folder

def Isomap(tfidf):
  iso = manifold.Isomap(n_neighbors=8, n_components=3)
  john = iso.fit_transform(tfidf)
   
  np.savetxt('iso3d.csv', john, delimiter=',', fmt="%6f")

  return john
def pca(tfidf):
  pca = PCA(n_components=3)
  k = pca.fit_transform(tfidf)
 
  return k
  
def plot_isomap(isocoord, idx_list, artname, numclass):

  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  
  colorlist = ['r', 'g', 'b', 'k']
  for i in range(numclass):
      sel_idx = idx_list == i
      
      ax.scatter(isocoord[sel_idx, 0], isocoord[sel_idx, 1], isocoord[sel_idx, 2], \
                 color=colorlist[i], edgecolor="None", label=artname[i])

  plt.savefig('isomap3d.png')
  return

def plot_PCA(pcacoord, idx_list, artname, numclass):
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')

  colorlist = ['r', 'g', 'b', 'k']
  for i in range(numclass):
      sel_idx = idx_list == i

      ax.scatter(pcacoord[sel_idx, 0], pcacoord[sel_idx, 1], pcacoord[sel_idx, 2], \
                 color=colorlist[i], edgecolor="None", label=artname[i])

  plt.savefig('PCA3d.png')
  return



if __name__ == '__main__':

   artname = []
   temp =  pywiki('Southeast Indian Ridge','txtfiles/SEIR%05d.txt') #include presidents here
   print temp
   idx_list = np.zeros((temp[1], 1))
   artname.append(temp[0])

   temp2 = pywiki('Southwest Indian Ridge','txtfiles/SWIR%05d.txt')
   print temp2
   idx_list = np.vstack((idx_list, np.ones((temp2[1], 1)))) 
   artname.append(temp2[0])


   temp3 = pywiki('Central Indian Ridge', 'txtfiles/CIR%05d.txt')
   print temp3
   idx_list = np.vstack((idx_list, 2 * np.ones((temp3[1], 1)) )) 
   artname.append(temp3[0])


   temp4 = pywiki('Mongolian Plateau', 'txtfiles/MP%05d.txt')
   print temp4
   idx_list = np.vstack((idx_list, 3 * np.ones((temp4[1], 1)) )) 
   artname.append(temp4[0])


   num_class = int( np.max(idx_list) + 1)
   idx_list = idx_list.reshape((idx_list.shape[0]))

   Main('txtfiles') #directory as parameter
   tfidfmat = tfidf('txtfiles')#directory as parameter
   iso_coord = Isomap(tfidfmat)
   pca_coord = pca(tfidfmat)
   plot_isomap(iso_coord, idx_list, artname, num_class)
   plot_PCA(pca_coord, idx_list, artname, num_class) 
