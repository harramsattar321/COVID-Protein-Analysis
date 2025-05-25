import os
import csv
import string
from collections import Counter
import glob

def process_fasta_files(folder_path, output_csv_path):
    """
    Process all .txt files in the given folder and store sequence data in a CSV file.
    
    Args:
        folder_path: Path to the folder containing .txt files
        output_csv_path: Path where the output CSV will be saved
    """
    # Initialize a list to store all data
    all_data = []
    
    # Get all txt files in the folder
    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
    
    for file_path in txt_files:
        # Extract filename without extension as label
        filename = os.path.basename(file_path)
        label = os.path.splitext(filename)[0]
        
        with open(file_path, 'r') as file:
            lines = file.readlines()
            
            i = 0
            while i < len(lines):
                if lines[i].startswith('>'):
                    # Found a header line, extract the sequence that follows
                    sequence = ""
                    i += 1  # Move to the next line
                    
                    # Continue reading sequence until we hit a blank line or another header
                    while i < len(lines) and not lines[i].startswith('>') and lines[i].strip():
                        sequence += lines[i].strip()
                        i += 1
                    
                    # Process the sequence if it's not empty
                    if sequence:
                        # Count occurrences of each letter A-Z
                        counter = Counter(sequence.upper())
                        
                        # Create a row with counts for each letter A-Z
                        row = {letter: counter.get(letter, 0) for letter in string.ascii_uppercase}
                        
                        # Add the label
                        row['Label'] = label
                        
                        all_data.append(row)
                else:
                    i += 1
    
    # Write data to CSV
    if all_data:
        fieldnames = list(string.ascii_uppercase) + ['Label']
        
        with open(output_csv_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_data)
        
        print(f"Data successfully saved to {output_csv_path}")
    else:
        print("No data was processed.")

# Example usage
if __name__ == "__main__":
    input_folder = "Dataset"
    output_csv = "genome_sequences.csv"
    
    process_fasta_files(input_folder, output_csv)