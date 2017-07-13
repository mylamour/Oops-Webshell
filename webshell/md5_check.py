# coding: utf-8
# author: I
# attation: if you want use patch from gevent ,you need ASAP 
from gevent import monkey,pool 
monkey.patch_all()
from multiprocessing import Process


import hashlib
import os 
import argparse

from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table,Column,Integer,String, ForeignKey


def insert_to_sqlitedb(tablename,metadata,filename,filemd5): 
    opreator_table = Table(tablename, metadata, autoload=True)
    insert =  opreator_table.insert()
    insert.execute(filename=filename, filemd5=filemd5)

def md5(file_full_path):
    return hashlib.md5(open(file_full_path, 'rb').read()).hexdigest()

def read_dir(dir_path):
    path = []
    for rt, dirs, files in os.walk(dir_path):
        for f in files:
            path.append(rt+"/"+f)
    return path

def check_dir_md5(dir_path):
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        for file_path in read_dir(dir_path):
            # print(os.path.basename((file_path)),md5(file_path))
            yield os.path.basename((file_path)) , md5(file_path)
    else:
        return "Your path is not a directory, Please select a correctly directory"

def main():
    import time
    start = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument("dpath",help="your directory path")
    parser.add_argument("table",help="your table name path")
    args = parser.parse_args()


    engine = create_engine('sqlite:///./filecheck.db',echo=False)
    metadata = MetaData(engine)

    if args.dpath and args.table is not None:

        files_table = Table(args.table, metadata,
                            Column('id', Integer, primary_key=True),
                            Column('filename', String(50)),
                            Column('filemd5', String(32)))

        metadata.create_all(engine)
        g = pool.Pool()
        for k,v in check_dir_md5(args.dpath):
            # print (k,v)
            g.spawn((insert_to_sqlitedb( args.table,metadata,k,v)))
            g.join()
            # insert_to_sqlitedb(args.table,metadata,k,v)
    elif args.table is None:
        print("Please setting a tablename")
    else:
        print("T_T,It's look like not professional....")

    end = time.time()
    print("Totally time is : ",end - start)

if __name__ == '__main__':
    main()


#  this is a magic shell command, you can use like this :
#   
#   $ find ./ -type f -exec md5sum {} \;  -exec basename {} \; | cut -c 1-32 | sed '$!N;s/\n/,/' | sed '1 ifilemd5,filename'  > ../filemd5.csv
#   $ echo "CREATE TABLE webshell (filename varchar(255) not null, filemd5 varchar(255) not null); 
#        .separator ,
#        .import filemd5.csv webshell" > restore.sql
#   $ sqlite3 webshell.db < restore.sql

#   Attation: the code encode decode