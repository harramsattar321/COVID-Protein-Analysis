import os
import csv
import string
from collections import Counter
import glob
import re

def process_peptide_files(folder_path, output_csv_path):
    """
    Process all .txt files in the given folder with new parsing rule:
    - Look for lines starting with arrow or numeric value
    - Read from next line until empty line and store as one record
    - Store amino acid counts in a CSV file.
    
    Args:
        folder_path: Path to the folder containing .txt files
        output_csv_path: Path where the output CSV will be saved
    """
    all_data = []
    filtered_count = 0

    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
    
    if not txt_files:
        print(f"No .txt files found in {folder_path}")
        return

    for file_path in txt_files:
        filename = os.path.basename(file_path)
        label = os.path.splitext(filename)[0]
        
        print(f"Processing file: {filename}")

        with open(file_path, 'r') as file:
            lines = file.readlines()
            
            i = 0
            record_count = 0
            
            while i < len(lines):
                line = lines[i].strip()
                
                # Check if line starts with arrow or numeric value
                if line and (line.startswith('>') or line.startswith('<') or 
                           line.startswith('->') or line.startswith('<-') or
                           re.match(r'^\d', line)):  # starts with digit
                    
                    print(f"  Found header at line {i+1}: {line[:50]}{'...' if len(line) > 50 else ''}")
                    
                    # Start reading from next line until empty line
                    i += 1
                    sequence_lines = []
                    
                    while i < len(lines):
                        current_line = lines[i].strip()
                        
                        # If we hit an empty line, stop reading this record
                        if not current_line:
                            break
                            
                        sequence_lines.append(current_line)
                        i += 1
                    
                    # Combine all sequence lines into one sequence
                    full_sequence = ''.join(sequence_lines)
                    
                    # Skip if sequence is empty
                    if not full_sequence:
                        print(f"    Skipping empty sequence for record {record_count + 1}")
                        filtered_count += 1
                        i += 1  # Move past the empty line
                        continue
                    
                    # Check if sequence contains only letters and spaces
                    if not all(c.isalpha() or c.isspace() for c in full_sequence):
                        print(f"    Skipping sequence with numbers/symbols for record {record_count + 1}: '{full_sequence[:50]}{'...' if len(full_sequence) > 50 else ''}'")
                        filtered_count += 1
                        i += 1  # Move past the empty line
                        continue
                    
                    # Remove spaces for counting amino acids
                    seq_no_spaces = full_sequence.replace(' ', '')
                    
                    # Skip if after removing spaces, there are no letters left
                    if not seq_no_spaces:
                        print(f"    Skipping sequence with only spaces for record {record_count + 1}")
                        filtered_count += 1
                        i += 1  # Move past the empty line
                        continue
                    
                    # Count A-Z in the sequence
                    counter = Counter(seq_no_spaces.upper())
                    row = {letter: counter.get(letter, 0) for letter in string.ascii_uppercase}
                    
                    # Check if all amino acid counts are zero
                    total_amino_acids = sum(row.values())
                    if total_amino_acids == 0:
                        print(f"    Skipping record with no amino acids for record {record_count + 1}")
                        filtered_count += 1
                        i += 1  # Move past the empty line
                        continue
                    
                    # Add metadata
                    record_count += 1
                    row['Label'] = f"{label}_{record_count}"
                    row['Original_Label'] = label
                    row['Record_Number'] = record_count
                    row['Sequence_Length'] = len(seq_no_spaces)
                    
                    all_data.append(row)
                    print(f"    Processed record {record_count}: {len(seq_no_spaces)} amino acids")
                    
                    i += 1  # Move past the empty line
                else:
                    i += 1  # Move to next line if current line doesn't match criteria

        print(f"  Found {record_count} valid records in {filename}")

    # Write to CSV
    if all_data:
        fieldnames = list(string.ascii_uppercase) + ['Label', 'Original_Label', 'Record_Number', 'Sequence_Length']
        
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_data)
        
        print(f"\nData successfully saved to {output_csv_path}")
        print(f"Total records processed: {len(all_data)}")
        if filtered_count > 0:
            print(f"Records filtered out: {filtered_count}")
        
        # Show summary by file
        print("\nSummary by file:")
        file_counts = {}
        for row in all_data:
            orig_label = row['Original_Label']
            file_counts[orig_label] = file_counts.get(orig_label, 0) + 1
        
        for file_label, count in file_counts.items():
            print(f"  {file_label}.txt: {count} records")
            
    else:
        print("No valid data was processed.")

if __name__ == "__main__":
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(script_dir, "Dataset")
    output_csv = os.path.join(script_dir, "peptide_sequences.csv")
    
    print(f"Looking for folder: {input_folder}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Check if folder exists
    if not os.path.exists(input_folder):
        print(f"Error: Folder '{input_folder}' does not exist.")
        print("Available folders/files in script directory:")
        try:
            for item in os.listdir(script_dir):
                item_path = os.path.join(script_dir, item)
                if os.path.isdir(item_path):
                    print(f"  [DIR]  {item}")
                else:
                    print(f"  [FILE] {item}")
        except Exception as e:
            print(f"  Could not list directory contents: {e}")
    else:
        process_peptide_files(input_folder, output_csv)