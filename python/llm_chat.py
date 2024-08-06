from flask import Flask, request, jsonify
import app 

flask_app = Flask(__name__)
llm_chat = app.LLMChat()

@flask_app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    model = data.get('model')
    message = data.get('message')
    
    if not model or not message:
        return jsonify({"error": "Missing model or message"}), 400

    try:
        llm_chat.select_model(model)
        response = llm_chat.get_response(message)
        return jsonify({"response": response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=5000)