from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

physicians, procedures, training = [d.copy() for d in dfs]
d = training.merge(procedures[procedures['Cost'].gt(5000)], left_on='Treatment', right_on='Code', how='inner').merge(physicians, left_on='Physician', right_on='EmployeeID', how='inner', suffixes=('_procedure','_physician'))
s = d.groupby('Name_physician', sort=True).size()
h.pie(plt, s, 'Training in procedures costing more than 5000, by physician')
