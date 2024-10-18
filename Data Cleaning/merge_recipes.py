import pandas as pd
import numpy as np

df1 = pd.read_csv('recipes_food_com.csv')
df2 = pd.read_csv('Datasets/epicurious.csv.xz')

df2 = df2[['Title', 'Instructions', 'Cleaned_Ingredients']]
df2.rename(columns = {'Title': 'Name',
                      'Cleaned_Ingredients' : 'Ingredients'}, inplace = True)
df2 = df2.dropna()

for col in df1.columns:
    if col not in df2.columns:
        df2[col] = np.nan
df1.info()

merged_df = pd.concat([df1, df2], ignore_index = True)
merged_df.to_csv('merged_recipes.csv', index = False)
merged_df.info()