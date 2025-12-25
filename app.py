from flask import Flask, render_template, request, jsonify
from agentic_RAG import agentic_rag
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    """Handle the query and return the agentic RAG response."""
    try:
        data = request.get_json()
        user_query = data.get('query', '')
        
        if not user_query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Prepare input state
        input_state = {"query": user_query}
        
        # Track the workflow execution
        workflow_steps = []
        final_response = None
        source = None
        route = None
        is_relevant = None
        
        # Stream through the agentic RAG workflow
        for step in agentic_rag.stream(input_state):
            for key, value in step.items():
                workflow_steps.append(key)
                
                # Capture important metadata
                if "response" in value:
                    final_response = value["response"]
                if "source" in value:
                    source = value["source"]
                if "route" in value:
                    route = value["route"]
                if "is_relevant" in value:
                    is_relevant = value["is_relevant"]
        
        # Return the result
        return jsonify({
            'success': True,
            'response': final_response,
            'source': source,
            'route': route,
            'is_relevant': is_relevant,
            'workflow_steps': workflow_steps
        })
    
    except Exception as e:
        print(f"Error processing query: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5009)

