---
name: project_scout
description: A recursive discovery, mapping or scouting tool. It allows the agent to map a project layer-by-layer  incrementally (Level 1 -> Level 2 -> ...), starting from the surface and drilling down interactively, till the entire structure is revealed, ensuring the user is not overwhelmed by data.
license: Apache-2.0
compatibility: python3.10+
metadata:
  author: sands
  version: "1.0"
---

# Project Scout (Interactive Mode)

## Description
This skill acts as a **Manual Scout**. It enforces **Progressive Disclosure**, revealing the file system one layer at a time. It is designed to capture the user's original intent of "walking" through a codebase rather than dumping it all at once.

## Instructions

**WHEN** the user says "Explore this project," "Map the codebase," or "Scout the directory," you **MUST** follow this strict execution loop.

### Phase 1: Initialization (The Surface)
1.  **Action:** Run the scout at **Depth 1**.
    ```bash
    python3 scripts/tree_scout.py --directory "." --depth 1
    ```
2.  **Observation:** Present the top-level folders to the user.
3.  **Mandatory Prompt:** "I have mapped the surface (Level 1). Shall I dig to Level 2? (Type 'N' to exit)"

### Phase 2: The Discovery Loop
**LISTEN** to the user's response to the previous prompt.

**CONDITION A: The User says 'N' (No/Stop/Exit)**
* **Action:** Terminate the workflow immediately.
* **Response:** "Understood. Scout halted at the current level."

**CONDITION B: The User says 'Y' (Yes/Go Deeper/Next)**
* **Step 1:** Increment the depth variable (`Current_Depth + 1`).
* **Step 2:** Execute the tool:
    ```bash
    python3 scripts/tree_scout.py --directory "." --depth <NEW_DEPTH>
    ```
* **Step 3: THE CONVERGENCE CHECK (Critical)**
    * **COMPARE** the output of this new run against the output of the *immediately preceding* run.
    * **IF IDENTICAL:**
        * **Conclusion:** There are no deeper directories; we have hit the bottom.
        * **Action:** **STOP**. Do not ask to go deeper.
        * **Response:** "Level <X> is identical to Level <X-1>. The entire structure has been mapped. No further directories exist."
    * **IF DIFFERENT:**
        * **Conclusion:** New folders were found.
        * **Action:** **CONTINUE**.
        * **Response:** "Level <X> mapped. Shall I dig to Level <X+1>? (Type 'N' to exit)"

### Phase 3: Completion
Once the loop terminates (via 'N' or Convergence):
1.  **Summarize:** "Scout complete. Directory structure is captured in context."
2.  **Next Step:** "Would you like me to read or analyze a specific file from this map?"

## Tool Usage

**Standard Invocation:**
```bash
# Replace <INT> with the current integer depth (1, 2, 3...)
python3 scripts/tree_scout.py --directory "." --depth <INT>
