import os
import pandas as pd

def move_values_in_first_data_row(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.csv'):  # Process only CSV files
                file_path = os.path.join(root, file)
                try:
                    # Read the CSV into a DataFrame
                    df = pd.read_csv(file_path)
                    
                    # Ensure there are at least two rows (header + data)
                    if len(df) > 1:
                        # Move value from 'AltTitle.other' (column I) to 'Title' (column J) in the first data row (index 0)
                        if 'AltTitle.other' in df.columns and 'Title' in df.columns:
                            # Move value from the first data row (index 0)
                            df.loc[0, 'Title'] = df.loc[0, 'AltTitle.other']  # Move the value
                            df.loc[0, 'AltTitle.other'] = ''  # Clear the original value if needed
                            
                            # Save the updated DataFrame back to the file
                            df.to_csv(file_path, index=False)
                            print(f"Updated file: {file_path}")
                        else:
                            print(f"Skipped file (missing 'AltTitle.other' or 'Title' columns): {file_path}")
                    else:
                        print(f"Skipped file (not enough rows): {file_path}")
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

if __name__ == "__main__":
    # Ask user for the folder path
    folder_path = input("Enter the path to the folder containing CSV files: ").strip()
    if os.path.exists(folder_path):
        move_values_in_first_data_row(folder_path)
    else:
        print("The provided folder path does not exist.")
