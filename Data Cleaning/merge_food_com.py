# Code processes and merges the two datasets scraped from Food.com 

import pandas as pd
import re

df1 = pd.read_csv('data/recipes_ingredients.csv.xz')
df2 = pd.read_csv('data/recipes.csv.xz')

# Remove double spaces in columns
df1['name'] = df1['name'].str.replace(r'\s{2,}', ' ', regex = True)
df2['name'] = df1['name'].str.replace(r'\s{2,}', ' ', regex = True)
df1['ingredients_raw'] = df1['ingredients_raw'].str.replace(r'\s{2,}', ' ', regex = True)

# Remove qutotations in names
df1['name'] = df1['name'].str.replace('"', '', regex = False)
df2['name'] = df2['name'].str.replace('"', '', regex = False)

# Cut down data frames
df1 = df1[['name', 'description', 'ingredients_raw', 'steps', 'servings']]
df2 = df2[['Name', 'TotalTime', 'Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent', 'SodiumContent', 'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent']]
df1.rename(columns = {'name': 'Name',
                      'description' : 'Description',
                      'ingredients_raw' : 'Ingredients',
                      'steps' : 'Instructions',
                      'servings' : 'Servings'}, inplace = True)

# Inner merge, dropping duplicates and null values in Ingredients
merged_df = pd.merge(df1, df2, how = 'inner', on = 'Name')
merged_df = merged_df.drop_duplicates(subset = 'Name', keep = 'first')
merged_df = merged_df.dropna(subset = ['Ingredients'])

# Change to amp and quotation mark
merged_df['Name'] = merged_df['Name'].replace({'&amp;': '&', '&quot;': '"', '&quot': '"', '&ndash': ''}, regex = True)
merged_df['Instructions'] = merged_df['Instructions'].replace({'&amp;': '&', '&quot;': '"', '&quot': '"', '&ndash': ''}, regex = True)

# Function to convert the TotalTime string to minutes
def convert_to_minutes(time):
    hours = 0
    minutes = 0
    
    hours_match = re.search(r'(\d+)H', time)

    if hours_match:
        hours = int(hours_match.group(1))
    
    minutes_match = re.search(r'(\d+)M', time)

    if minutes_match:
        minutes = int(minutes_match.group(1))
    
    total_minutes = hours * 60 + minutes
    return total_minutes

# Apply function
merged_df['TotalTime'] = merged_df['TotalTime'].apply(convert_to_minutes)

merged_df.to_csv('recipes_food_com.csv', index = False)
print(merged_df.info())