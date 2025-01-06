import google.generativeai as genai
from typing import List, Dict

class AIService:
    def __init__(self, api_key: str, max_history_length: int = 5):
        # Configure the API key for Google Generative AI
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Define chat prompts for different types
        self.chat_prompts = {
'legal': "Provide clear, concise, and accurate legal advice on any topic. Stay focused on the facts and answer logically.",

'psychological': """Provide practical advice on managing stress, anxiety, self-esteem, relationships, and overcoming gender stereotypes. Offer support in a clear and empathetic manner.""",

'general': """Offer useful, concise advice on gender equality, education, career development, leadership, and well-being. Keep responses practical and informative."""

        }
        
        self.max_history_length = max_history_length

    def get_ai_response(self, message: str, context: List[Dict], chat_type: str = 'general') -> str:
        try:
            # Get the corresponding prompt based on chat type
            chat_prompt = self.chat_prompts.get(chat_type, self.chat_prompts['general'])
            
            # Create the chat history
            chat_history = [{'role': 'system', 'content': chat_prompt}]
            
            # Limit the context to the last N messages
            context = context[-self.max_history_length:]
            
            # Add the context messages
            for msg in context:
                role = 'user' if msg['is_user'] else 'assistant'
                chat_history.append({'role': role, 'content': msg['content']})
            
            # Add the current user message
            chat_history.append({'role': 'user', 'content': message})
            
            # Prepare the message list to send to the model
            messages = [msg['content'] for msg in chat_history]
            
            # Call the model synchronously
            response = self.model.generate_content(messages)
            
            return response.text
            
        except Exception as e:
            print(f"Error in AI service: {str(e)}")
            return "Извините, произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте еще раз."
