# Agent Skills: Cognitive Patterns

**Foundational Capabilities for Autonomous Agents.**

A collection of enterprise-grade **Agent Skills** designed to equip LLMs with the procedural knowledge required for complex, high-stakes workflows. These patterns transform raw model intelligence into reliable engineering outcomes.

*Maintained by [@shuvajyotikar13](https://github.com/shuvajyotikar13)*

---

### Research Context
The concept of mapping **Agent Skills** to **Cognitive Patterns** is part of a broader research framework on *Agentic Design* developed in collaboration with **Shruti Mantri**.

While this repository provides the reference implementations for the "Control Layer" (Validation & Repair), the framework extends to encompass reasoning strategies, memory architectures, and multi-agent coordination.

---

## Overview

Large Language Models (LLMs) are inherently stochastic (probabilistic), while enterprise systems require deterministic (rigid) inputs. This impedance mismatch causes the majority of agent failures in production.

This repository bridges that gap by implementing **Cognitive Control Loops**—portable skills that force an agent to self-correct and adhere to strict schemas before interacting with downstream APIs.

### The Cognitive Layer


1.  **Schema Enforcement:** Recursive validation loops that ensure output strict typing (Pydantic/JSON Schema).
2.  **Self-Healing:** Autonomous "repair-and-retry" workflows that correct malformed JSON or logic errors without human intervention.

**Standard Alignment:** Built on the open [Agent Skills](https://agentskills.io) specification for interoperability.

## Featured Skills

### 1. The Schema Enforcer
A rigid control loop that wraps the LLM generation process. It treats the LLM as an untrusted component, validating every output against a defined `pydantic` model. If validation fails, the error stack trace is fed back into the model for a focused retry.

### 2. The Self-Healing Signal
A pattern for handling partial failures. Instead of crashing on a `JSONDecodeError` or a hallucinated field, this skill activates a "Repair Agent" that parses the broken string, identifies the syntax error, and reconstructs valid JSON.

## Getting Started

### Prerequisites
* Python 3.10+
* OpenAI API Key (or compatible LLM endpoint)

### Installation

```bash
git clone [https://github.com/Agent-Skills-Lab/agent-design-patterns.git](https://github.com/Agent-Skills-Lab/agent-design-patterns.git)
cd agent-design-patterns
pip install -r requirements.txt
```

### Usage Example

```bash
```

### Contributing
This project is a reference implementation for the Cognitive Patterns using Agent Skills(eg. Google Antigravity). Issues and Pull Requests pertaining to cognitive patternsfor enterprise use-cases are welcome.

### License
Apache 2.0
Copyright 2026[@shuvajyotikar13](https://github.com/shuvajyotikar13).

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.

