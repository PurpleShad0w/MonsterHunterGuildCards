import pandas as pd
import dash
from dash import html
import numpy as np
import os

app = dash.Dash(__name__, assets_folder='assets')
get_asset_url = app.get_asset_url


df_raw = pd.read_csv(r'data/MHWI.tsv', sep='\t', names=['Variable', 'Value'])
df_raw = df_raw[df_raw['Variable'].str.startswith('Hunting Log')]
df_raw['Value'] = pd.to_numeric(df_raw['Value'], errors='coerce').fillna(0)

def parse_row(var):
	parts = var.split(' - ')
	if len(parts) == 3:
		return parts[1], parts[2]
	return None, None

parsed = df_raw['Variable'].apply(parse_row)
df_raw[['Metric', 'Monster']] = pd.DataFrame(parsed.tolist(), index=df_raw.index)


df_summary = (
	df_raw
	.pivot_table(index='Monster', columns='Metric', values='Value', aggfunc='sum', fill_value=0)
	.reset_index()
)

from assets.classification import monsters as category_map


monster_to_cat = {}
for cat, subcats in category_map.items():
	for subcat, monsters in subcats.items():
		for m in monsters:
			monster_to_cat[m] = (cat, subcat)

def safe_categories(monster):
	return monster_to_cat.get(monster, ('Misc', 'Misc'))

cat_expanded = df_summary['Monster'].apply(
	lambda m: pd.Series(safe_categories(m), index=['Cat', 'SubCat'])
)
df_summary = pd.concat([df_summary, cat_expanded], axis=1)

agg_dict = {
	'Hunted': 'sum',
	'Slain': 'sum',
	'Captured': 'sum',
	'Small Crown Size': 'min',
	'Large Crown Size': 'max',
	'Research Experience': 'sum',
	'Research Level': 'sum',
}

df_cat = df_summary.groupby('Cat').agg(agg_dict).reset_index()
df_subcat = df_summary.groupby(['Cat', 'SubCat']).agg(agg_dict).reset_index()


rows = []
for _, cat in df_cat.iterrows():
	rows.append({ 'level':0, 'Name': cat['Cat'], **{c:int(cat[c]) for c in agg_dict} })
	subs = df_subcat[df_subcat['Cat'] == cat['Cat']]
	for _, sub in subs.iterrows():
		rows.append({ 'level':1, 'Name': sub['SubCat'], **{c:int(sub[c]) for c in agg_dict} })
		monsters = df_summary[np.logical_and(
			df_summary['Cat'] == sub['Cat'],
			df_summary['SubCat'] == sub['SubCat']
		)]
		for _, m in monsters.iterrows():
			rows.append({ 'level':2, 'Name': m['Monster'], **{c:int(m[c]) for c in agg_dict} })

df_display = pd.DataFrame(rows)


base_cell = {'border':'1px solid #ccc','padding':'8px'}
header_style = {**base_cell,'backgroundColor':'#f8f8f8','fontWeight':'bold'}
icon_cell = {**base_cell,'width':'10px'}
name_cell = {**base_cell,'textAlign':'left'}
number_cell = {**base_cell,'textAlign':'right'}
level_bg = {0:'#e0e0e0',1:'#f0f0f0',2:'#ffffff'}


def render_row(row):
	icon_rel_path = f"icons/MHWI/{row['Name']}.png"
	icon_fs_path = os.path.join('assets', icon_rel_path)
	if os.path.isfile(icon_fs_path):
		icon = html.Img(src=get_asset_url(icon_rel_path), height='30px')
	else:
		icon = ''
	padded_name = {'paddingLeft': f"10px"}
	name_style = {**name_cell, **padded_name, 'fontWeight': 'bold' if row['level']<2 else 'normal'}
	cells = [
		html.Td(icon, style=icon_cell),
		html.Td(row['Name'], style=name_style),
		html.Td(row['Hunted'], style=number_cell),
		html.Td(row['Slain'], style=number_cell),
		html.Td(row['Captured'], style=number_cell),
		html.Td(row['Small Crown Size'], style=number_cell),
		html.Td(row['Large Crown Size'], style=number_cell),
		html.Td(row['Research Experience'], style=number_cell),
		html.Td(row['Research Level'], style=number_cell),
	]
	return html.Tr(cells, style={'backgroundColor': level_bg.get(row['level'], '#fff')})


app.layout = html.Div([
	html.H1('Monster Hunting Log'),
	html.Table([
		html.Thead(html.Tr([
			html.Th('', style=header_style),
			html.Th('Name', style=header_style),
			html.Th('Hunted', style={**header_style,'textAlign':'right'}),
			html.Th('Slain', style={**header_style,'textAlign':'right'}),
			html.Th('Captured', style={**header_style,'textAlign':'right'}),
			html.Th('Small Size', style={**header_style,'textAlign':'right'}),
			html.Th('Large Size', style={**header_style,'textAlign':'right'}),
			html.Th('Research XP', style={**header_style,'textAlign':'right'}),
			html.Th('Research Level', style={**header_style,'textAlign':'right'}),
		])),
		html.Tbody([render_row(r) for _, r in df_display.iterrows()])
	], style={'width':'100%','borderCollapse':'collapse'})
])

app.run()