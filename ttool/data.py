import os
import pandas as pd


class Olist:
    def get_data(self):
        """
        This function returns a Python dict.
        Its keys should be 'sellers', 'orders', 'order_items' etc...
        Its values should be pandas.DataFrames loaded from csv files
        """
        # Hints 1: Build csv_path as "absolute path" in order to call this method from anywhere.
            # Do not hardcode your path as it only works on your machine ('Users/username/code...')
            # Use __file__ instead as an absolute path anchor independant of your usename
            # Make extensive use of `breakpoint()` to investigate what `__file__` variable is really
        # Hint 2: Use os.path library to construct path independent of Mac vs. Unix vs. Windows specificities
        #\\wsl$\Ubuntu\home\hossein\code\hbaloochi\data-challenges\04-Decision-Science\data\csv
        #'/home/hossein/code/hbaloochi/data-challenges/04-Decision-Science/olist/data.py'
        csv_path=os.path.join(__file__[:-8],'..','data','csv')
        file_names=os.listdir(csv_path)[1:]
        key_names=[fn[0:-4] for fn in file_names]
        key_names=[kn.replace('olist_','') for kn in key_names]
        key_names=[kn.replace('_dataset','') for kn in key_names]
        data={}
        data={kn:pd.read_csv(os.path.join(csv_path,fn)) for (kn,fn) in zip(key_names,file_names) }
        return data


    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")
