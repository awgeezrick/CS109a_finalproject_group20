# spotify_utils
# Author - Mark McDonald - 2019
# Includes some basic utilities for Spotify db and api handling

import os
import pickle
from tqdm import tqdm_notebook as tqdm

class List_Generator():
    """
    Create batch generator for a list that you want to interate over
    """

    def __init__(self, mainlist, batch_size: int = 50, name: str = None):

        self.mainlist = mainlist
        self.batch_size = batch_size
        self.length = len(self.mainlist)
        self.num_batches = int(self.length / self.batch_size)+1
        self.name = name

        print("Creating List Generator:")
        print("\tbatch size : ",self.batch_size)
        print("\tlength     : ",self.length)
        print("\tnum batches: ",self.num_batches)

    def batch_generator(self) -> list:
        batch_num = 0
        start = 0
        finished = False
        progbar = tqdm(total=self.length, desc=self.name)
        while True:
            if not finished:
                start = batch_num * self.batch_size
                end = (batch_num * self.batch_size) + self.batch_size
                record_batch = self.mainlist[start:end]
                batch_num += 1
                progbar.update(len(record_batch))
                if record_batch is None or len(record_batch) == 0 or len(record_batch) < self.batch_size:
                    finished = True
                yield record_batch
            else:
                break
        progbar.close()


class Table_Generator():
    """
    Create batch generator for a db table that you want to interate over
    """

    def __init__(self, query, batch_size:int=50, name:str=None):

        self.query        = query
        self.batch_size   = batch_size
        self.length       = self.query.count()
        self.num_batches  = int(self.length / self.batch_size)+1
        self.name         = name

        print("Creating Table Generator:")
        print("\tbatch size : ", self.batch_size)
        print("\tlength     : ", self.length)
        print("\tnum batches: ", self.num_batches)

    def batch_generator(self) -> list:
        offset = 0
        end    = False
        progbar = tqdm(total=self.length, desc=self.name)
        while True:
            if not end:
                record_batch = self.query.limit(self.batch_size).offset(offset).all()
                offset += self.batch_size
                progbar.update(len(record_batch))
                if record_batch is None or len(record_batch) == 0 or len(record_batch) < self.batch_size:
                    end = True
                yield record_batch
            else:
                break
        progbar.close()


## Example
## pickle_save( history_p2_1,'p2_1.pkl' )
## history_p2_1 = pickle_load('p2_1.pkl')
## history_p2_1 = history_p2_1[0]
def pickle_save(variable, pickel_filename):
    cwd = os.getcwd()
    save_dir = cwd + '//pickle//'
    save_file = save_dir + pickel_filename
    if os.path.isdir(save_dir) == 0:
        os.mkdir(save_dir)
    with open(save_file, 'wb') as f:
        pickle.dump(variable, f)


def pickle_load(pickel_filename):
    cwd = os.getcwd()
    pickle_file = cwd + '//pickle//' + pickel_filename
    # Getting back the data:
    with open(pickle_file, 'rb') as f:
        variable = pickle.load(f)
        return variable


