# Python LLM Chat Application
Python LLM interacting with Llama 2 and Mistral language models using the Hugging Face API and Langchain.

## Quick Start

1. Clone and navigate to the repository:
   ```
   git clone https://github.com/emman25/llm.git
   cd llm/python
   ```

2. Create virtual environment:
   ```
   python -m venv base
   source base/bin/activate  # On Windows use `base\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set your Hugging Face API token:
   ```
   export HUGGINGFACEHUB_API_TOKEN='your-token-here'
   ```

5. Run the app:
   ```
   python llm_chat.py [API]

   or

   python app.py [Console]
   ```


The API will be available at `http://localhost:5000`.

## API Usage

Send POST requests to `/chat` endpoint:
```
curl -X POST http://localhost:5000/chat \
     -H "Content-Type: application/json" \
     -d '{"model": "llama2", "message": "Hello, how are you?"}'
```

## Docker Usage

Build and run with Docker:
```
docker build -t python-llm-chat .
docker run -p 5000:5000 -e HUGGINGFACEHUB_API_TOKEN='your-token-here' python-llm-chat
```

## Project Structure

- `app.py`: Contains Langchain declarations and LLM chat logic
- `llm_chat.py`: Flask API server that uses the logic from `app.py`

## Notes

- Requires Python 3.11+ and a Hugging Face account
- Modify `app.py` to change models or parameters
- Modify `llm_chat.py` to adjust API behavior