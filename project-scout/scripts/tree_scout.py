#!/usr/bin/env python3
# =============================================================================
# COMPONENT: stateful-data-profiler
# -----------------------------------------------------------------------------
# Copyright 2026 Shuva Jyoti Kar
# License: Apache 2.0
# =============================================================================
import os
import argparse
import sys

def generate_tree(root_dir, max_depth):
    if not os.path.isdir(root_dir):
        print(f"ERROR: {root_dir} is not a directory.")
        sys.exit(1)

    print(f"SCOUT REPORT for: {os.path.abspath(root_dir)}")
    print("=" * 40)

    root_depth = root_dir.rstrip(os.path.sep).count(os.path.sep)

    for root, dirs, files in os.walk(root_dir):
        current_depth = root.count(os.path.sep) - root_depth
        if current_depth >= max_depth:
            del dirs[:]
            continue

        indent = "  " * current_depth
        print(f"{indent}[DIR] {os.path.basename(root)}/")
        for file in files:
            if not file.startswith('.'):
                print(f"{indent}  - {file}")

    print("=" * 40)
    print("END OF REPORT")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", required=True)
    parser.add_argument("--depth", type=int, default=2)
    args = parser.parse_args()
    
    generate_tree(args.directory, args.depth)
