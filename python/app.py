import os
from typing import List, Dict
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

class LLMChat:
    def __init__(self):
        self.hf_token = self._get_huggingface_token()
        self.models = {
            "llama2": HuggingFaceEndpoint(
                repo_id="meta-llama/Llama-2-7b-chat-hf",
                task="text-generation",
                model_kwargs={"temperature": 0.7, "max_length": 512},
                huggingfacehub_api_token=self.hf_token
            ),
            "mistral": HuggingFaceEndpoint(
                repo_id="mistralai/Mistral-7B-v0.1",
                task="text-generation",
                model_kwargs={"temperature": 0.7, "max_length": 512},
                huggingfacehub_api_token=self.hf_token
            )
        }
        self.current_model = None
        self.memory = ConversationBufferMemory(return_messages=True)

    def _get_huggingface_token(self):
        token = os.getenv('HUGGINGFACEHUB_API_TOKEN')
        if not token:
            raise ValueError("HUGGINGFACEHUB_API_TOKEN not found in environment variables.")
        return token
    
    def select_model(self, model_name: str):
        if model_name not in self.models:
            raise ValueError(f"Invalid model name. Choose from {', '.join(self.models.keys())}")
        
        self.current_model = self.models[model_name]
        self.memory = ConversationBufferMemory(return_messages=True)
        print(f"Model {model_name} loaded successfully.")

    def get_response(self, user_input: str) -> str:
        if not self.current_model:
            raise ValueError("Please select a model first.")

        prompt = PromptTemplate(
            input_variables=["chat_history", "human_input"],
            template="""
            The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

            Current conversation:
            {chat_history}
            Human: {human_input}
            AI: """
        )

        chain = LLMChain(llm=self.current_model, prompt=prompt, memory=self.memory)
        response = chain.predict(human_input=user_input)
        return response.strip()

    def get_conversation_history(self) -> List[Dict[str, str]]:
        return self.memory.chat_memory.messages

def main():
    try:
        chat = LLMChat()
    except ValueError as e:
        print(f"Error initializing chat: {e}")
        return

    while True:
        if not chat.current_model:
            model_choice = input("Select a model (llama2/mistral) or 'quit' to exit: ").lower()
            if model_choice == 'quit':
                break
            try:
                chat.select_model(model_choice)
            except ValueError as e:
                print(e)
                continue
        
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        
        try:
            response = chat.get_response(user_input)
            print(f"AI: {response}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()