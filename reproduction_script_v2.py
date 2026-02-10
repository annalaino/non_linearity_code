
import os
import pandas as pd

cwd = os.getcwd()
print(f"Current Working Directory: {cwd}")

root_path = os.path.join(cwd, 'data')
print(f"Root path: {root_path}")

csv_name = "baseline"
csv_filename = f"{csv_name}.csv"

print(f"Attempting to write {csv_filename} to CWD...")
try:
    with open(csv_filename, 'w') as f:
        f.write("test,content\n1,2")
    print(f"Successfully created {csv_filename} using open()")
except Exception as e:
    print(f"Failed to create {csv_filename} using open(): {e}")

print(f"Attempting to write {csv_name}_pandas.csv to CWD...")
try:
    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    df.to_csv(f'{csv_name}_pandas.csv', index=False)
    print(f"Successfully created {csv_name}_pandas.csv using pandas")
except Exception as e:
    print(f"Failed to create {csv_name}_pandas.csv using pandas: {e}")

# Check folder path logic
folder_path_1 = os.path.join(root_path, 'baseline')
print(f"Folder path 1: {folder_path_1}")
print(f"Basename of folder path 1: {os.path.basename(folder_path_1)}")

if os.path.exists(folder_path_1):
    print(f"Folder {folder_path_1} exists.")
else:
    print(f"Folder {folder_path_1} DOES NOT exist.")
