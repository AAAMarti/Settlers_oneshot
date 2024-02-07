import pandas as pd

# Read the CSV file
file_path = r'D:\linguistic_only_tables\linguistic_only_tables\incoming_base_spect.csv'
df = pd.read_csv(file_path)

# Create a dictionary to map dialogue_act and relation_type to their corresponding columns
dialogue_act_map = {"Offer": "Offer", "Counteroffer": "Counteroffer", "Accept": "Accept", "Refusal": "Refusal", "Other": "Other"}
surface_act_map = {"Assertion": "Assertion", "Question": "Question", "Request": "Request"}
relation_type_map = {"Continuation": "Continuation", "Narration": "Narration", "Result": "Result",
                     "Correction": "Correction", "Elaboration": "Elaboration", "Explanation": "Explanation",
                     "Conditional": "Conditional", "Alternation": "Alternation", 
                     "Contrast": "Contrast", "Parallel": "Parallel",
                     "Question_answer_pair": "Question_answer_pair", "Commentary": "Commentary",
                     "Q-elab": "Q-elab", "Clarification_Q": "Clarification_Q", "Acknowledgement": "Acknowledgement",
                     "Background": "Background"}

# Initialize the output text
output_text = "doc\tdialogue_num\tEmitter\tAddressee\ttext\t" + "\t".join(list(surface_act_map.keys()) + list(dialogue_act_map.keys()) + list(relation_type_map.keys())) + "\tContext\n"

# Iterate through each row in the dataframe
for index, row in df.iterrows():
    if index > 13440:
        break
    doc = row['doc']
    dialogue_num = row['dialogue_num']
    text = row['text']
    addressee = row['addressee'] if 'addressee' in df.columns else ''
    emitter = row['emitter'] if 'emitter' in df.columns else ''
    
    # Get all texts uttered before the current text during the same dialogue
    context_texts = df[(df['doc'] == doc) & (df['dialogue_num'] == dialogue_num) & (df.index < index)]['text'].tolist()
    
    # Convert any NaN values to empty strings
    context_texts = [str(text) if pd.notnull(text) else '' for text in context_texts]
    
    # Join the context texts into a single string
    context_str = " ".join(context_texts)
    
    # Initialize row data with doc, dialogue_num, text, adressee, and emitter
    row_data = f"{doc}\t{dialogue_num}\t{emitter}\t{addressee}\t{text}\t"
    
    # Check for surface_act, dialogue_act, and relation_type presence
    for key, value in surface_act_map.items():
        row_data += "1\t" if row['surface_act'] == key else "0\t"
    for key, value in dialogue_act_map.items():
        row_data += "1\t" if row['dialogue_act'] == key else "0\t"
    for key, value in relation_type_map.items():
        row_data += "1\t" if row['relation_type'] == key else "0\t"
    
    # Append the context data to the row
    row_data += f"{context_str}\n"
    
    # Append the row to the output text
    output_text += row_data

# Save the output text to a file named "Annotations_STAC"
with open("Annotations_STAC.txt", "w") as file:
    file.write(output_text)
