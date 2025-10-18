# supermemory Agent 🤖

A smart AI assistant with memory and web search capabilities, built with LangGraph and Streamlit.

## Features ✨

- **Conversational AI**: Natural language interactions
- **Web Search**: Retrieve up-to-date information
- **Memory**: Persistent conversation history
- **Modular Architecture**: Easy to extend and customize

## Tech Stack 🛠️

- **Framework**: [LangGraph](https://langchain-ai.github.io/langgraph/)
- **UI**: [Streamlit](https://streamlit.io/)
- **LLM**: OpenAI GPT-4
- **Vector Store**: [SuperMemory](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://supermemory.ai/&ved=2ahUKEwjh1KfQ2qiQAxXCSmwGHdGCKmwQFnoECB0QAQ&sqi=2&usg=AOvVaw2bVeuTJ9gGnaoyxJnbctSy) (custom implementation)
- **Web Search**: Custom Tavily client

## Installation 🚀

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/supermemory.git
   cd supermemory
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r app/requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Usage 💻

### Web Interface
```bash
cd app
streamlit run app.py
```

### API Server
```bash
cd app
uvicorn main:api --reload
```

## Project Structure 📁

```
app/
├── graph/               # LangGraph workflow definitions
│   ├── nodes/           # Individual node implementations
│   ├── chains/          # LangChain chains
│   └── main_graph.py    # Main workflow definition
├── utils/              # Utility functions
└── app.py              # Streamlit web interface
```

## Workflow

1. User submits a query
2. System checks memory for relevant context
3. Performs web search if needed
4. Generates response using LLM
5. Updates conversation history


Made with ❤️ by [Arnav Singh]
