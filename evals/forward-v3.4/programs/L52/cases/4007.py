from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

accelerators, browsers, compatibility = [d.copy() for d in dfs]
d = compatibility.merge(accelerators[['id','name']], left_on='accelerator_id', right_on='id', how='inner').merge(browsers[['id','name']], left_on='browser_id', right_on='id', how='inner', suffixes=('_accelerator','_browser'))
p = d.groupby(['name_browser','name_accelerator'], sort=True).size().unstack(fill_value=0)
h.stacked(plt, p, 'Compatible accelerators by browser', 'Browser', 'Number of compatible accelerators')
