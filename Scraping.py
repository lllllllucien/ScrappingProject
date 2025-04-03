import json 
import os
import time
from datetime import datetime
import pandas as pd


def read_dic(dic, indent=0):
    if isinstance(dic, dict):
        for key, value in dic.items():
            print("  " * indent + str(key))
            read_dic(value, indent + 1)
    elif isinstance(dic, list):
        for index, item in enumerate(dic):
            print("  " * indent + f"[{index}]")
            read_dic(item, indent + 1)
    else:
        print("  " * indent + str(dic))


def run_scrap(file_name : str) -> dict:

    time_exec = datetime.now()

    bash_file = "bash " + file_name

    btc = os.popen(bash_file).read().strip()

    return json.loads(btc)


def get_current_scrap() -> pd.DataFrame:

    sh_file = [file for file in os.listdir(os.getcwd()) if file.endswith(".sh")]

    data = []

    for file in sh_file:

        scrap = run_scrap(file)

        for k,v in scrap.items():
            try:
                scrap[k] = float(v)
            except:
                continue

        data.append(scrap)

    df = pd.DataFrame(data)

    # Convert 'timestamp' to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Sort the DataFrame by timestamp
    df = df.sort_values(by='timestamp').reset_index(drop=True)
    
    return df
    
path = "C:/Users/lucie/OneDrive/Documents/ESILV/A4/S2/Git"
if __name__ == "__main__":

    os.chdir(path)

    print(get_current_scrap())

    

    pass