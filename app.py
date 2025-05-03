from flask import Flask, render_template, request, jsonify
from main import AdamAI
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Initialize AdamAI
adam_ai = None

def initialize_ai():
    global adam_ai
    adam_ai = AdamAI()
    print("AdamAI initialized")

# Start initialization in background
init_thread = threading.Thread(target=initialize_ai)
init_thread.daemon = True
init_thread.start()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    if not adam_ai:
        return jsonify({
            "response": "*clay crumbles* I am still waking up...",
            "status": "initializing"
        })
    
    data = request.get_json()
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({"response": "", "status": "empty"})
    
    # Simulate typing delay
    time.sleep(0.5)
    
    try:
        response = adam_ai.query(message)
        return jsonify({
            "response": response,
            "status": "success"
        })
    except Exception as e:
        return jsonify({
            "response": "*dust falls* My knowledge fails me...",
            "status": "error"
        })

if __name__ == '__main__':
    app.run(debug=True)