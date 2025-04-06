import json 
import os
import pandas as pd
import h5py
import numpy as np



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

    bash_file = "bash " + file_name

    asset = os.popen(bash_file).read().strip()

    return json.loads(asset)


def get_current_scrap() -> pd.DataFrame:

    # Lire les fichiers .sh dans le dossier actuel, les stocker dans une liste
    sh_file = [file for file in os.listdir(os.getcwd()) if file.endswith("SOL.sh")]

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

    # Colonne timestamp comme Datetime Index
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df.sort_values(by='timestamp')

    # Mettre 'timestamp' comme index proprement (et ne pas le garder en colonne)
    df.set_index('timestamp', inplace=True)

    # Supprimer la colonne 'symbol'
    df.drop(columns="symbol", inplace=True)
    
    return df


def save_to_h5(df = pd.DataFrame):

    # Forcer le type des colonnes une à une
    df['timestamp'] = df['timestamp'].astype(str)
    df['open'] = df['open'].astype(np.float32)
    df['high24h'] = df['high24h'].astype(np.float32)
    df['low24h'] = df['low24h'].astype(np.float32)
    df['lastPr'] = df['lastPr'].astype(np.float32)
    df['quoteVolume'] = df['quoteVolume'].astype(np.float64)

    # Construire une structure de tableau structuré (record array)
    dtype = np.dtype([
        ('timestamp', h5py.string_dtype('utf-8')),
        ('open', 'f4'),
        ('high24h', 'f4'),
        ('low24h', 'f4'),
        ('lastPr', 'f4'),
        ('quoteVolume', 'f8'),
    ])
    records = np.array([tuple(row) for row in df.to_numpy()], dtype=dtype)

    # Sauvegarde dans le fichier HDF5
    with h5py.File("latest_scrap.h5", "w") as h5f:
        h5f.create_dataset("data", data=records)

        # Sauvegarder les colonnes aussi, si tu veux
        col_names = np.array(df.columns, dtype=h5py.string_dtype('utf-8'))
        h5f.create_dataset("columns", data=col_names)

def save_to_csv(df : pd.DataFrame) :

    file_path = os.path.join(os.getcwd(), "data.csv")

    if os.path.exists(file_path):
        old_data = pd.read_csv(file_path, index_col=0, parse_dates=True)
        df = pd.concat([old_data, df], axis=0)
        df.to_csv(file_path, index=True)
    
    else:
        df.to_csv(file_path, index=True)

    return None


if __name__ == "__main__":

    df = get_current_scrap()

    save_to_csv(df)

    pass