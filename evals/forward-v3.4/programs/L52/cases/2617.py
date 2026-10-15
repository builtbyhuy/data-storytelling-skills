from pathlib import Path
import importlib.util
_helper_path = Path(__file__).resolve().parents[1] / "chart_helpers.py"
_spec = importlib.util.spec_from_file_location("local_chart_helpers", _helper_path)
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

d = dfs[0].copy()
d = d[pd.to_numeric(d['amount_paid'], errors='coerce').gt(300) | d['payment_type_code'].eq('Check')]
s = d.groupby('payment_date', sort=True).size()
fig, ax = h.frame(plt, 'Payments over 300 or by Check, by timestamp', 'Payment date', 'Number of payments')
ax.plot(s.index.astype(str), s.to_numpy(), marker='o')
ax.tick_params(axis='x', labelrotation=45)
ax.set_ylim(bottom=0)
h.finish(fig, ax, 'line')
