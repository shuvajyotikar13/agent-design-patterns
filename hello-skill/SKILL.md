---
name: hello-skill
description: Generates a compliant corporate greeting. Trigger this ONLY when the user sends a standalone greeting (e.g., "Hi", "Hello") or explicitly asks for an introduction.DO NOT trigger this for substantive requests (e.g., "Hi, I have a bug").
license: Apache-2.0
metadata:
  author: sands
  version: "1.0"
---

# Professional Greeting Procedure

## 1. Input Validation (Soft Guardrails)
Before generating text, you must extract the following variables from the context and validate them against these rules.

### Variable: `user_name`
* **Source:** The name of the user, if known from context.
* **Validation Rule:** Check if the value is a valid string.
    * **IF Valid:** Use the name (e.g., "Sarah").
    * **IF Missing/Empty:** Set the value to `"Valued Partner"`.

### Variable: `user_role`* 
**Source:** The user's permission level.
* **Validation Rule (Enum Check):** You must coerce the value into one of these three exact strings: `["Visitor", "Employee", "Admin"]`.
* **Constraint:** If the provided role is invalid (e.g., "Ninja", "SuperUser") or missing, you **MUST** default to `"Visitor"`.

### Variable: `time_of_day`
* **Source:** Current system time in HH:MM 24h format.
* **Validation Rule (Required Field):**    
* **Step 1:** Verify that `time_of_day` is present in the context.
* **Step 2:** Verify it matches the `HH:MM` format (e.g., "14:30").
* **Fallback:** If this required field is missing or malformed, you **MUST** assume `"09:00"` (Morning) to ensure the greeting generates successfully.

## 2. Logic: Time-Based Selection
Select the greeting phrase based on `time_of_day` (HH:MM):
- **00:00 - 11:59**: "Good Morning"
- **12:00 - 16:59**: "Good Afternoon"
- **17:00 - 23:59**: "Good Evening"

## 3. Logic: Role-Based Suffix
Append a suffix based on `user_role`:
- **Visitor**: "...Welcome to the Acme Agent Hub."
- **Employee**: "...Ready to assist with internal workflows."
- **Admin**: "...System controls are active."

## 4. Output Contract
The final output must be a single string in this exact format:
`[Greeting Phrase], [user_name]. [Suffix]`

## 5. Examples (Few-Shot)
Use these examples to calibrate your output:

**Invocation:**
`{ "user_name": "Sarah", "user_role": "Admin", "time_of_day": "09:30" }`
**Output:**
"Good Morning, Shruti. System controls are active."

**Invocation:**
`{ "user_name": null, "user_role": "Unknown", "time_of_day": "14:00" }`
**Output:**
"Good Afternoon, Valued Partner. Welcome to the Acme Agent Hub."


