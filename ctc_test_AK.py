# Function script created by Adam Kahana, but borrowed heavily from existing code
# written by Calvo-Zaragoza and Rizo.

# Calling the function in Command Line:
# python ctc_test_AK.py -corpus ./Corpus/ -set Data/test.txt -model <PATH_TO_OUR_MODEL> -vocabulary Data/vocabulary_agnostic.txt


#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import argparse
import tensorflow as tf
from primus_AK import CTC_PriMuS
import ctc_utils_AK
import ctc_model_AK
import cv2
import numpy as np

parser = argparse.ArgumentParser(description='Test a trained model (CTC).')
# parser.add_argument('-image',  dest='image', type=str, required=True, help='Path to the input image.')
parser.add_argument('-corpus', dest='corpus', type=str, required=True, help='Path to the corpus.')
parser.add_argument('-set',  dest='set', type=str, required=True, help='Path to the test set file.')
parser.add_argument('-model', dest='model', type=str, required=True, help='Path to the trained model.')
parser.add_argument('-vocabulary', dest='voc_file', type=str, required=True, help='Path to the vocabulary file.')
parser.add_argument('-semantic', dest='semantic', action="store_true", default=False)
args = parser.parse_args()

tf.reset_default_graph()
sess = tf.InteractiveSession()

# Read the dictionary
dict_file = open(args.voc_file,'r')
dict_list = dict_file.read().splitlines()
int2word = dict()
for word in dict_list:
    word_idx = len(int2word)
    int2word[word_idx] = word
dict_file.close()

# Restore weights
saver = tf.train.import_meta_graph(args.model)
saver.restore(sess,args.model[:-5])

graph = tf.get_default_graph()

inputs = graph.get_tensor_by_name("model_input:0")
seq_len = graph.get_tensor_by_name("seq_lengths:0")
rnn_keep_prob = graph.get_tensor_by_name("keep_prob:0")
height_tensor = graph.get_tensor_by_name("input_height:0")
width_reduction_tensor = graph.get_tensor_by_name("width_reduction:0")
logits = tf.get_collection("logits")[0]
decoded, _ = tf.nn.ctc_greedy_decoder(logits, seq_len)

# Constants that are saved inside the model itself
WIDTH_REDUCTION, HEIGHT = sess.run([width_reduction_tensor, height_tensor])

# Load the Primus dataset.
primus = CTC_PriMuS(args.corpus,args.set,args.voc_file, args.semantic, val_split = 0)

img_height = 128
params = ctc_model_AK.default_model_params(img_height,primus.vocabulary_size)
# params['batch_size'] = 1

test_ed = 0
test_len = 0
test_count = 0
test_idx = 0
while test_idx < len(primus.training_list):   
    print(test_idx)
    
    batch = primus.nextBatch(params)
    
    prediction = sess.run(decoded,
                             feed_dict={
                                 inputs: batch['inputs'],
                                 seq_len: batch['seq_lengths'],
                                 rnn_keep_prob: 1.0,
                             })
    
    str_predictions = ctc_utils_AK.sparse_tensor_to_strs(prediction)

    
    for i in range(len(str_predictions)):
        ed = ctc_utils_AK.edit_distance(str_predictions[i], batch['targets'][i])
        test_ed = test_ed + ed
        test_len = test_len + len(batch['targets'][i])
        test_count = test_count + 1
        
    test_idx = test_idx + params['batch_size']
    
print (str(1. * test_ed / test_count) + ' (' + str(100. * test_ed / test_len) + ' SER) from ' + str(test_count) + ' samples.')        


