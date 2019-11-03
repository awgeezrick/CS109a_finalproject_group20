# spotify_utils
# Author - Mark McDonald - 2019
# Includes some basic utilities for Spotify db and api handling

import os
import sys
import json
import time
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tqdm import tqdm_notebook as tqdm

class List_Generator():
    """
    Create batch generator for a list that you want to interate over
    """

    def __init__(self, mainlist, batch_size:int=50):

        self.mainlist = mainlist
        self.batch_size = batch_size
        self.length = len(self.mainlist)
        self.num_batches = int(self.length / self.batch_size)+1

        print("Creating List Generator:")
        print("\tbatch size : ",self.batch_size)
        print("\tlength     : ",self.length)
        print("\tnum batches: ",self.num_batches)

    def batch_generator(self) -> list:
        batch_num = 0
        start = 0
        finished = False
        progbar = tqdm(total=self.length)
        while True:
            if not finished:
                start = batch_num * self.batch_size
                end = (batch_num * self.batch_size) + self.batch_size
                record_batch = self.mainlist[start:end]
                batch_num += 1
                progbar.update(len(record_batch))
                if record_batch==None or len(record_batch)<self.batch_size:
                    finished = True
                yield record_batch
            else:
                break
        progbar.close()


class Table_Generator():
    """
    Create batch generator for a db table that you want to interate over
    """

    def __init__(self, query, batch_size:int=50):

        self.query        = query
        self.batch_size   = batch_size
        self.length       = self.query.count()
        self.num_batches  = int(self.length / self.batch_size)+1

        print("Creating Table Generator:")
        print("\tbatch size : ",self.batch_size)
        print("\tlength     : ",self.length)
        print("\tnum batches: ",self.num_batches)

    def batch_generator(self) -> list:
        offset = 0
        end    = False
        progbar = tqdm(total=self.length)
        while True:
            if not end:
                record_batch = self.query.limit(self.batch_size).offset(offset).all()
                offset += self.batch_size
                progbar.update(len(record_batch))
                if record_batch==None or len(record_batch)<self.batch_size:
                    end = True
                yield record_batch
            else:
                break
        progbar.close()
