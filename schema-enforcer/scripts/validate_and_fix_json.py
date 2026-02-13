#!/usr/bin/env python3
# =============================================================================
# COMPONENT: stateful-data-profiler
# -----------------------------------------------------------------------------
# Copyright 2026 Shuva Jyoti Kar 
# License: Apache 2.0
# =============================================================================
import json
import sys
import argparse
import os

def get_safe_default(dtype):
    """Returns a type-safe empty value if no default is provided."""
    dtype = dtype.lower()
    if dtype == "string": return ""
    if dtype == "integer": return 0
    if dtype == "float": return 0.0
    if dtype == "boolean": return False
    if dtype == "list": return []
    if dtype == "dict": return {}
    return None

def validate_and_fix(input_json_str, schema_path):
    # 1. Load the Schema
    if not os.path.exists(schema_path):
        print(f"CRITICAL ERROR: Schema file not found at {schema_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(schema_path, 'r') as f:
            schema = json.load(f)
    except json.JSONDecodeError:
        print(f"CRITICAL ERROR: Schema file at {schema_path} is invalid JSON.", file=sys.stderr)
        sys.exit(1)

    # 2. Parse the Input (Resilient Load)
    # If the LLM sends 'None' or empty string, treat it as empty dict
    if not input_json_str or input_json_str.strip() == "None":
        data = {}
    else:
        try:
            data = json.loads(input_json_str)
        except json.JSONDecodeError:
            print("ERROR: Input is not valid JSON. Cannot validate.", file=sys.stderr)
            sys.exit(1)

    fixed_data = data.copy()
    corrections = []

    # 3. The Enforcer Loop
    for field in schema.get('fields', []):
        name = field['name']
        dtype = field.get('type', 'string')
        is_required = field.get('required', False)
        schema_default = field.get('default', None)

        # CHECK: Is the field missing?
        if name not in fixed_data:
            if is_required:
                # DECISION: Inject Default or Type-Safe Null
                final_value = schema_default if schema_default is not None else get_safe_default(dtype)
                
                fixed_data[name] = final_value
                corrections.append(f"MISSING FIELD '{name}': Injected default value '{final_value}' (Type: {dtype})")
            else:
                # It's optional and missing. Do nothing.
                continue
        
        # CHECK: Type Validation (Bonus: Simple Casting)
        # If schema says integer but we have "8080" (string), fix it.
        elif name in fixed_data and dtype == "integer":
            try:
                if type(fixed_data[name]) != int:
                    fixed_data[name] = int(fixed_data[name])
                    corrections.append(f"TYPE FIX '{name}': Cast to integer.")
            except (ValueError, TypeError):
                # Fallback to default if cast fails
                fallback = schema_default if schema_default is not None else 0
                fixed_data[name] = fallback
                corrections.append(f"TYPE ERROR '{name}': Could not cast. Reset to default '{fallback}'.")

    # 4. Output the CLEAN JSON (Standard Out)
    print(json.dumps(fixed_data, indent=4))
    
    # 5. Output the Report (Standard Error - Agent Visibility Only)
    if corrections:
        print(f"\n[SCHEMA ENFORCER REPORT]", file=sys.stderr)
        for c in corrections:
            print(f"- {c}", file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="The JSON string to validate")
    parser.add_argument("--schema", default="assets/schema.json", help="Path to schema file")
    args = parser.parse_args()
    
    validate_and_fix(args.input, args.schema)
