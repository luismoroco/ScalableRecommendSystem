import os 

output_folder = os.path.join(os.getcwd(), 'data', 'preprocessed')

def exportFile(df: any, name: str) -> None:
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f'{name}.csv')
    df.to_csv(output_file, index=False)
    