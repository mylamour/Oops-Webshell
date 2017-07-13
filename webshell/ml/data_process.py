# coding: utf-8
# author : I

import os,re
import argparse

def read_dir(dir_path):
    path = []
    for rt, dirs, files in os.walk(dir_path):
        for f in files:
            path.append(rt+""+f)
    return path

def pre_process(dir_path,output_filepath_name):
    for input_filepath in dir_path:
        print("Now we process the file: " + input_filepath)
        try :
            write_single(input_filepath,output_filepath_name)
        except Exception as e:
            print(input_filepath + "is error")
        finally:
            pass

def write_single(input_filepath,output_filepath_name):
    res = ''
    try:
        with open(input_filepath,'r') as inputfile, open(output_filepath_name,'w') as outputfile:
            for _ in inputfile.readlines():
                res = "".join(_.split('\n'))+ res
            outputfile.writelines(res+'\n')
            return True
    except Exception as e:
        print("This File " + input_filepath + "Look Like can't read")
        return False

# how to avoid duplicated code in your project? may be i need to read fluent python
def oneline(input_filepath):
    res = ''
    try:
        with open(input_filepath,'r') as inputfile:
            for _ in inputfile.readlines():
                res = "".join(_.split('\n'))+ res
            return res
    except Exception as e:
        # It's can't be read
        return None

def clean_str(string):
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()

def load_unkown_data(data_file):

    try:
        unkown_examples = list(open(data_file, "r").readlines())
    except Exception as e:
        return False

    unkown_examples = [s.strip() for s in unkown_examples]
    x_text = [clean_str(sent) for sent in unkown_examples]
    return x_text

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("file",help="your file path")
    parser.add_argument("nfile",help="your new file path")

    args = parser.parse_args()

    if args.file and args.nfile is not None:
        write_single(args.file,args.nfile)
    elif args.file is None:
        print("Please Input your File Name With Abs Path")
    elif args.nfile is None:
        print('Please Input your New File Name With Abs Path')
    else:
        print("T_T,It's look like not professional....")


if __name__ == '__main__':
    main()
