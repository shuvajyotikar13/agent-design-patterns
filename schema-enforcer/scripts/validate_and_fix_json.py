#!/usr/bin/env python3
# =============================================================================
# COMPONENT: stateful-data-profiler
# -----------------------------------------------------------------------------
# Copyright 2026 Shuva Jyoti Kar 
# License: Apache 2.0
# =============================================================================
"""
Resilient Schema Enforcer for Agentic Workflows
===============================================

Overview:
---------
This script acts as a hard boundary for LLM-generated JSON. It performs three
distinct phases of validation:
1. Heuristic Repair: Aggressively fixes common LLM syntax errors:
   - Concatenated strings ("val""val")
   - Missing commas between fields
   - Trailing commas before closing braces
   - Markdown code fences
2. Syntax Validation: Ensures the input is structurally valid JSON.
3. Schema Enforcement: Injects missing defaults and strictly enforces data 
   types without overwriting valid existing values.

Usage:
------
python3 validate_and_fix_json.py --input '{"tags": ["a""b"],}' --schema 'schema.json'
"""

import json
import sys
import argparse
import os
import re

def get_safe_default(dtype):
    """Returns a type-safe empty value if no default is provided in the schema."""
    dtype = dtype.lower()
    if dtype == "string": return ""
    if dtype == "integer": return 0
    if dtype == "float": return 0.0
    if dtype == "boolean": return False
    if dtype == "list": return []
    if dtype == "dict": return {}
    return None

def heuristic_repair(broken_json):
    """
    Attempts to fix common LLM JSON syntax errors using regex patterns.
    """
    text = broken_json.strip()
    
    # 1. Strip Markdown Code Blocks (```json ... ```)
    if "```" in text:
        pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
        match = re.search(pattern, text)
        if match:
            text = match.group(1)

    # 2. Fix Concatenated Strings (e.g., "production""web-tier")
    # Logic: A quote, followed by optional whitespace, followed by another quote.
    # We ignore ":" to avoid breaking key:value pairs.
    text = re.sub(r'"\s*(?=")', '", ', text)

    # 3. Fix Missing Commas between Values (e.g., 123 "key": val)
    # Logic: End of a literal (digit, bool, null) followed by a quote (start of next key/val)
    text = re.sub(r'(\d|true|false|null)\s*(?=")', r'\1, ', text)

    # 4. Fix Trailing Commas (e.g., {"a": 1,})
    # Logic: A comma followed immediately by a closing brace/bracket
    text = re.sub(r',(\s*?[}\]])', r'\1', text)

    # 5. Balance Braces (Simple Check)
    # If we have more opens than closes, append them.
    open_curly = text.count('{')
    close_curly = text.count('}')
    if open_curly > close_curly:
        text += '}' * (open_curly - close_curly)
        
    open_square = text.count('[')
    close_square = text.count(']')
    if open_square > close_square:
        text += ']' * (open_square - close_square)

    return text

def validate_and_fix(input_json_str, schema_path):
    """
    Validates syntax (with repair), patches missing fields, and enforces schema types.
    """
    
    # =========================================================================
    # 1. Load the Schema
    # =========================================================================
    if not os.path.exists(schema_path):
        print(f"CRITICAL ERROR: Schema file not found at {schema_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(schema_path, 'r') as f:
            schema = json.load(f)
    except json.JSONDecodeError:
        print(f"CRITICAL ERROR: Schema file at {schema_path} is invalid JSON.", file=sys.stderr)
        sys.exit(1)

    # =========================================================================
    # 2. Syntax Validation & Heuristic Repair
    # =========================================================================
    data = {}
    
    # Handle empty inputs
    if not input_json_str or input_json_str.strip() == "None":
        input_json_str = "{}"

    try:
        # Attempt 1: Standard Load
        data = json.loads(input_json_str)
    except json.JSONDecodeError:
        # Attempt 2: Heuristic Repair
        print(f"WARNING: Invalid JSON detected. Attempting heuristic repair...", file=sys.stderr)
        repaired_str = heuristic_repair(input_json_str)
        try:
            data = json.loads(repaired_str)
            print(f"SUCCESS: JSON repaired automatically.", file=sys.stderr)
        except json.JSONDecodeError as e:
            # Attempt 3: Fail Gracefully
            print(f"SYNTAX ERROR: Could not repair JSON.", file=sys.stderr)
            print(f"DETAILS: {e.msg}", file=sys.stderr)
            sys.exit(1)

    ordered_data = {}
    corrections = []

    # =========================================================================
    # 3. The Enforcer Loop (Schema Compliance)
    # =========================================================================
    for field in schema.get('fields', []):
        name = field['name']
        dtype = field.get('type', 'string')
        is_required = field.get('required', False)
        schema_default = field.get('default', None)

        # 3A. CHECK: Is the field missing?
        if name not in data:
            if is_required or schema_default is not None:
                final_value = schema_default if schema_default is not None else get_safe_default(dtype)
                ordered_data[name] = final_value
                corrections.append(f"MISSING FIELD '{name}': Injected default value '{final_value}' (Type: {dtype})")
        
        # 3B. CHECK: The field exists.
        else:
            val = data[name]
            
            # Constraint Check: Type enforcement
            if dtype == "integer":
                try:
                    if type(val) != int:
                        val = int(val)
                        corrections.append(f"TYPE FIX '{name}': Cast to integer.")
                except (ValueError, TypeError):
                    fallback = schema_default if schema_default is not None else 0
                    val = fallback
                    corrections.append(f"TYPE ERROR '{name}': Could not cast. Reset to default '{fallback}'.")
            
            ordered_data[name] = val

    # =========================================================================
    # 4. Pass-Through
    # =========================================================================
    for k, v in data.items():
        if k not in ordered_data:
            ordered_data[k] = v

    # =========================================================================
    # 5. Output Generation
    # =========================================================================
    print(json.dumps(ordered_data, indent=4))
    
    if corrections:
        print(f"\n[SCHEMA ENFORCER REPORT]", file=sys.stderr)
        for c in corrections:
            print(f"- {c}", file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validates and fixes JSON based on a schema.")
    parser.add_argument("--input", required=True, help="The raw JSON string to validate")
    parser.add_argument("--schema", default="assets/schema.json", help="Path to schema file")
    args = parser.parse_args()
    
    validate_and_fix(args.input, args.schema)
