import pandas as pd
import glob
import os


folder_path = "."  # current folder; change to your folder path if needed
pattern = "answer_*.csv"  # matches all your answer_q1.csv, answer_q2.csv, etc.
output_file = "merged.csv"

csv_files = glob.glob(os.path.join(folder_path, pattern))


def standardize_columns(df):
    """Rename columns to English standard names regardless of language."""
    rename_map = {}
    for col in df.columns:
        col_lower = col.strip().lower()
        if "question" in col_lower or "問題" in col:
            rename_map[col] = "question"
        elif "scenario" in col_lower or "情境" in col:
            rename_map[col] = "scenario"
        elif "answer" in col_lower or "answers" in col_lower or "回答" in col or "答案" in col:
            rename_map[col] = "answer"
    if rename_map:
        df = df.rename(columns=rename_map)
    
    return df


all_data = []

for file in csv_files:
    try:
        
        df = pd.read_csv(file, encoding='utf-8-sig')  # handles BOM in some files
        
        
        df = standardize_columns(df)
        
        
        source_name = os.path.splitext(os.path.basename(file))[0]
        df["source_file"] = source_name
        
        all_data.append(df)
        print(f"Loaded: {os.path.basename(file)} - {len(df)} rows")
        
    except Exception as e:
        print(f"Error reading {file}: {e}")

if not all_data:
    print("No data loaded. Exiting.")
    exit()


merged_df = pd.concat(all_data, ignore_index=True, sort=False)


merged_df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n✅ Successfully merged {len(all_data)} files into '{output_file}'")
print(f"Total rows: {len(merged_df)}")
print(f"Columns: {list(merged_df.columns)}")
