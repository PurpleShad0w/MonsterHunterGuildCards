import pandas as pd
import dash
from dash import html

app = dash.Dash(__name__, assets_folder='assets')
get_asset_url = app.get_asset_url

df_raw = pd.read_csv('processing/processed_iceborne.tsv', sep='\t', names=['Variable', 'Value'])
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

icon_map = {
	'Anjanath': r'icons/MHWI Anjanath.png',
	'Diablos': r'icons/MHWI Diablos.png',
	'Black Diablos': r'icons/MHWI Black Diablos.png',
}

category_map = { # all wrong, only for testing
	'Anjanath': ['Brute Wyverns', 'Anjanath Family'],
	'Fulgur Anjanath': ['Brute Wyverns', 'Anjanath Family'],
	'Diablos': ['Wyverns', 'Diablos Family'],
	'Black Diablos': ['Wyverns', 'Diablos Family'],
	'Kirin': ['Elder Dragons', 'Kirin Family'],
	'Glavenus': ['Brute Wyverns', 'Glavenus Family'],
	'Acidic Glavenus': ['Brute Wyverns', 'Glavenus Family'],
}

def safe_categories(monster):
	mapping = category_map.get(monster)
	return mapping if isinstance(mapping, list) and len(mapping) == 2 else ['Unknown', 'Unknown']

df_summary['IconFile'] = df_summary['Monster'].map(icon_map)
cat_expanded = df_summary['Monster'].apply(
	lambda m: pd.Series(safe_categories(m), index=['Cat','SubCat'])
)
df_summary = pd.concat([df_summary, cat_expanded], axis=1)

group_cols = ['Hunted', 'Slain', 'Captured']
cat_totals = df_summary.groupby('Cat')[group_cols].sum().reset_index()
subcat_totals = df_summary.groupby(['Cat','SubCat'])[group_cols].sum().reset_index()

rows = []
for _, cat in cat_totals.iterrows():
	rows.append({ 'level':0, 'Name':cat['Cat'], 'IconFile':None, **{c:int(cat[c]) for c in group_cols} })
	subs = subcat_totals[subcat_totals['Cat']==cat['Cat']]
	for _, sub in subs.iterrows():
		rows.append({ 'level':1, 'Name':sub['SubCat'], 'IconFile':None, **{c:int(sub[c]) for c in group_cols} })
		monsters = df_summary[(df_summary['Cat']==cat['Cat']) & (df_summary['SubCat']==sub['SubCat'])]
		for _, m in monsters.iterrows():
			rows.append({ 'level':2, 'Name':m['Monster'], 'IconFile':m['IconFile'], **{c:int(m[c]) for c in group_cols} })

df_display = pd.DataFrame(rows)

base_cell = {'border':'1px solid #ccc','padding':'8px'}
header_style = {**base_cell,'backgroundColor':'#f8f8f8','fontWeight':'bold'}
icon_cell = {**base_cell,'width':'10px'}
name_cell = {**base_cell,'textAlign':'left','paddingLeft':'24px'}
number_cell = {**base_cell,'textAlign':'right'}

level_bg = {0:'#e0e0e0', 1:'#f0f0f0', 2:'#ffffff'}

def render_row(row):
	if row['level']==2 and isinstance(row['IconFile'], str):
		icon = html.Img(src=get_asset_url(row['IconFile']), height='30px')
	else:
		icon = ''
	cells = [
		html.Td(icon, style=icon_cell),
		html.Td(row['Name'], style={**name_cell, 'fontWeight':'bold' if row['level']<2 else 'normal'}),
		html.Td(row['Hunted'], style=number_cell),
		html.Td(row['Slain'], style=number_cell),
		html.Td(row['Captured'], style=number_cell)
	]
	return html.Tr(cells, style={'backgroundColor': level_bg.get(row['level'], '#fff')})

app.layout = html.Div([
	html.H1('Monster Hunting Log'),
	html.Table([
		html.Thead(html.Tr([
			html.Th('Icon', style=header_style),
			html.Th('Name', style=header_style),
			html.Th('Hunted', style={**header_style,'textAlign':'right'}),
			html.Th('Slain', style={**header_style,'textAlign':'right'}),
			html.Th('Captured',style={**header_style,'textAlign':'right'})
		])),
		html.Tbody([render_row(r) for _, r in df_display.iterrows()])
	], style={'width':'100%','borderCollapse':'collapse'})
])

app.run()