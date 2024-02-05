import pandas as pd

# Existing DataFrame
data = {'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35]}

df = pd.DataFrame(data)

# New row data
new_data = {'Name': 'David', 'Age': 28}

# Creating a new DataFrame with the new row
new_row_df = pd.DataFrame([new_data], index=[len(df)])

# Appending the new row DataFrame to the existing DataFrame
df = pd.concat()

print(df)