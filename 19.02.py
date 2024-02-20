import pandas as pd

# Read the CSV file
file_path = r'D:\linguistic_only_tables\linguistic_only_tables\incoming_base_spect.csv'
df = pd.read_csv(file_path)

# Initialize an empty list to store DataFrames
dfs = []

# Define the dialogue acts to consider for grouping
grouping_dialogue_acts = {"Offer", "Counteroffer", "Accept", "Refusal"}

# Iterate through each row in the dataframe
index = 0
while index < len(df):
    # Get the original_turn_number of the current row
    original_turn_number = df.loc[index, "original_turn_number"]
    emitter = df.loc[index, "emitter"]
    # Check if there are consecutive rows with the same original_turn_number and emitter
    consecutive_rows = [index]
    while index + 1 < len(df) and df.loc[index + 1, "original_turn_number"] == original_turn_number and df.loc[index + 1, "emitter"] == emitter:
        consecutive_rows.append(index + 1)
        index += 1
    index += 1

    if len(consecutive_rows) == 1:
        # Only one row for this original_turn_number and emitter, append as it is
        dfs.append(df.loc[consecutive_rows[0], ["subdoc", "emitter", "addressee", "dialogue_act", "text", "original_turn_number"]].to_frame().transpose())
    else:
        # Multiple consecutive rows with the same original_turn_number and emitter
        dialogue_acts = set(df.loc[consecutive_rows, "dialogue_act"])
        # Check if there are 2 or more types between Offer, Counteroffer, Accept, and Refusal
        if len(grouping_dialogue_acts.intersection(dialogue_acts)) >= 2:
            # Keep them splitted as regular
            for row_index in consecutive_rows:
                dfs.append(df.loc[row_index, ["subdoc", "emitter", "addressee", "dialogue_act", "text", "original_turn_number"]].to_frame().transpose())
        else:
            # Group these lines in one line
            combined_text = " ".join(df.loc[consecutive_rows, "text"].tolist())
            combined_dialogue_act = " ".join(dialogue_acts)
            # Keep only one type between Offer, Counteroffer, Accept, and Refusal as dialogue_act
            for act in grouping_dialogue_acts:
                if act in combined_dialogue_act:
                    combined_dialogue_act = act
                    break
            row_data = {"subdoc": df.loc[consecutive_rows[0], "subdoc"],
                        "emitter": df.loc[consecutive_rows[0], "emitter"],
                        "addressee": df.loc[consecutive_rows[0], "addressee"],
                        "dialogue_act": combined_dialogue_act,
                        "text": combined_text,
                        "original_turn_number": original_turn_number}
            dfs.append(pd.DataFrame(row_data, index=[0]))

# Concatenate the DataFrames
output_df = pd.concat(dfs, ignore_index=True)

# Save the output dataframe to a file named "test2_STAC.txt"
output_df.to_csv("test2_STAC.txt", sep='\t', index=False)
