import pandas as pd

df = pd.read_csv(r'processing/raw_sunbreak.tsv', sep='\t')


df.loc[len(df)] = ['Total Monsters Slain', int(df.loc[df['Variable'] == 'Total Monsters Hunted', 'Value'].values[0]) - int(df.loc[df['Variable'] == 'Total Monsters Captured', 'Value'].values[0])]

df.loc[len(df)] = ['Play Time (hrs)', float(df.loc[df['Variable'] == 'Play Time (s)', 'Value'].values[0]) / 3600]
df.loc[len(df)] = ['Time Spent on Canyne (hrs)', float(df.loc[df['Variable'] == 'Time Spent on Canyne (s)', 'Value'].values[0]) / 3600]

hunted = df[df['Variable'].str.startswith('Hunting Log - Hunted -')]
captured = df[df['Variable'].str.startswith('Hunting Log - Captured -')]
hunted = hunted.copy()
captured = captured.copy()
hunted['Monster'] = hunted['Variable'].str.replace('Hunting Log - Hunted - ', '', regex=False)
captured['Monster'] = captured['Variable'].str.replace('Hunting Log - Captured - ', '', regex=False)
merged = pd.merge(hunted[['Monster', 'Value']], captured[['Monster', 'Value']], on='Monster', suffixes=('_Hunted', '_Captured'))
merged['Slain'] = merged['Value_Hunted'].astype(int) - merged['Value_Captured'].astype(int)

for _, row in merged.iterrows():
	new_variable = f'Hunting Log - Slain - {row["Monster"]}'
	df.loc[len(df)] = [new_variable, row['Slain']]


df = df.sort_values(by=['Variable'])
df.to_csv(r'processing/processed_sunbreak.tsv', sep='\t', index=False)


df = pd.read_csv(r'processing/raw_iceborne.tsv', sep='\t')


df.loc[len(df)] = ['Play Time (hrs)', float(df.loc[df['Variable'] == 'Play Time (s)', 'Value'].values[0]) / 3600]
df.loc[len(df)] = ['Time Spent in the Guiding Lands (hrs)', float(df.loc[df['Variable'] == 'Time Spent in the Guiding Lands (s)', 'Value'].values[0]) / 3600]

slain = df[df['Variable'].str.startswith('Hunting Log - Slain -')]
captured = df[df['Variable'].str.startswith('Hunting Log - Captured -')]
slain = slain.copy()
captured = captured.copy()
slain['Monster'] = slain['Variable'].str.replace('Hunting Log - Slain - ', '', regex=False)
captured['Monster'] = captured['Variable'].str.replace('Hunting Log - Captured - ', '', regex=False)
merged = pd.merge(slain[['Monster', 'Value']], captured[['Monster', 'Value']], on='Monster', suffixes=('_Slain', '_Captured'))
merged['Hunted'] = merged['Value_Slain'].astype(int) + merged['Value_Captured'].astype(int)

for _, row in merged.iterrows():
	new_variable = f'Hunting Log - Hunted - {row["Monster"]}'
	df.loc[len(df)] = [new_variable, row['Hunted']]


df = df.sort_values(by=['Variable'])
df.to_csv(r'processing/processed_iceborne.tsv', sep='\t', index=False)