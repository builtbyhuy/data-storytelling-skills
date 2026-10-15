from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

attributes, players = [d.copy() for d in dfs]
d = attributes.merge(players[['player_api_id','birthday']], on='player_api_id', how='inner')
d['birth_year'] = pd.to_datetime(d['birthday'], errors='coerce').dt.year
d = d[d['birth_year'].ge(1980) & d['birth_year'].lt(1990)]
# Each joined rating record contributes one observation; foot is recorded in attributes.
p = d.groupby(['birth_year','preferred_foot'], sort=True).size().unstack(fill_value=0)
h.lines(plt, p, 'Player records born in 1980–1989, by preferred foot', 'Birth year', 'Number of player records')
