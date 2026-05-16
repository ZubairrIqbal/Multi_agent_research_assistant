````markdown
# 🔬 Multi-Agent Research Assistant

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Streamlit App](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io)

A sophisticated AI-powered research automation system that leverages **multi-agent collaboration** to gather, analyze, synthesize, and critique research on any topic. Built with LangChain, Claude AI, and Streamlit.

## ✨ Features

- **🔍 Search Agent** — Aggregates recent web information from multiple sources
- **📄 Reader Agent** — Scrapes and extracts detailed content from top resources
- **✍️ Writer Chain** — Synthesizes comprehensive research reports
- **🧐 Critic Chain** — Reviews, scores, and refines report quality
- **🎨 Modern UI** — Custom-designed dark theme with glassmorphism effects
- **⚡ Real-time Pipeline** — Visual feedback for each agent's progress
- **📥 Export Ready** — Download final reports in multiple formats

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- **pip** or **conda**
- **API Keys**: OpenAI/Anthropic (for LLM), SerpAPI (for web search)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/multi-agent-research-assistant.git
   cd multi-agent-research-assistant
   ```

2. **Create a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Create .env file in project root
   copy .env.example .env
   ```

   Then edit `.env` with your API keys:
   ```
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-...
   SERPAPI_API_KEY=...
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

   The app will open at `http://localhost:8501`


```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT models | ✅ |
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude | ✅ |
| `SERPAPI_API_KEY` | SerpAPI key for web search | ✅ |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING) | ❌ |

### Settings

Edit `src/utils/config.py` to customize:
- Model selection (gpt-4, claude-3-opus, etc.)
- Search depth and result limits
- Report generation parameters
- Quality thresholds

## 📖 Usage

### Basic Research Report

```python
# Access the Streamlit web interface
streamlit run app.py

# Enter your research topic, e.g.:
# "Future of LLM in Tech Industry"
# "AGI Development Roadmap for 2026"
```

### Programmatic Usage

```python
from src.agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# Initialize agents
search_agent = build_search_agent()
reader_agent = build_reader_agent()

# Run search
results = search_agent.invoke({
    "messages": [("user", "Find information about quantum computing")]
})

# Process with other agents
content = reader_agent.invoke({
    "messages": [("user", f"Extract details from: {results}")]
})
```

## 🏗️ Architecture

```
User Input
    ↓
[Search Agent] → Web Results
    ↓
[Reader Agent] → Scraped Content
    ↓
[Writer Chain] → Draft Report
    ↓
[Critic Chain] → Reviewed Report
    ↓
Final Output
```

## 🛠️ Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `streamlit` | >=1.28.0 | Web UI framework |
| `langchain` | >=0.1.0 | Agent orchestration |
| `langchain-anthropic` | >=0.1.0 | Claude integration |
| `langchain-openai` | >=0.1.0 | GPT integration |
| `python-dotenv` | >=1.0.0 | Environment management |
| `requests` | >=2.31.0 | HTTP requests |
| `beautifulsoup4` | >=4.12.0 | Web scraping |

See `requirements.txt` for complete list.

## 🔐 Security

- **Never commit `.env` files** — Add to `.gitignore`
- **Rotate API keys regularly**
- **Use separate keys for dev/prod**
- **Validate all user inputs** before passing to LLMs
- **Implement rate limiting** for production deployments

## 🚨 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8501
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8501
kill -9 <PID>
```

### API Key Issues
```bash
# Verify your .env file is properly formatted
python -c "import dotenv; print(dotenv.dotenv_values('.env'))"
```

### Slow Performance
- Reduce `SEARCH_RESULT_LIMIT` in config
- Use faster models (gpt-3.5-turbo vs gpt-4)
- Implement caching for repeated searches

## 🧪 Testing

```bash
# Run unit tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src

# Test specific agent
pytest tests/test_agents.py -k "search_agent"
```

## 📊 Performance Metrics

| Metric | Time | Notes |
|--------|------|-------|
| Search Agent | 2-5s | Web search + aggregation |
| Reader Agent | 3-8s | Content scraping |
| Writer Chain | 5-15s | Report generation |
| Critic Chain | 3-10s | Review & scoring |
| **Total** | **15-40s** | Depends on complexity |

## 🐳 Docker Deployment

```bash
# Build Docker image
docker build -t research-assistant .

# Run container
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=sk-... \
  -e ANTHROPIC_API_KEY=sk-... \
  -e SERPAPI_API_KEY=... \
  research-assistant
```

## 🌐 Deployment Options

- **Streamlit Cloud** — Zero-config cloud hosting
- **AWS/GCP/Azure** — Full control & scaling
- **Docker Compose** — Multi-container orchestration
- **Heroku** — One-click deployment

## 📝 Examples

### Example 1: Technology Research
```
Topic: "Latest AI Breakthroughs in 2026"
Output: Comprehensive report with analysis and critic feedback
```

### Example 2: Market Analysis
```
Topic: "Emerging Trends in Renewable Energy"
Output: Structured report with sources and quality score
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.



## 🎯 Roadmap

- [ ] Multi-language support
- [ ] Custom agent templates
- [ ] Real-time collaboration
- [ ] PDF/Word export
- [ ] Advanced caching system
- [ ] Analytics dashboard
- [ ] API endpoint for programmatic access

## ⭐ Acknowledgments

- Built with [LangChain](https://github.com/langchain-ai/langchain)
- UI powered by [Streamlit](https://streamlit.io)
- AI models from [Anthropic](https://anthropic.com) & [OpenAI](https://openai.com)

---

**Made with ❤️ by Zubair Iqbal** |)
````