# agentic-rag-langgraph
This branch represents a hands‑on learning project to deepen my expertise in building an agentic RAG system with LangGraph—covering ingestion, retrieval, filtering, generation, web‑search integration, self‑refinement, and adaptive behavior.

## Ice Breaker
This application uses agents and a scraper—"Scrape Any Data"—to extract data from websites. Specifically, it is designed to find information about a person on LinkedIn and generate structured information about them.<img width="1050" height="988" alt="Bildschirmfoto 2025-08-14 um 00 00 32" src="https://github.com/user-attachments/assets/a73e94ca-8135-4b86-9c72-c24504a4b303" />

# ReAct AgentExecutor – From Scratch

Dieser Branch implementiert Schritt für Schritt einen **ReAct AgentExecutor** mit LangChain, inklusive vollständigem Verständnis des ReAct-Algorithmus und moderner Best Practices.

## 📌 Ziele
- Aufbau eines ReAct-Agenten von Grund auf
- Verständnis des ReAct-Algorithmus und seiner Komponenten
- Implementierung und Integration eigener Tools
- Nutzung von CallbackHandlers zur Steuerung des Agentenflusses
- Vorbereitung auf den Wechsel zu modernem Tool Calling

## 📂 Inhalte

### 1. Environment Setup & Algorithm Overview
- Einrichtung der Entwicklungsumgebung
- Überblick über den ReAct-Algorithmus und seine Kernprinzipien

### 2. Defining Tools
- Erstellung eigener Tools für den Agenten
- Schnittstellen für Tool-Integration

### 3. Debugging
- Lösen typischer Fehler:
  - Stop Token Probleme
  - Template Indentation Issues

### 4. ReAct Prompt & Reasoning Engine
- Erstellung des ReAct-Prompts
- LLM Reasoning Engine implementieren
- Output Parsing & Tool Execution

### 5. Agent Core Components
- `AgentAction`
- `AgentFinish`
- Agent-Loop

### 6. CallbackHandlers
- Nutzung zur Steuerung und Finalisierung des Agent-Loops

### 7. Recap & LangSmith
- Kurzes Recap der Implementierung
- Monitoring und Debugging mit LangSmith

## 🛠 Technologien
- Python 3.x
- [LangChain](https://python.langchain.com/)
- OpenAI / Azure OpenAI API
- LangSmith