from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

d = dfs[0].copy()
p = d.groupby(['Industry','Headquarters'], sort=True).size().unstack(fill_value=0)
p = p.loc[p.sum(axis=1).sort_values(ascending=False, kind='stable').index]
h.stacked(plt, p, 'Company counts by industry and headquarters', 'Industry', 'Number of headquarters records')
