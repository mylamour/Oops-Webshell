#!/usr/bin/env python
#coding=utf-8
#  Change from "https://github.com/dennybritz/cnn-text-classification-tf/blob/master/eval.py
#  Apply it to predict webshell or not 
#  Useage:
#         ./aeval.py --eval_train --checkpoint_dir="./runs/1499142849/checkpoints/" --unknown_file="./data/test/unknown0"  

import numpy as np
import os,re
import time
import datetime
from .data_helpers import load_data_and_labels,batch_iter
from .data_process import load_unkown_data,write_single
import tensorflow as tf
from tensorflow.contrib import learn
import csv

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

# Data Parameters
tf.flags.DEFINE_string("unknown_file", "", "Data source for the positive data.")

# Eval Parameters
tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
tf.flags.DEFINE_string("checkpoint_dir", "", "Checkpoint directory from training run")
tf.flags.DEFINE_boolean("eval_train", False, "Evaluate on all training data")

# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")


FLAGS = tf.flags.FLAGS
FLAGS._parse_flags()


def predict_webshell(x_test,m_checkpoint_dir):
    checkpoint_file = tf.train.latest_checkpoint(m_checkpoint_dir)
    graph = tf.Graph()
    with graph.as_default():
        session_conf = tf.ConfigProto(
          allow_soft_placement=FLAGS.allow_soft_placement,
          log_device_placement=FLAGS.log_device_placement)
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            # Load the saved meta graph and restore variables
            saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
            saver.restore(sess, checkpoint_file)

            # Get the placeholders from the graph by name
            input_x = graph.get_operation_by_name("input_x").outputs[0]
            # input_y = graph.get_operation_by_name("input_y").outputs[0]
            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

            # Tensors we want to evaluate
            predictions = graph.get_operation_by_name("output/predictions").outputs[0]

            # Generate batches for one epoch
            batches = batch_iter(list(x_test), FLAGS.batch_size, 1, shuffle=False)

            # Collect the predictions here
            all_predictions = []

            for x_test_batch in batches:
                batch_predictions = sess.run(predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
                all_predictions = np.concatenate([all_predictions, batch_predictions])
    return all_predictions

def read_and_predict(m_unknown_file,m_checkpoint_dir):
    """
        如果不进行oneline处理，会导致耗时非常之长，以及内存耗尽。
    """
    write_single(m_unknown_file,'/tmp/tmp.test')           #if not, 59.72s vs 2.97s 
    x_raw = load_unkown_data('/tmp/tmp.test')
    y_test = None

    results_human_read = {}

    if x_raw is False or len(x_raw) == 0:               # 不能读取，或者读取为空
        results_human_read = {'file':m_unknown_file,'file_type':'Can\'t Read'}
        return results_human_read
    else:

        # x_raw = data_process.load_unkown_data(m_unknown_file)             # 注意：使用predect.sh时uncomment this line，并且修改增加打印提示
        
        file_path=os.path.split(m_unknown_file)[0]
        file_name=os.path.split(m_unknown_file)[1]

        # Map data into vocabulary
        vocab_path = os.path.join(m_checkpoint_dir, "..", "vocab")
        vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
        x_test = np.array(list(vocab_processor.transform(x_raw)))

        results = predict_webshell(x_test,m_checkpoint_dir)
        for result in results:
            if result == 0 :
                file_type = 'Dangerous'
                # print(bcolors.FAIL+": Look Like  Dangerous" + bcolors.ENDC)
            elif result == 1 :
                file_type = 'Safe'
                # print(bcolors.OKGREEN + ":  Look Like Safe" + bcolors.ENDC)
            else:
                return None
        results_human_read = {'file_type': file_type, 'file_name': file_name,
                              'detect_method': 'Machine Learning', 'platform': 'Linux', 'description': "webshell文件或疑似webshell文件"}
        return results_human_read

def read_and_predict_dir(m_dir,m_checkpoint_dir):
    res = []
    for p,d,f in os.walk(m_dir):
        for item in f:
            res.append(read_and_predict(os.path.join(p,item),m_checkpoint_dir))
    return res

def test():
    # 其实吧，每次预测一个文件都要启动tfsession导致挺慢的，批量预测时，还是用predict.sh来的方便吧。
    s = read_and_predict(FLAGS.unknown_file,FLAGS.checkpoint_dir)
    
    print(s)

if __name__ == '__main__':
    test()
    

# # Save the evaluation to a csv
# predictions_human_readable = np.column_stack((np.array(x_raw), all_predictions))
# out_path = os.path.join(FLAGS.checkpoint_dir, "..", "prediction.csv")
# print("Saving Predict Result to {0}".format(out_path))
# with open(out_path, 'a') as f:
#     csv.writer(f).writerows(predictions_human_readable)
