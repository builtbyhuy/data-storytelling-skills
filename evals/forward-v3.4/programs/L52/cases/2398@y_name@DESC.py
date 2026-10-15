from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

movies, ratings = [d.copy() for d in dfs]
d = movies[movies['director'].notna()].merge(ratings, on='mID', how='inner')
s = d.groupby('director', sort=True)['stars'].max().sort_values(ascending=False, kind='stable')
h.bar(plt, s, 'Highest movie rating by director', 'Director', 'Highest rating (stars)')
