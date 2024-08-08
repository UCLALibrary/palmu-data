import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import os
import imagesize
from io import BytesIO

# Function to get image dimensions from URL
def get_image_dimensions(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check that the request was successful
        img_data = BytesIO(response.content)
        width, height = imagesize.get(img_data)
        return width, height
    except Exception as e:
        print(f"Error getting dimensions for {url}: {e}")
        return None, None

# Get input CSV file path from user and strip extra whitespace
csv_file_path = input("Enter the path to the input CSV file: ").strip()

# Extract file name without extension
file_name = os.path.splitext(os.path.basename(csv_file_path))[0]

# Read CSV file
df = pd.read_csv(csv_file_path)

# Create new columns for height and width
df['media.height'] = None
df['media.width'] = None

# Function to update DataFrame with image dimensions
def update_dimensions(index, row):
    image_url_column = 'IIIF Access URL'  # This column name should be adjusted to match your CSV
    image_url = row[image_url_column]
    width, height = get_image_dimensions(image_url)
    df.at[index, 'media.width'] = width
    df.at[index, 'media.height'] = height

# Update DataFrame with image dimensions in parallel using concurrent.futures module
with ThreadPoolExecutor(max_workers=8) as executor:  # Adjust max_workers based on your system
    futures = [executor.submit(update_dimensions, index, row) for index, row in df.iterrows()]
    for future in tqdm(futures, total=len(futures), desc="Processing images"):
        future.result()

# Save the updated DataFrame to a new CSV file with original file name
output_csv_file_path = f'{file_name}_with_dimensions.csv'
df.to_csv(output_csv_file_path, index=False)

print(f"Image dimensions added and saved to {output_csv_file_path}")