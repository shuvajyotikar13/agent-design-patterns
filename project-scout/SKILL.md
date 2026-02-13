---
name: project-scout
description: A recursive discovery tool. It allows the agent to map a project layer-by-layer, starting from the surface and drilling down interactively, ensuring the user is not overwhelmed by data.
compatibility: python3.10+
license: Apache-2.0
metadata:
  author: sands
  version: "1.0"
---

# Project Scout (Interactive Mode)

## Description
This skill acts as a "Scout" that generates a mental map of the project. Unlike standard `ls` commands, this tool is designed for **Progressive Disclosure**. It starts shallow and allows the agent to drill down based on user feedback.

## Instructions

**WHEN** the user says "Explore this project," "What is in here?", or "Map the codebase," **DO NOT** just dump the whole tree.

**FOLLOW THIS STRICT PROTOCOL:**

### Phase 1: Surface Scan (Level 0)
1.  **Run** the tool with `depth=0`.
    ```bash
    python3 scripts/tree_scout.py --directory "." --depth 0
    ```
2.  **Present** the high-level folders to the user.
3.  **Ask:** "I see these top-level directories. Shall I dig deeper into Level 2?"

### Phase 2: The Deep Dive Loop
1.  **IF** the user says "Yes" or "Go deeper":
    * Increment the depth (e.g., `depth=1`, `depth=2`, then `depth=3`).
    * **Run** the tool again:
        ```bash
        python3 scripts/tree_scout.py --directory "." --depth <CURRENT_DEPTH>
        ```
2.  **Analyze the Output:**
    * **Condition A:** If the output reveals new `[DIR]` folders, show them and **Ask**: "Shall I go to Level <NEXT_LEVEL>?"
    * **Condition B:** If the output contains **NO** new directories (only files), or if the tree structure looks complete.
        * **STOP** the loop.
        * **Proceed to Phase 3.**

### Phase 3: Targeted Action
1.  **State:** "We have mapped the entire structure."
2.  **Ask:** "Which specific file would you like me to read or analyze?"

## Tool Usage

**Standard Invocation:**
```bash
python3 scripts/tree_scout.py --directory "<ROOT_DIR>" --depth <INT>
