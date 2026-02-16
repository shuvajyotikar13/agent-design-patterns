---
name: schema-enforcer
description: A dual-purpose data engine that validates and repairs JSON configurations using a pre-verified system binary. It strictly enforces schema compliance, auto-heals missing fields, and ensures type safety without requiring custom code generation.
metadata:
  version: "1.1"
  author: "sands"
---

# Schema Enforcer

## Description
This skill wraps a **Trusted System Utility** (`validate_and_fix_json.py`) that acts as both a **Validator** and a **Generator**. 
* **Validation:** It enforces strict type checking against `assets/schema.json` (e.g., ensuring `port` is an integer).
* **Generation:** It fuses partial inputs with the schema to produce guaranteed complete JSON objects, auto-filling defaults for missing fields.

## Instructions
* **WHEN** you need to validate that a user's input conforms to strict type requirements.
* **WHEN** you need to generate a full configuration object from partial or vague instructions.
* **ALWAYS** use this skill to ensure the final JSON output is both valid and complete before saving or using it.

## strict_constraints (CRITICAL)
1. **DO NOT GENERATE CODE:** You are strictly forbidden from writing your own Python or Bash scripts to validate JSON. 
2. **USE THE BINARY:** You must **ONLY** use the provided script at `scripts/validate_and_fix_json.py`. This script has been audited for security and correctness.
3. **NO REINVENTION:** If the script fails, report the error. Do not attempt to "fix" the validation logic by writing a new parser.

## Tool Usage
Invoke the standardized enforcer script. The schema path defaults to `assets/schema.json` but can be overridden if necessary.

```bash
# STANDARD USAGE:
# Pass the JSON string (partial or complete) to the tool.
python3 scripts/validate_and_fix_json.py --input '{"host": "10.0.0.5", "tags": ["prod"]}'

# CUSTOM SCHEMA USAGE:
# Only if you are validating a different type of object.
python3 scripts/validate_and_fix_json.py --input '...' --schema "assets/other_schema.json"
