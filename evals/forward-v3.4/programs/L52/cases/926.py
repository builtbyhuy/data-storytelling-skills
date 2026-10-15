from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

d = dfs[0].copy()
s = d.groupby('other_account_details', sort=True).size()
h.bar(plt, s, 'Accounts by account details', 'Other account details', 'Number of accounts')
