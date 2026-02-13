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
    """
    Generates a bounded, LLM-friendly directory tree representation.
    
    In Agentic Workflows, giving an LLM unbounded filesystem visibility often 
    leads to context-window exhaustion (Denial of Wallet/Service). This scout 
    tool provides a strictly bounded map of the environment, granting the agent 
    situational awareness while aggressively managing the token footprint.

    Args:
        root_dir (str): The starting directory path to profile.
        max_depth (int): The maximum traversal depth to prevent runaway recursion.
    """
    
    # 1. Guardrail: Fail fast and return a strict error to the Host Agent 
    # if the target is invalid, preventing silent hallucination loops.
    if not os.path.isdir(root_dir):
        print(f"ERROR: {root_dir} is not a directory.")
        sys.exit(1)

    # 2. Context Header: Provide a clear structural boundary for the LLM
    print(f"SCOUT REPORT for: {os.path.abspath(root_dir)}")
    print("=" * 40)

    # Calculate the baseline depth to determine relative depth during traversal
    root_depth = root_dir.rstrip(os.path.sep).count(os.path.sep)

    # 3. Traversal Loop
    for root, dirs, files in os.walk(root_dir):
        current_depth = root.count(os.path.sep) - root_depth
        
        # 4. Token Constraint Enforcement (The Circuit Breaker)
        # If we hit the max depth, we clear the `dirs` list IN-PLACE. 
        # This is a Python-specific trick that forces os.walk() to stop 
        # descending into subdirectories, saving compute and tokens.
        if current_depth >= max_depth:
            del dirs[:]
            continue

        # 5. Visual Hierarchy Formatting
        # Uses standard indentation so the LLM easily parses parent-child relationships
        indent = "  " * current_depth
        print(f"{indent}[DIR] {os.path.basename(root)}/")
        
        # 6. File Listing & Noise Reduction
        for file in files:
            # Drop hidden files/folders (e.g., .git, .env, .DS_Store). 
            # This prevents leaking secrets to the prompt and reduces token noise.
            if not file.startswith('.'):
                print(f"{indent}  - {file}")

    # 7. Context Footer: Explicitly signal the end of the tool's output to the LLM
    print("=" * 40)
    print("END OF REPORT")

if __name__ == "__main__":
    # 8. Command-Line Interface setup for the Host Agent execution layer
    parser = argparse.ArgumentParser(description="Bounded filesystem scout for Agentic context.")
    parser.add_argument("--directory", required=True, help="Target directory to profile.")
    
    # Default depth is kept intentionally shallow (2) to enforce the Principle of Least Context
    parser.add_argument("--depth", type=int, default=2, help="Max recursion depth (token safety limit).")
    args = parser.parse_args()
    
    generate_tree(args.directory, args.depth)
