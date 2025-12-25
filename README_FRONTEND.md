# Medical Agentic RAG System - Frontend

A beautiful, modern web interface for the Medical Agentic RAG (Retrieval-Augmented Generation) system built with Flask, featuring an intelligent routing system that dynamically selects the best data source for medical queries.

## 🌟 Features

- **Intelligent Routing**: Automatically determines whether to search Medical Q&A database, Medical Device Manuals, or perform Web Search
- **Real-time Workflow Visualization**: See the decision-making process in action
- **Context Relevance Check**: Ensures retrieved information is relevant to the query
- **Beautiful Modern UI**: Dark-themed, responsive design with smooth animations
- **Example Queries**: Quick-start with pre-populated medical questions
- **Metadata Display**: Shows route decision, information source, and relevance status

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- All dependencies from the original `agentic_RAG.py` project
- Flask web framework

### Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Ensure your environment variables are set**:
   - OpenAI API key
   - Google Serper API key (for web search)

3. **Make sure ChromaDB collections are initialized**:
   - The app requires `collection1` (Medical Q&A) and `collection2` (Medical Device Manuals) from `chromaDB.py`

### Running the Application

1. **Start the Flask server**:
```bash
python app.py
```

2. **Open your browser** and navigate to:
```
http://localhost:5000
```

3. **Start asking medical questions!**

## 📁 Project Structure

```
rag_agentic/
├── app.py                          # Flask backend server
├── agentic_RAG.py                 # Core agentic RAG logic
├── chromaDB.py                    # Vector database collections
├── results_openai.py              # LLM integration
├── requirements.txt               # Python dependencies
├── templates/
│   └── index.html                 # Main web interface
└── static/
    ├── style.css                  # Beautiful styling
    └── script.js                  # Interactive functionality
```

## 🎯 How It Works

1. **User Input**: Enter a medical query in the text area
2. **Router Decision**: AI decides which data source to use:
   - `Retrieve_QnA`: General medical knowledge, symptoms, treatments
   - `Retrieve_Device`: Medical devices, manuals, instructions
   - `Web_Search`: Recent news, brand names, external data
3. **Context Retrieval**: Fetches relevant information from the chosen source
4. **Relevance Check**: Verifies if the retrieved context is relevant
5. **Response Generation**: Creates an informed answer using the context
6. **Display Results**: Shows the answer with full metadata and workflow visualization

## 🎨 UI Features

- **Dark Modern Theme**: Easy on the eyes for medical professionals
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Smooth Animations**: Elegant transitions and loading states
- **Keyboard Shortcuts**: Press Ctrl/Cmd + Enter to submit queries
- **Example Queries**: Quick-start buttons for common questions
- **Workflow Visualization**: See each step of the agentic process

## 📝 Example Queries

Try these queries to see the system in action:

1. "What are the treatments for Kawasaki disease?"
2. "What are the usage of Dialysis Machine Device?"
3. "What are medicines/treatment for COVID?"
4. "What's the export duty on medical tablets on India by USA in 2025?"

## 🔧 Configuration

### Modifying the Workflow

The agentic workflow is defined in `agentic_RAG.py`. You can customize:
- Routing logic in the `router()` function
- Relevance checking criteria in `check_context_relevance()`
- Number of results retrieved (`n_results` parameter)
- Response length limit in the prompt

### Styling Customization

Edit `static/style.css` to customize:
- Color scheme (CSS variables in `:root`)
- Layout and spacing
- Animations and transitions
- Responsive breakpoints

## 🐛 Troubleshooting

### Port Already in Use
If port 5000 is already in use, change it in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

### ChromaDB Not Found
Ensure your ChromaDB collections are properly initialized:
```python
python chromaDB.py
```

### API Keys Not Set
Set your environment variables:
```bash
export OPENAI_API_KEY="your-key-here"
export SERPER_API_KEY="your-key-here"
```

## 🔒 Security Notes

- Always use environment variables for API keys (never hardcode)
- Consider adding rate limiting for production use
- Implement user authentication if deploying publicly
- Use HTTPS in production environments

## 🚀 Production Deployment

For production deployment, consider:

1. **Use a production WSGI server** (e.g., Gunicorn):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Set up a reverse proxy** (e.g., Nginx)

3. **Enable HTTPS** with SSL certificates

4. **Add error logging and monitoring**

5. **Configure CORS** if needed for different domains

## 📄 License

This project is part of the Agentic RAG homework assignment.

## 🙏 Acknowledgments

- Built with LangGraph for workflow orchestration
- Powered by OpenAI for language understanding
- ChromaDB for efficient vector storage
- Google Serper for web search capabilities

