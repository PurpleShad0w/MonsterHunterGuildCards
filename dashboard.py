import pandas as pd
import plotly.express as px

df = pd.read_csv(r'processing/processed_sunbreak.tsv', sep='\t')


weapons = df[df['Variable'].str.startswith('Weapon Usage - ')].copy()
weapons['Variable'] = weapons['Variable'].str.replace('Weapon Usage - ', '', regex=False)
weapons = weapons.sort_values(by=['Value'])

fig = px.bar(weapons, x='Variable', y='Value', color='Variable', barmode='group')
fig.update_yaxes(type="log")
fig.update_traces(width=0.6)
fig.show()