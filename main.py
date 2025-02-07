import pandas as pd
import json
import shutil

# Load flagged words from JSON file
def load_flagged_words():
    with open('flagged_words.json', 'r') as file:
        data = json.load(file)
    return data['flagged_words']

# Load country confidence data from JSON file
def load_country_confidence():
    with open('country.json', 'r') as file:
        data = json.load(file)
    return data

# Load amount scale data from JSON file
def load_amount_scale():
    with open('amountscale.json', 'r') as file:
        data = json.load(file)
    return data

def get_amount_level(amount, amount_scale):
    for range_str, level in amount_scale.items():
        min_val, max_val = map(int, range_str.split('-'))
        if min_val <= amount < max_val:
            return level
    return 1  # Default level if amount is out of range

def flag_suspicious_transactions(df, flagged_words, country_confidence_data, amount_scale):
    # Create a new column to store flag (1 for suspicious, 0 for not flagged)
    df['Flagged'] = 0  # Default is not flagged
    
    # Create new columns
    df['Country confidence level'] = 0.0  # Default is 0.0
    df['Amount Level'] = 1.0  # Default level if no match found

    for index, row in df.iterrows():
        transaction_wording = row['TransactionWording'].lower()  # Convert text to lowercase for easier matching
        
        # Check if any flagged word is present in the transaction wording
        if any(flagged_word in transaction_wording for flagged_word in flagged_words):
            df.at[index, 'Flagged'] = 1  # Flagged as suspicious
        
        # Get the country confidence level from the loaded data
        country = row['Country']
        country_confidence = 0.0
        for source_country, confidence_mapping in country_confidence_data.items():
            if country in confidence_mapping:
                country_confidence = confidence_mapping[country]
                break  # Stop searching once found
        df.at[index, 'Country confidence level'] = country_confidence
        
        # Get the amount level
        amount = row['Amount']
        df.at[index, 'Amount Level'] = get_amount_level(amount, amount_scale)
    
    # Reorder columns to place 'Country confidence level' after 'Country' and 'Amount Level' after 'Amount'
    columns_order = df.columns.tolist()
    if 'Country' in columns_order and 'Country confidence level' in columns_order:
        country_index = columns_order.index('Country')
        columns_order.insert(country_index + 1, columns_order.pop(columns_order.index('Country confidence level')))
    if 'Amount' in columns_order and 'Amount Level' in columns_order:
        amount_index = columns_order.index('Amount')
        columns_order.insert(amount_index + 1, columns_order.pop(columns_order.index('Amount Level')))
    df = df[columns_order]
    
    return df

# Path of the original Excel file
original_file_path = 'negative_fraud_transactions2.xlsx'  # Replace with the actual file path

# Create a copy of the original Excel file
copied_file_path = 'copied_fraud_transactions.xlsx'
shutil.copy(original_file_path, copied_file_path)

# Load the copied Excel file to modify its contents
df = pd.read_excel(copied_file_path)

# Load flagged words, country confidence data, and amount scale data
flagged_words = load_flagged_words()
country_confidence_data = load_country_confidence()
amount_scale = load_amount_scale()

# Run the analysis and flag suspicious transactions
flagged_df = flag_suspicious_transactions(df, flagged_words, country_confidence_data, amount_scale)

# Save the changes in the copied Excel file (overwrite the copied file)
flagged_df.to_excel(copied_file_path, index=False)
print(f"Suspicious transactions flagged and saved to {copied_file_path}")
