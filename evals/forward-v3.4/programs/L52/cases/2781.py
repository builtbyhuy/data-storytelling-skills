from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

attributes, players = [d.copy() for d in dfs]
d = attributes[pd.to_numeric(attributes['overall_rating'], errors='coerce').ge(75)].merge(players[['player_api_id','birthday']], on='player_api_id', how='inner')
d['birth_year'] = pd.to_datetime(d['birthday'], errors='coerce').dt.year
p = d.groupby(['birth_year','preferred_foot'], sort=True).size().unstack(fill_value=0)
h.lines(plt, p, 'Player records rated at least 75, by birth year and foot', 'Birth year', 'Number of player records')
