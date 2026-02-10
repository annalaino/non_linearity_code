
import os
import pandas as pd

print(f"Current Working Directory: {os.getcwd()}")
print(f"Root path based on CWD: {os.getcwd() + '\\data\\'}")

csv_name = "baseline"
try:
    with open(f'{csv_name}.csv', 'w') as f:
        f.write("test,content\n1,2")
    print(f"Successfully created {csv_name}.csv using open()")
except Exception as e:
    print(f"Failed to create {csv_name}.csv using open(): {e}")

try:
    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    df.to_csv(f'{csv_name}_pandas.csv', index=False)
    print(f"Successfully created {csv_name}_pandas.csv using pandas")
except Exception as e:
    print(f"Failed to create {csv_name}_pandas.csv using pandas: {e}")

# Check folder path logic
root_path = os.getcwd() + '\\data\\'
folder_path_1 = root_path + 'baseline'
print(f"Folder path 1: {folder_path_1}")
print(f"Basename of folder path 1: {os.path.basename(folder_path_1)}")

if os.path.exists(folder_path_1):
    print(f"Folder {folder_path_1} exists.")
else:
    print(f"Folder {folder_path_1} DOES NOT exist.")
