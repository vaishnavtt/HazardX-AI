import urllib.request
import json

def check_models():
    req = urllib.request.urlopen('http://127.0.0.1:8000/api/v1/models')
    data = json.loads(req.read().decode('utf-8'))
    print(f"Total Models in Registry: {len(data['models'])}")
    for m in data['models']:
        print(f"  * [{m['operational_status']}] {m['hazard']} - {m['task_name']}")
        print(f"    - Type: {m['task_type']} | Target: {m['target_column']}")
        print(f"    - Metric: {m['primary_metric_name']} = {m['primary_test_score']}")
        print(f"    - Version: {m['model_version']}\n")

if __name__ == '__main__':
    check_models()
