from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

genres, tracks = [d.copy() for d in dfs]
d = tracks.merge(genres, left_on='genre_id', right_on='id', how='inner', suffixes=('_track','_genre'))
s = d.groupby('name_genre', sort=True).size().sort_values(ascending=False, kind='stable').head(5)
h.pie(plt, s, 'Top 5 genres by number of tracks')
