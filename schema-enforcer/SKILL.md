---
name: schema-enforcer
description: A dual-purpose data engine that strictly validates input JSON against a schema AND synthesizes complete, production-ready json objects for a given schema. It enforces type safety while automatically populating missing mandatory and optional fields with schema-defined defaults.
---

# Schema Enforcer

## Description
This skill acts as both a **Validator** and a **Generator**.
1.  **Validation:** It checks that all provided fields match the data types defined in the schema (e.g., ensuring `port` is an integer).
2.  **Generation:** It takes partial inputs and fuses them with the schema to produce a guaranteed complete JSON object, auto-filling defaults for missing fields.

## Instructions
* **WHEN** you need to **validate** that a user's input conforms to strict type requirements.
* **WHEN** you need to **generate** a full configuration object from partial or vague instructions.
* **ALWAYS** use this skill to ensure the final JSON output is both valid and complete before saving or using it.

## Tool Usage
Run the script with the input JSON. The schema defaults to `assets/schema.json`.

```bash
# Example: Validates "host" is a string, then fills in "port" (8080) and others.
python3 scripts/validate_and_fix_json.py --input '{"host": "10.0.0.5"}' --schema "assets/schema.json"
```
