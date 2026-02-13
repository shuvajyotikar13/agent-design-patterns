import tiktoken
import textwrap

# 1. Setup the Tokenizer (using GPT-4 encoding as a standard baseline)
enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    return len(enc.encode(text))

# 2. Simulate the Data
# -------------------

# Scenario A: The Monolith (The "Old Way")
# Imagine dumping the entire REST API docs for GCP into the prompt.
# We simulate this by generating technical "bloat" per tool.
def generate_heavy_docs(service_name, api_subdomain):
    bloat = f"""
    ## {service_name} Detailed Specification
    - Version: v1
    - API Endpoint: https://{api_subdomain}.googleapis.com/
    - Authentication: OAuth 2.0 / Service Account Bearer Token
    - Error Codes: 400, 401, 403, 404, 429, 500, 503
    - Retry Policy: Exponential Backoff (Base 2)
    - Methods: GET, POST, PUT, DELETE, PATCH
    - Payload Limit: 10MB
    [... insert 5 pages of parameter definitions for {service_name} ...]
    [... insert 10 examples of JSON responses for {service_name} ...]
    """
    # Repeat to simulate real documentation length (~500 tokens per tool)
    return bloat * 5

monolith_prompt = """
You are a Cloud Admin Agent. Here is the complete documentation for all your tools.
""" + generate_heavy_docs("Compute Engine", "compute") + \
      generate_heavy_docs("Cloud Storage", "storage") + \
      generate_heavy_docs("Cloud SQL", "sqladmin") + \
      generate_heavy_docs("Cloud Functions", "cloudfunctions")

# Scenario B: The Skill Registry (The "New Way")
# This is just the Discovery Metadata found in the YAML frontmatter.
discovery_prompt = """
You are a Cloud Admin Agent. Here are the tools available to you.
To use one, request to LOAD it by name.

- Name: compute-engine-manager
  Description: Manage virtual machine instances. Actions: start, stop, delete VM.
  
- Name: cloud-storage-store
  Description: Object storage management. Actions: create bucket, upload object, set IAM.

- Name: cloud-sql-database
  Description: Fully managed relational database service. Actions: create instance, backup, restore.

- Name: cloud-functions-serverless
  Description: Event-driven serverless compute. Actions: deploy function, trigger, view logs.
"""

# 3. The Measurement
# ------------------
print(f"{'METRIC':<30} | {'TOKENS':<10} | {'COST (approx input)'}")
print("-" * 60)

# Measure Monolith
mono_count = count_tokens(monolith_prompt)
print(f"{'Monolithic Prompt (All Docs)':<30} | {mono_count:<10} | ${mono_count / 1000 * 0.01:.4f}")

# Measure Discovery
disc_count = count_tokens(discovery_prompt)
print(f"{'Discovery Prompt (Metadata)':<30} | {disc_count:<10} | ${disc_count / 1000 * 0.01:.4f}")

# 4. The Savings Calculation
# --------------------------
savings = mono_count - disc_count
percent = (savings / mono_count) * 100

print("-" * 60)
print(f"TOKENS SAVED PER TURN: {savings}")
print(f"PERCENTAGE REDUCTION:  {percent:.2f}%")
print("-" * 60)

# 5. The "Quadratic Reality" Check
# If this conversation goes for 20 turns, how many tokens do we waste?
turns = 20
wasted_total = savings * turns
print(f"\nIMPACT OVER {turns} TURNS:")
print(f"You avoided re-sending {wasted_total:,} unnecessary tokens.")
print(f"That is the equivalent of processing 'War and Peace' {wasted_total / 587287:.1f} times.")
