#!/usr/bin/env python3
# =============================================================================
# COMPONENT: S.A.N.D.S. REPAIR AGENT
# -----------------------------------------------------------------------------
# Copyright 2026 Shuva Jyoti Kar & Shruti Mantri
# License: Apache 2.0

import json
import sys
import os
import argparse

def repair_and_write(filepath, content_str):
    try:
        # Step 1: Validation
        # We try to parse it. If it fails, we throw the specific error back to the Agent.
        data = json.loads(content_str)
        
        # Step 2: Write (Only if valid)
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
            
        print(f"SUCCESS: Valid JSON saved to {filepath}")
        sys.exit(0)

    except json.JSONDecodeError as e:
        # Step 3: feedback Loop
        # We don't just say "Failed". We say WHERE and WHY.
        # This allows the Agent to "debug" itself.
        error_msg = (
            f"JSON_ERROR: {e.msg}\n"
            f"LOCATION: Line {e.lineno}, Column {e.colno}\n"
            f"SNIPPET: ...{content_str[max(0, e.pos-20):e.pos+20]}..."
        )
        print(error_msg, file=sys.stderr)
        sys.exit(1)
        
    except Exception as e:
        print(f"SYSTEM_ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", required=True)
    parser.add_argument("--content", required=True)
    args = parser.parse_args()
    
    repair_and_write(args.filepath, args.content)
