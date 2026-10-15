from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

skills, faults, requirements = [d.copy() for d in dfs]
d = requirements.merge(skills, on='skill_id', how='inner').merge(faults, on='part_fault_id', how='inner')
p = d.groupby(['skill_description','fault_short_name'], sort=True).size().unstack(fill_value=0)
p = p.loc[p.sum(axis=1).sort_values(ascending=False, kind='stable').index]
h.stacked(plt, p, 'Faults by required skill and short name', 'Skill description', 'Number of faults')
