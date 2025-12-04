# LLM Pipeline & Techniques

This document explains the **Large Language Model (LLM) training pipeline**, its core techniques, and practical applications.

---

## Overview of LLM Training Pipeline

Modern LLMs are built using a series of techniques that help the model:

- **Learn language, knowledge, and reasoning**  
- **Follow instructions accurately**  
- **Align outputs with human preferences**  
- **Specialize for specific domains**

### Main Techniques

| Technique | Purpose | Type of Learning | Example |
|-----------|---------|----------------|--------|
| **Pretraining** | Learn general language patterns, grammar, reasoning, world knowledge | Self-supervised (predict next token) | GPT base model trained on internet data |
| **Supervised Instruction Tuning (SFT)** | Teach model to follow instructions | Supervised learning | Instruction: "Explain photosynthesis." Label: correct human-written answer |
| **Reinforcement Learning from Human Feedback (RLHF)** | Align model behavior to human preferences, reduce hallucinations | Reinforcement learning | Human rankings guide the model to prefer polite and accurate answers |
| **Optional Finetuning** | Specialize model for domain or task | Supervised learning (sometimes with light RL) | Legal or medical chatbots |
| **RAG (Retrieval-Augmented Generation)** | Provide trusted knowledge sources at query time | Augmentation technique | Enterprise document Q&A |
| **Prompting** | Guide LLM responses without additional training | Instruction-driven | Asking AI to summarize a report |

---

## LLM Training Pipeline Flow

```mermaid
---
config:
  layout: elk
---
flowchart TB

    %% PIPELINE STAGES
    A["1-Technique Applications - Simple Apps"]
    B["2-Technique Combinations - Real-world Apps"]
    C["3-Technique Combination - Strong Enterprise Apps"]
    D["Full LLM Development Pipeline - Labs / Enterprise"]

    %% FLOW
    A --> B --> C --> D

    %% EXAMPLES IN PIPELINE
    A1["Prompting Only - Simple chatbot"]:::one
    A2["RAG Only - Document QA"]:::one
    A3["Finetuning Only - Email classifier"]:::one
    B1["Prompting + RAG - Enterprise QA assistant"]:::two
    B2["Prompting + Finetuning - Domain chatbot"]:::two
    B3["RAG + Finetuning - Search with domain tuning"]:::two
    C1["Prompting + RAG + Finetuning - Strong enterprise system"]:::three
    D1["Pretraining + SFT + RLHF - GPT/Llama base"]:::full
    D2["Base + Finetuning - Custom GPT"]:::full
    D3["All Techniques + RAG - Enterprise deployed LLM"]:::full

    %% CONNECT EXAMPLES TO STAGES
    A --> A1
    A --> A2
    A --> A3
    B --> B1
    B --> B2
    B --> B3
    C --> C1
    D --> D1
    D --> D2
    D --> D3

    %% CLASS DEFINITIONS FOR COLORS
    classDef one fill:#FFDFE5,stroke:#FF5978,stroke-width:1px,color:#8E2236
    classDef two fill:#D0E8FF,stroke:#3399FF,stroke-width:1px,color:#004C99
    classDef three fill:#D4FFD4,stroke:#33CC33,stroke-width:1px,color:#006600
    classDef full fill:#E6D4FF,stroke:#9933FF,stroke-width:1px,color:#4B0082
