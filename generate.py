import csv
import random
import string
import os

# --- Configuration ---
FILENAME = "dummy_data.csv"
NUM_COLS = 20

# OPTION 1: Set to ~1,500 for a ~100 KB file
# OPTION 2: Set to 100,000 for a ~8 MB file
NUM_ROWS = 1500 

def generate_random_string(length=4):
    """Generates a random string of fixed length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_csv(filename, rows, cols):
    print(f"Generating {rows} rows and {cols} columns...")
    
    # Create column headers (e.g., Col_1, Col_2, ...)
    headers = [f"Col_{i+1}" for i in range(cols)]
    
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        # Generate rows
        for _ in range(rows):
            # Mix of random strings and numbers for realistic data sizing
            row = [
                generate_random_string(random.randint(2, 6)) if random.choice([True, False]) 
                else str(random.randint(10, 9999)) 
                for _ in range(cols)
            ]
            writer.writerow(row)
            
    # Calculate and print the resulting file size
    file_size_bytes = os.path.getsize(filename)
    file_size_kb = file_size_bytes / 1024
    file_size_mb = file_size_kb / 1024
    
    print(f"✅ File created successfully: {filename}")
    print(f"📊 Final File Size: {file_size_bytes:,} bytes ({file_size_kb:.2f} KB / {file_size_mb:.2f} MB)")

if __name__ == "__main__":
    generate_csv(FILENAME, NUM_ROWS, NUM_COLS)
