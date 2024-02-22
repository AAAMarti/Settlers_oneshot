import pandas as pd

# Read the CSV file
file_path = r'D:\linguistic_only_tables\linguistic_only_tables\incoming_base_spect.csv'
df = pd.read_csv(file_path)

# Define the dialogue act classes
dialogue_act_classes = ['Offer', 'Counteroffer', 'Accept', 'Refusal', 'Other']

# Initialize variables to track previous row's information
prev_dialogue_num = None
prev_original_turn_number = None
concatenated_text = ""
concatenated_dialogue_act = set()

# Initialize an empty list to store the formatted rows
formatted_rows = []

# Iterate through each row in the dataframe
for index, row in df.iterrows():
    # Check if the row is from a new dialogue_num
    if prev_dialogue_num != row['dialogue_num']:
        prev_dialogue_num = row['dialogue_num']
    
    # Check if the row is from the same original_turn_number
    if prev_original_turn_number == row['original_turn_number']:
        # Check if the dialogue_act classes are the same or only include one type between offer, counteroffer, accept, and refusal
        if row['dialogue_act'] in dialogue_act_classes or len(concatenated_dialogue_act) == 1:
            concatenated_text += " " + str(row['text'])  # Convert to string
            concatenated_dialogue_act.add(row['dialogue_act'])
        else:
            formatted_rows.append([', '.join(concatenated_dialogue_act), row['emitter'], concatenated_text.strip()])
            concatenated_text = str(row['text'])  # Convert to string
            concatenated_dialogue_act = {row['dialogue_act']}
    else:
        # Append the last concatenated row
        if concatenated_text:
            formatted_rows.append([', '.join(concatenated_dialogue_act), row['emitter'], concatenated_text.strip()])
        # Reset concatenated_text and concatenated_dialogue_act for the new original_turn_number
        concatenated_text = str(row['text'])  # Convert to string
        concatenated_dialogue_act = {row['dialogue_act']}
    
    # Update previous row's information
    prev_original_turn_number = row['original_turn_number']

# Append the last concatenated row
if concatenated_text:
    formatted_rows.append([', '.join(concatenated_dialogue_act), row['emitter'], concatenated_text.strip()])

# Write the formatted rows to the output file
output_file_path = r'D:\Chatbots\STAC\emitter_text_dialogue_act.csv'
df_formatted = pd.DataFrame(formatted_rows, columns=['Dialogue Act', 'Emitter', 'Text'])
df_formatted.to_csv(output_file_path, index=False)
