import json

with open('models/model_comparison_dashboard.json') as f:
    data = json.load(f)

print(f"Total entries in dashboard: {len(data)}")
for i, row in enumerate(data, 1):
    hazard = row.get('hazard') or row.get('hazard_type')
    task = row.get('task') or row.get('task_name')
    metric = row.get('primary_metric_name') or row.get('metric')
    score = row.get('test_score') if row.get('test_score') is not None else row.get('primary_test_score')
    baseline = row.get('baseline_score')
    status = row.get('operational_status') or row.get('governance_status')
    task_type = row.get('task_type')
    print(f"{i}. [{status}] {hazard} - {task} ({task_type})")
    print(f"   Metric: {metric} = {score} (Baseline: {baseline})")
    print(f"   Target: {row.get('target_column')}")
    print(f"   Notes: {row.get('governance_policy') or row.get('notes', 'None')}\n")
