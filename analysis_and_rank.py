import pandas as pd

df = pd.read_csv('house_full_info.csv')

#convert the rent column to integer
df['rent'] = df['rent'].str.replace('$', '').str.replace(',', '').str.replace('/mo', '').str.replace('+', '').astype(float)
#convert the number of beds column to integer  
df['number of beds'] = df['number of beds'].str.replace('beds', '').astype(float)
#convert the number of baths column to integer
df['number of baths'] = df['number of baths'].str.replace('baths', '').astype(float)
#convert the size column to integer
df['size'] = df['size'].str.replace('sqft', '').str.replace(',', '').astype(float)

df['school1_score'] = df['school1_score'].astype(float)

#insert a column to the dataframe which is the result of rent/size
df['rent/size'] = df['rent'] / df['size']

#insert a column to the dataframe which is the result of average walk score transit score and bike score
df['average transit score'] = (df['walk_score'] + df['transit_score'] + df['bike_score']) / 3

#replace na values with 0
df['school1_score'].fillna(0, inplace=True)
df['school2_score'].fillna(0, inplace=True)
df['school3_score'].fillna(0, inplace=True)

#insert a column to the dataframe which is the result of total school scores
df['total school score'] = df['school1_score'] + df['school2_score'] + df['school3_score']

#create a weighted average formula to calculate the final score for each entry in the dataframe, the weight of the total school score is 50 percent, the weight of the average transit score is 15 percent, and the weight of the rent/size is 35 percent

df['rent/size Normalized'] = (1 - (df['rent/size'] - df['rent/size'].min()) / (df['rent/size'].max() - df['rent/size'].min()))

df['total school score Normalized'] = (df['total school score'] - df['total school score'].min()) / (df['total school score'].max() - df['total school score'].min())

df['average transit score Normalized'] = (df['average transit score'] - df['average transit score'].min()) / (df['average transit score'].max() - df['average transit score'].min())

df['final score'] = 0.5 * df['rent/size Normalized'] + 0.15 * df['average transit score Normalized'] + 0.35 * df['total school score Normalized']

df['final score without transit'] = 0.3 * df['rent/size Normalized'] + 0.7 * df['total school score Normalized']

#return the top 10 entries in the dataframe with highest final score
print(df.nlargest(10, 'final score')['link'])
print(df.nlargest(10, 'final score without transit')['link'])
#save the dataframe to a csv file
df.to_csv('house_full_information_formatted.csv', index=False)

#save the dataframe to an excel file
df.to_excel('house_full_information_formatted.xlsx', index=False)

