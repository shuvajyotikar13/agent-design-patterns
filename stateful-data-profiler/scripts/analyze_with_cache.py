#!/usr/bin/env python3
# =============================================================================
# COMPONENT: stateful-data-profiler
# -----------------------------------------------------------------------------
# Copyright 2026 Shuva Jyoti Kar
# License: Apache 2.0
# =============================================================================
"""
Stateful Data Profiler (Memory & Cognitive Caching)
===================================================

Overview:
---------
In Agentic Systems, the LLM often acts as a data analyst. A naive agent will 
repeatedly execute commands like `head data.csv` or `wc -l` every time it 
starts a new thought process regarding the same file, wasting tokens and compute.

This script implements the "Stateful Tool" pattern. It performs a deep, 
expensive analysis of a dataset on the first pass, and commits that semantic 
profile to local memory (`.antigravity_data_cache.json`). On subsequent calls 
by the LLM, it acts as a high-speed memory retrieval mechanism.

Key Engineering Features:
-------------------------
1. Idempotent Memory: Uses MD5 hashing to ensure the cache is only invalidated 
   if the underlying file actually changes.
2. Cognitive Summarization: Extracts high-leverage semantic data (like identifying 
   Primary Keys via cardinality) so the LLM doesn't have to guess.
3. Graceful Degradation: Falls back to generic metadata if advanced dependencies 
   (like pandas) are missing, preventing hard crashes in constrained environments.
"""

import sys
import os
import json
import hashlib
import argparse

# =============================================================================
# DEPENDENCY INJECTION & GRACEFUL DEGRADATION
# =============================================================================
# The "Staff Engineer" way to handle dependencies.
# We do not crash the agent if Pandas is missing. We log a warning to stderr
# (so the Host Agent/Orchestrator sees it) and gracefully downgrade our capabilities.
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("WARNING: pandas not found. Advanced CSV profiling disabled.", file=sys.stderr)

# The local memory store for this skill.
CACHE_FILE = ".antigravity_data_cache.json"

def get_file_hash(filepath):
    """
    Generates an MD5 hash of the file contents.
    
    This acts as the cache invalidation key. It allows the Agent to 
    instantly know if a file was modified (e.g., by another agent tool) 
    since the last time it looked at it.

    Args:
        filepath (str): Path to the target file.
        
    Returns:
        str: MD5 hex digest, or exits with code 1 if file is missing.
    """
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            # Chunked reading (4KB) ensures memory safety. 
            # We don't want an Agent crashing the server by trying to hash a 50GB CSV in RAM.
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        # Halt execution. Do not let the LLM hallucinate data for a missing file.
        print(f"ERROR: File {filepath} not found.", file=sys.stderr)
        sys.exit(1)

def profile_csv(filepath):
    """
    Performs deep semantic extraction on CSV files to build a cognitive profile.
    
    Instead of just giving the LLM the raw text, we give it the *metadata* it actually needs to reason about the data structure.
    
    Args:
        filepath (str): Path to the CSV file.
        
    Returns:
        tuple: (stats_dict, summary_string)
    """
    if not HAS_PANDAS:
        return {}, "Pandas missing. Generic analysis only."

    try:
        # Load the dataframe. Note: In production with multi-GB files, 
        # this should be swapped out for chunking or a library like Polars/DuckDB.
        df = pd.read_csv(filepath)
        rows, cols = df.shape
        
        # 1. Cardinality Analysis
        # Calculate unique elements per column.
        unique_counts = df.nunique().to_dict()
        
        # 2. Semantic Inference (The "Aha!" moment for the LLM)
        # If a column has exactly as many unique values as there are rows, 
        # it is highly probable to be a Primary Key (ID).
        potential_ids = [col for col, count in unique_counts.items() if count == rows]
        
        stats = {
            "type": "csv",
            "rows": rows,
            "columns": cols,
            "column_names": list(df.columns),
            "unique_values": unique_counts, # Helps LLM spot categorical columns
            "potential_keys": potential_ids # Saves the LLM from having to guess the ID
        }

        # Create a dense, information-rich summary for quick context ingestion.
        summary = f"CSV: {rows:,} rows, {cols} cols. Key Candidates: {potential_ids if potential_ids else 'None'}"
        return stats, summary

    except Exception as e:
        # Catch parse errors (e.g., malformed CSVs) and report them back to the Agent.
        return {}, f"Error analyzing CSV structure: {str(e)}"

def analyze_data(filepath):
    """
    The main execution loop implementing the ReAct + Memory pattern.
    
    Args:
        filepath (str): Path to the file to analyze.
    """
    
    # =========================================================================
    # 1. Cognitive Step: Check Memory (State Retrieval)
    # =========================================================================
    current_hash = get_file_hash(filepath)
    cache = {}
    
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                cache = json.load(f)
        except json.JSONDecodeError:
            cache = {} 
            
    # =========================================================================
    # 2. Decision Engine: Recall vs. Re-read
    # =========================================================================
    # We check if the file is in cache, AND the hash matches, AND the cache 
    # schema is up-to-date (contains the 'stats' key).
    is_cached = filepath in cache and cache.get(filepath, {}).get('hash') == current_hash
    has_stats = 'stats' in cache.get(filepath, {})
    
    if is_cached and (has_stats or not filepath.endswith('.csv')):
        # Cache Hit: Bypass expensive I/O operations.
        print(f"MEMORY RECALL: I have already analyzed this file.")
        print(f"SUMMARY: {cache[filepath]['summary']}")
        
        # Inject the structured stats directly into the LLM's context window for this turn.
        if 'stats' in cache[filepath]:
            print(f"\n[DETAILED PROFILE RECALLED]")
            print(json.dumps(cache[filepath]['stats'], indent=2))
        return

    # =========================================================================
    # 3. Action: Perform Analysis (Compute)
    # =========================================================================
    print("ANALYZING: Reading file and calculating deep stats...")
    
    file_stats = {}
    summary = ""
    file_size = os.path.getsize(filepath)

    if filepath.endswith('.csv'):
        file_stats, summary = profile_csv(filepath)
    else:
        # Fallback for non-CSV files (e.g., JSON, txt).
        summary = f"File {os.path.basename(filepath)} is {file_size} bytes (Generic)."

    # =========================================================================
    # 4. Cognitive Step: Commit to Memory (State Persistence)
    # =========================================================================
    # We save the structural knowledge to disk so it persists across LLM sessions 
    # and even across different agent processes.
    cache[filepath] = {
        'hash': current_hash,
        'summary': summary,
        'stats': file_stats, 
        'analyzed_at': str(os.path.getmtime(filepath))
    }
    
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)
        
    print(f"ANALYSIS COMPLETE: {summary}")
    if file_stats:
        print(json.dumps(file_stats, indent=2))

if __name__ == "__main__":
    # Command Line Interface for Host Agent Execution
    parser = argparse.ArgumentParser(description="Profiles data files and caches semantic metadata.")
    parser.add_argument("--filepath", required=True, help="Target file to profile.")
    args = parser.parse_args()
    
    analyze_data(args.filepath)
