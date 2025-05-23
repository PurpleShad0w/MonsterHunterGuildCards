import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import numpy as np
import os


app = dash.Dash(__name__, assets_folder='assets')
get_asset_url = app.get_asset_url

ASSETS_DIR = os.path.join(os.getcwd(), 'assets')


from assets.classification import monsters as category_map


def parse_row(var):
	parts = var.split(' - ')
	return (parts[1], parts[2]) if len(parts) == 3 else (None, None)


monster_to_cat = {}
for cat, subcats in category_map.items():
	for subcat, monsters in subcats.items():
		if isinstance(monsters, dict):
			for subsubcat, mon_list in monsters.items():
				for m in mon_list:
					monster_to_cat[m] = (cat, subcat, subsubcat)
		else:
			for m in monsters:
				monster_to_cat[m] = (cat, subcat, None)

def safe_categories(monster):
	return monster_to_cat.get(monster, ('Undefined', 'Undefined', 'Undefined'))


DATASETS = {
	'Monster Hunter Series': {
		'files': [
			'data/Monster Hunter Rise Sunbreak.tsv',
			'data/Monster Hunter World Iceborne.tsv'
		],
		'icon_folders': [
			'icons/Monster Hunter Wilds',
			'icons/Monster Hunter Rise Sunbreak',
			'icons/Monster Hunter World Iceborne',
			'icons/Monster Hunter Generations Ultimate'
		],
		'agg': {
			'Hunted': 'sum',
			'Slain': 'sum',
			'Captured': 'sum',
		},
		'display_names': {
			'Hunted': 'Hunted',
			'Slain': 'Slain',
			'Captured': 'Captured',
		},
	},

	'Monster Hunter Rise Sunbreak': {
		'files': ['data/Monster Hunter Rise Sunbreak.tsv'],
		'icon_folders': ['icons/Monster Hunter Rise Sunbreak'],
		'agg': {
			'Hunted': 'sum',
			'Slain': 'sum',
			'Captured': 'sum',
			'Anomaly Hunts': 'sum',
			'Special Investigation Completed': 'all',
		},
		'display_names': {
			'Hunted': 'Hunted',
			'Slain': 'Slain',
			'Captured': 'Captured',
			'Anomaly Hunts': 'Anomaly Hunts',
			'Special Investigation Completed': 'Spec. Invest. Completed',
		},
	},

	'Monster Hunter World Iceborne': {
		'files': ['data/Monster Hunter World Iceborne.tsv'],
		'icon_folders': ['icons/Monster Hunter World Iceborne'],
		'agg': {
			'Hunted': 'sum',
			'Slain': 'sum',
			'Captured': 'sum',
			'Small Crown Size': 'min',
			'Large Crown Size': 'max',
			'Research Experience': 'sum',
			'Research Level': 'sum',
		},
		'display_names': {
			'Hunted': 'Hunted',
			'Slain': 'Slain',
			'Captured': 'Captured',
			'Small Crown Size': 'Smallest Size',
			'Large Crown Size': 'Largest Size',
			'Research Experience': 'Research XP',
			'Research Level': 'Research Level',
		},
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

def generate_table(dataset_key, dark_mode=False):
	cfg = DATASETS[dataset_key]
	agg_map = cfg['agg']
	display_names = cfg.get('display_names', {})

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
		lambda m: pd.Series(safe_categories(m), index=['Cat', 'SubCat', 'SubSubCat'])
	)
	df_summary = pd.concat([df_summary, cat_expanded], axis=1)

	df_cat = df_summary.groupby('Cat').agg(agg_map).reset_index()
	df_subcat = df_summary.groupby(['Cat', 'SubCat']).agg(agg_map).reset_index()
	df_subsubcat = df_summary.groupby(['Cat', 'SubCat', 'SubSubCat']).agg(agg_map).reset_index()

	def build_row(level, name, df, match_filter, metrics):
		filtered = df.loc[match_filter]
		if not filtered.empty:
			row_data = filtered.iloc[0]
			return {'level': level, 'Name': name, **{m: int(row_data[m]) for m in metrics}}
		else:
			return {'level': level, 'Name': name, **{m: 0 for m in metrics}}

	rows = []
	for cat in category_map:
		rows.append(build_row(0, cat, df_cat, df_cat['Cat'] == cat, agg_map))

		for subcat in category_map[cat]:
			rows.append(build_row(1, subcat, df_subcat, 
				(df_subcat['Cat'] == cat) & (df_subcat['SubCat'] == subcat), agg_map))
			
			submap = category_map[cat][subcat]

			if isinstance(submap, dict):
				for subsub in submap:
					rows.append(build_row(2, subsub, df_subsubcat,
						(df_subsubcat['Cat'] == cat) & (df_subsubcat['SubCat'] == subcat) & (df_subsubcat['SubSubCat'] == subsub),
						agg_map))

					for mon in submap[subsub]:
						rows.append(build_row(3, mon, df_summary,
							df_summary['Monster'] == mon,
							agg_map))
			else:
				for mon in submap:
					rows.append(build_row(3, mon, df_summary,
						df_summary['Monster'] == mon,
						agg_map))

	df_display = pd.DataFrame(rows)

	if dark_mode:
		page_bg = '#121212'
		text_color = '#E0E0E0'
		border_color = '#333333'
		level_bg = {0: '#263238', 1: '#37474f', 2: '#455a64', 3: '#546e7a'}

	else:
		page_bg = '#ffffff'
		text_color = '#000000'
		border_color = '#ccc'
		level_bg = {0: '#4a6741', 1: '#7f9c6b', 2: '#b6c9a6', 3: '#e9f2e3',}

	base_cell = {'border': f'1px solid {border_color}', 'padding': '8px', 'color': text_color}
	icon_cell = {**base_cell, 'width': '10px', 'textAlign': 'center'}
	name_cell = {**base_cell, 'textAlign': 'left'}
	number_cell = {**base_cell, 'textAlign': 'right'}

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

		font_weight = 'bold' if row['level'] == 0 or row['level'] == 2 else 'normal'
		font_style = 'italic' if row['level'] == 1 else 'normal'
		name_style = {**name_cell, 'paddingLeft': "10px", 'fontWeight': font_weight, 'fontStyle': font_style}
		cells = [html.Td(icon, style=icon_cell), html.Td(row['Name'], style=name_style)]
		cells += [html.Td(row[col], style=number_cell) for col in agg_map]
		return html.Tr(cells, style={'backgroundColor': level_bg[row['level']]})

	header_cells = [html.Th('', style=base_cell), html.Th('Name', style=base_cell)] + [
		html.Th(display_names.get(col, col), style={**base_cell, 'textAlign': 'right'}) for col in agg_map
	]

	table = html.Table([
		html.Thead(html.Tr(header_cells)),
		html.Tbody([render_row(r) for _, r in df_display.iterrows()])
	], style={'width':'100%', 'borderCollapse':'collapse'})

	return html.Div(table, style={'backgroundColor': page_bg, 'padding':'20px'})


app.layout = html.Div(id='page-container', children=[
	dcc.Store(id='dark-mode-store', data={'dark': True}),
	html.Div(id='page-header', style={
		'display': 'flex',
		'justifyContent': 'space-between',
		'alignItems': 'center',
		'marginBottom': '5px'
	}, children=[
		html.Div([
			html.Button('Light Mode', id='dark-mode-button', n_clicks=0, style={'marginRight': '15px'}),
			html.H1('Monster Hunting Log', id='page-title', style={'margin': '0', 'marginLeft': '15px'})
		], style={'display': 'flex', 'alignItems': 'center'}),
		dcc.Dropdown(
			id='dataset-dropdown',
			options=[{'label': k, 'value': k} for k in DATASETS],
			value='Monster Hunter Series',
			clearable=False,
			style={'width': '350px'}
		)
	]),
	html.Div(id='table-container')
], style={'minHeight': '100vh', 'margin': '0', 'padding': '20px'})


@app.callback(
	[Output('table-container', 'children'),
	Output('page-container', 'style'),
	Output('page-title', 'style'),
	Output('dark-mode-store', 'data'),
	Output('dark-mode-button', 'children'),
	Output('dark-mode-button', 'style')],
	[Input('dataset-dropdown', 'value'),
	Input('dark-mode-button', 'n_clicks')],
	[State('dark-mode-store', 'data')]
)

def update(selected_dataset, n_clicks, store):
	ctx = dash.callback_context
	dark = store.get('dark', False)
	if ctx.triggered and ctx.triggered[0]['prop_id'].startswith('dark-mode-button'):
		dark = not dark

	page_style = {
		'backgroundColor': '#121212' if dark else '#ffffff',
		'minHeight': '100vh', 'margin': '0', 'padding': '20px'
	}

	title_style = {
		'margin': '0', 'marginLeft': '15px',
		'color': '#E0E0E0' if dark else '#000000'
	}

	btn_label = 'Light Mode' if dark else 'Dark Mode'
	btn_style = {
		'height': '30px', 'width': '100px', 'borderRadius': '15px', 'border': 'none',
		'cursor': 'pointer',
		'backgroundColor': '#37474f' if dark else '#e0e0e0',
		'color': '#ffffff' if dark else '#000000',
		'marginRight': '15px'
	}

	return (
		generate_table(selected_dataset, dark),
		page_style,
		title_style,
		{'dark': dark},
		btn_label,
		btn_style
	)

app.run()