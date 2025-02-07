# Machine-Learning-and-AI-Project

The code executes an analysis which detects suspicious economic transactions in an Excel spreadsheet. A dataset of transaction details includes the "Country" field along with "Amount" data while containing "TransactionWording."  The script starts its operation by importing three vital datasets: flagged_words.json with suspicious transaction keyword definitions and country.json containing transaction country-based confidence measures along with amountscale.json which defines transaction amount categories.  

The flag_suspicious_transactions function examines every row in the selected data set to search for fraudulent transactions. The script will activate a suspicious transaction flag if it finds any keywords from the flagged keywords list within the transaction wording. Subsequently the function applies confidence ratings to countries from the loaded country confidence data source. The amount level evaluation is determined through the process of comparing each transaction amount to defined amount scale ranges.  

The flagged transactions together with the new "Country confidence level" and "Amount Level" columns get saved into a separate Excel file duplicate. The code positions the new columns directly next to their corresponding data points for easy understanding.  

The script streamlines security analysis by detecting questionable transactions through keyword scans and country risk assessment and transaction value evaluation which generates direct results in the processed Excel file. 
