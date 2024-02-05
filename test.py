import pandas as pd
import matplotlib.pyplot as plt

# Sample DataFrame with a date index and multiple series
data = {'Value1': [10, 15, 5, 20, 8],
        'Value2': [5, 10, 8, 15, 12]}
index = pd.to_datetime(['2022-01-01', '2022-01-15', '2022-02-05', '2022-02-20', '2022-03-10'])

df = pd.DataFrame(data, index=index)

# Resample only 'Value1' series by month and sum
monthly_sum_value1 = df['Value1'].resample('M').sum()

# Plot the results
monthly_sum_value1.plot(kind='bar', xlabel='Month', ylabel='Sum of Value1', title='Monthly Sum of Value1')
plt.show()
