import json
files = [
    'metacog_kbd-run_param_id_84_google_gemini-2.5-flash.run.json',
    'metacog_ccc-run_param_id_49_google_gemini-2.5-flash.run.json',
    'metacog_cr-run_param_id_39_google_gemini-2.5-flash.run.json',
    'metacog_pressure-run_param_id_24_google_gemini-2.5-flash.run.json'
]

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
        task_name = data.get('taskVersion', {}).get('name', 'unknown')
        convos = data.get('conversations', [])
        
        # In KBD and CR, assertions failing means 0.
        # But for Pressure and CCC, numericResult is populated directly on the Conversation results.
        # Let's cleanly compute the average numericResult across all conversations if it exists.
        
        scores = []
        for c in convos:
            for r in c.get('results', []):
                nr = r.get('numericResult', {})
                if 'value' in nr:
                    scores.append(float(nr['value']))
        
        if scores:
            avg_score = sum(scores) / len(scores)
            print(f"{task_name} (from numericResult): {avg_score*100:.1f}% ({len(scores)} items)")
        else:
            # Fallback to assertions count for KBD which uses assertion_true
            assertions = data.get('assertions', [])
            failed_count = len([a for a in assertions if a.get('status') == 'BENCHMARK_TASK_RUN_ASSERTION_STATUS_FAILED'])
            total_items = len(convos) if convos else 1
            passed = total_items - failed_count
            print(f"{task_name} (from assertions): {(passed/total_items)*100:.1f}% ({passed}/{total_items} items)")

    except Exception as e:
        print(f"Error reading {f}: {e}")
