---
name: stateful_data_profiler
description: A smart data analysis tool that maintains a persistent cache of file profiles. It includes a reporting tool to view the cached knowledge base in a human-readable format.
license: Apache-2.0
compatibility: python3.10+
metadata:
  author: sands
  version: "1.0"
---

# Stateful Data Profiler

## Description
This skill implements the "Librarian" pattern. It analyzes datasets (CSV, JSON, Text) and stores the results in a local cache (`.antigravity_data_cache.json`) to avoid expensive re-reading. It also provides a viewer script to inspect this long-term memory.

## Instructions

### Capability 1: Analyze a File
* **WHEN** the user asks to analyze, summarize, or get stats for a specific file.
* **USE** the `scripts/analyze_with_cache.py` script.
* **Behavior:** It checks the cache first. If the file is new or changed, it performs a fresh analysis.
* **Output:** The tool will print either "ANALYZING" (fresh read) or "MEMORY RECALL" (cached read). Report this distinction to the user.

### Capability 2: View Knowledge Base
* **WHEN** the user asks "What do you know?", "Show me the cache", "List analyzed files", or "What is in your memory?".
* **USE** the `assets/view_report.py` script.
* **Behavior:** It reads the entire cache and prints a formatted Markdown table of all files the agent has tracked.

## Tool Usage

**To Analyze a File:**
```bash
python3 scripts/analyze_with_cache.py --filepath "data.csv"
```
