import os
import csv
import string
from collections import Counter
import glob

def process_peptide_files(folder_path, output_csv_path):
    """
    Process all .txt files in the given folder in new peptide format 
    and store amino acid counts in a CSV file.
    
    Args:
        folder_path: Path to the folder containing .txt files
        output_csv_path: Path where the output CSV will be saved
    """
    all_data = []

    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))

    for file_path in txt_files:
        filename = os.path.basename(file_path)
        label = os.path.splitext(filename)[0]

        with open(file_path, 'r') as file:
            lines = file.readlines()
            
            i = 0
            while i < len(lines) - 1:
                meta_line = lines[i].strip()
                seq_line = lines[i + 1].strip()

                # Example: you can extract a custom label from meta_line if needed
                # parts = meta_line.split(',')
                # custom_label = parts[2].strip() + "_" + parts[3].strip()  # Chain + Description

                # Count A-Z in the sequence
                counter = Counter(seq_line.upper())
                row = {letter: counter.get(letter, 0) for letter in string.ascii_uppercase}
                
                # Add label (either filename or extracted from metadata)
                row['Label'] = label
                all_data.append(row)

                i += 2  # Move to next record

    # Write to CSV
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
    output_csv = "peptide_sequences.csv"
    
    process_peptide_files(input_folder, output_csv)
