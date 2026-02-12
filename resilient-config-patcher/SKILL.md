---
name: resilient_config_patcher
description: A fault-tolerant file writer that enforces valid JSON and fuxes invalid JSON.
license: Apache-2.0
metadata:
  author: sands
  version: "2.0"
---

# Resilient Configuration Patcher

## Description
This skill writes JSON files. It acts as a **Strict Gatekeeper**. If the input JSON is invalid, the tool will reject it and provide a specific syntax error.

## Autonomous Repair Protocol
This skill is designed for **Self-Correction**. 
1. The Agent attempts to write the file.
2. If the tool returns a `JSON_ERROR` (Exit Code 1), the Agent **MUST NOT** ask the user for help.
3. The Agent **MUST** analyze the error message (Line/Column), fix the JSON payload in its internal context, and **CALL THE TOOL AGAIN**.
4. Repeat this loop up to 3 times until `SUCCESS` is returned.

## Instructions
* **WHEN** generating configuration files (JSON).
* **IF** the tool fails with a syntax error, **IMMEDIATELY** retry with the corrected syntax.
* **DO NOT** output the invalid JSON to the user; only output the final success message.

## Tool Usage
```bash
python3 scripts/repair_json.py --filepath "/path/to/config.json" --content '{"key": "value"}'
```
