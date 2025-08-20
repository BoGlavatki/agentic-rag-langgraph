# agentic-rag-langgraph
This branch is a hands-on learning project to deepen my expertise in building an agentic RAG system with LangGraph—covering ingestion, retrieval, filtering, generation, web-search integration, self-refinement, and adaptive behavior.

## Ice Breaker
This application uses agents and a scraper—"Scrape Any Data"—to extract data from websites. Specifically, it is designed to find information about a person on LinkedIn and generate structured information about them.
<img width="1050" height="988" alt="Screenshot 2025-08-14 at 00 00 32" src="https://github.com/user-attachments/assets/a73e94ca-8135-4b86-9c72-c24504a4b303" />

## ReAct AgentExecutor – From Scratch

This branch implements a **ReAct AgentExecutor** step by step with LangChain, including a complete understanding of the ReAct algorithm and modern best practices.

### 📌 Goals
- Build a ReAct agent from scratch
- Understand the ReAct algorithm and its components
- Implement and integrate custom tools
- Use CallbackHandlers to control agent flow
- Prepare for transition to modern tool calling

### 📂 Contents

#### 1. Environment Setup & Algorithm Overview
- Setting up the development environment
- Overview of the ReAct algorithm and its core principles

#### 2. Defining Tools
- Creating custom tools for the agent
- Interfaces for tool integration

#### 3. Debugging
- Solving common errors:
    - Stop token issues
    - Template indentation issues

#### 4. ReAct Prompt & Reasoning Engine
- Creating the ReAct prompt
- Implementing the LLM reasoning engine
- Output parsing & tool execution

#### 5. Agent Core Components
- `AgentAction`
- `AgentFinish`
- Agent loop

#### 6. CallbackHandlers
- Using them to control and finalize the agent loop

#### 7. Recap & LangSmith
- Brief recap of the implementation
- Monitoring and debugging with LangSmith

### 🛠 Technologies
- Python 3.x
- [LangChain](https://python.langchain.com/)
- OpenAI / Azure OpenAI API
- LangSmith

# Agentic Tool-Routing Mini Project (LangChain + Azure OpenAI)

This small project demonstrates how to build a **tool-calling agent** that routes user requests to the right specialist:
1) a **Python Agent** that **writes & executes Python code** via a REPL, and  
2) a **CSV Agent** that answers questions about a local CSV file (`episode_info.csv`) using pandas.

It uses **LangChain’s tool calling**, a prompt from the **LangChain Hub**, and **Azure OpenAI** as the LLM backend.

---

## How it works

- We pull the `react-agent-template` from the LangChain Hub and partially fill it with tool names and instructions.
- Two tools are exposed to the LLM:
  - **Python_Agent** → turns natural-language tasks into Python code and runs it in a REPL.  
    > Example task: generate 15 QR codes into a `qrcodes/` folder.
  - **CSV_Agent** → answers questions about `episode_info.csv` (e.g., counts, filtering) by running pandas ops.
- A **router agent** (LLM) decides which tool to call for a given input and returns the final result.

### Flow (Mermaid)
```mermaid
flowchart TD
    U([User Query]) --> R([Router Agent])
    R -- "Tool Call" --> P[Python_Agent]
    R -- "Tool Call" --> C[CSV_Agent]
    P --> O1[Result]
    C --> O2[Result]
    O1 --> A[Final Answer]
    O2 --> A
