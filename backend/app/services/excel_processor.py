import pandas as pd

def process_file(file):
    df = pd.read_excel(file.file)

    for _, row in df.iterrows():
        # Insert row safely into DB
        pass