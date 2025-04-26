import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import numpy as np
import os


app = dash.Dash(__name__, assets_folder='assets')
get_asset_url = app.get_asset_url

ASSETS_DIR = os.path.join(os.getcwd(), 'assets')


from assets.classification import monsters as category_map


def parse_row(var):
	parts = var.split(' - ')
	return (parts[1], parts[2]) if len(parts) == 3 else (None, None)


monster_to_cat = {
	m: (cat, subcat)
	for cat, subcats in category_map.items()
	for subcat, monsters in subcats.items()
	for m in monsters
}

def safe_categories(monster):
	return monster_to_cat.get(monster, ('Undefined', 'Undefined'))


DATASETS = {
	'all': {
		'files': ['data/MHWI.tsv', 'data/MHRS.tsv'],
		'icon_folders': ['icons/MHWI', 'icons/MHRS'],
		'agg': {
			'Hunted': 'sum',
			'Slain': 'sum',
			'Captured': 'sum',
		}
	},

	'MHWI': {
		'files': ['data/MHWI.tsv'],
		'icon_folders': ['icons/MHWI'],
		'agg': {
			'Hunted': 'sum',
			'Slain': 'sum',
			'Captured': 'sum',
			'Small Crown Size': 'min',
			'Large Crown Size': 'max',
			'Research Experience': 'sum',
			'Research Level': 'sum',
		}
	},

	'MHRS': {
		'files': ['data/MHRS.tsv'],
		'icon_folders': ['icons/MHRS'],
		'agg': {
			'Hunted': 'sum',
			'Slain': 'sum',
			'Captured': 'sum',
			'Anomaly Hunts': 'sum',
			'Special Investigation Completed': 'all',
		}
	},
}


icon_available = {}
for cfg in DATASETS.values():
	for folder in cfg['icon_folders']:
		full_path = os.path.join(ASSETS_DIR, folder)
		try:
			icon_available[folder] = set(os.listdir(full_path))
		except FileNotFoundError:
			icon_available[folder] = set()

def generate_table(dataset_key):
	cfg = DATASETS[dataset_key]
	agg_map = cfg['agg']

	frames = []
	for f in cfg['files']:
		df = pd.read_csv(f, sep='\t', names=['Variable', 'Value'])
		df = df[df['Variable'].str.startswith('Hunting Log')]
		df['Value'] = pd.to_numeric(df['Value'], errors='coerce').fillna(0)
		frames.append(df)
	df_raw = pd.concat(frames, ignore_index=True)

	parsed = df_raw['Variable'].apply(parse_row)
	df_raw[['Metric', 'Monster']] = pd.DataFrame(parsed.tolist(), index=df_raw.index)

	df_summary = (
		df_raw
		.pivot_table(index='Monster', columns='Metric', values='Value',aggfunc='sum', fill_value=0)
		.reset_index()
	)

	cat_expanded = df_summary['Monster'].apply(
		lambda m: pd.Series(safe_categories(m), index=['Cat', 'SubCat'])
	)
	df_summary = pd.concat([df_summary, cat_expanded], axis=1)

	df_cat = df_summary.groupby('Cat').agg(agg_map).reset_index()
	df_subcat = df_summary.groupby(['Cat', 'SubCat']).agg(agg_map).reset_index()

	rows = []
	for _, cat in df_cat.iterrows():
		rows.append({ 'level': 0, 'Name': cat['Cat'], **{c: int(cat[c]) for c in agg_map} })
		subs = df_subcat[df_subcat['Cat'] == cat['Cat']]
		for _, sub in subs.iterrows():
			rows.append({ 'level': 1, 'Name': sub['SubCat'], **{c: int(sub[c]) for c in agg_map} })
			monsters = df_summary[(df_summary['Cat'] == sub['Cat']) & (df_summary['SubCat'] == sub['SubCat'])]
			for _, m in monsters.iterrows():
				rows.append({ 'level': 2, 'Name': m['Monster'], **{c: int(m[c]) for c in agg_map} })
	df_display = pd.DataFrame(rows)

	base_cell = {'border': '1px solid #ccc', 'padding': '8px'}
	icon_cell = {**base_cell, 'width': '10px'}
	name_cell = {**base_cell, 'textAlign': 'left'}
	number_cell = {**base_cell, 'textAlign': 'right'}
	level_bg = {0: '#e0e0e0', 1: '#f0f0f0', 2: '#ffffff'}

	def render_row(row):
		found_src = None
		filename = f"{row['Name']}.png"
		for folder in cfg['icon_folders']:
			if filename in icon_available.get(folder, []):
				found_src = get_asset_url(f"{folder}/{filename}")
				break
		if not found_src:
			found_src = get_asset_url('icons/Question Mark.png')
		icon = html.Img(src=found_src, height='30px')

		name_style = {**name_cell, 'paddingLeft': "10px", 'fontWeight': 'bold' if row['level'] < 2 else 'normal'}
		cells = [html.Td(icon, style=icon_cell), html.Td(row['Name'], style=name_style)]
		cells += [html.Td(row[col], style=number_cell) for col in agg_map]
		return html.Tr(cells, style={'backgroundColor': level_bg[row['level']]})

	header_cells = [html.Th('', style=base_cell), html.Th('Name', style=base_cell)] + [
		html.Th(col, style={**base_cell, 'textAlign': 'right'}) for col in agg_map
	]

	return html.Table([
		html.Thead(html.Tr(header_cells)),
		html.Tbody([render_row(r) for _, r in df_display.iterrows()])
	], style={'width': '100%', 'borderCollapse': 'collapse'})


app.layout = html.Div([
	html.Div([
		html.H1('Monster Hunting Log', style={'margin': '0'}),
		dcc.Dropdown(
			id='dataset-dropdown',
			options=[
				{'label': 'All', 'value': 'all'},
				{'label': 'MHWI', 'value': 'MHWI'},
				{'label': 'MHRS', 'value': 'MHRS'},
			],
			value='all',
			clearable=False,
			style={'width': '200px'}
		)
	], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '20px'}),
	html.Div(id='table-container')
])


@app.callback(Output('table-container', 'children'), Input('dataset-dropdown', 'value'))
def update_table(selected_dataset):
	return generate_table(selected_dataset)

app.run()