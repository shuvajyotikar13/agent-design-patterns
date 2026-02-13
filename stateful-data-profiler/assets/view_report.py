#!/usr/bin/env python3
# =============================================================================
# COMPONENT: stateful-data-profiler
# -----------------------------------------------------------------------------
# Copyright 2026 Shuva Jyoti Kar
# License: Apache 2.0
# =============================================================================
import json
import os  
import datetime

CACHE_FILE = ".antigravity_data_cache.json"

def render_report():
    if not os.path.exists(CACHE_FILE):
        print("No knowledge base found. Run the analyzer first.")
        return

    try:
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
    except json.JSONDecodeError:
        print("Error: Cache file is corrupt.")
        return

    # The Presentation Layer
    print("\n# 📚 The Librarian's Report")
    print(f"*Generated at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
    
    # Table Header
    print(f"| {'Filename':<30} | {'Status':<10} | {'Summary':<50} |")
    print(f"|{'-'*32}|{'-'*12}|{'-'*52}|")

    file_count = 0
    for filepath, data in cache.items():
        filename = os.path.basename(filepath)
        # Truncate long filenames for display
        if len(filename) > 28:
            filename = filename[:25] + "..."
            
        summary = data.get('summary', 'No summary available.')
        # Truncate long summaries
        if len(summary) > 48:
            summary = summary[:45] + "..."

        print(f"| {filename:<30} | {'Cached':<10} | {summary:<50} |")
        file_count += 1

    print(f"\n**Total Files Tracked:** {file_count}")

if __name__ == "__main__":
    render_report()
