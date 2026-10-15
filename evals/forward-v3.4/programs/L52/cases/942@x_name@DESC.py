from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

d = dfs[0].copy()
d['opening_year'] = pd.to_datetime(d['date_account_opened'], errors='coerce').dt.year
# The retained natural-language request explicitly asks for ascending x order.
p = d.groupby(['opening_year','other_account_details'], sort=True).size().unstack(fill_value=0).sort_index()
h.lines(plt, p, 'Accounts opened by year and details', 'Opening year', 'Number of accounts')
