from openai import OpenAI

class DeepSeekModelHandler:
    def __init__(self, model_name: str, api_key: str):
        """
        Initialize the DeepSeekModelHandler with the model and OpenRouter-based client.
        :param model_name: e.g. 'openai/gpt-4o'
        :param api_key: Your OpenRouter API key
        """
        self.model_name = model_name
        self.api_key = api_key

        # Create an OpenAI client pointing to OpenRouter's base URL
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key
        )
        
        # Optional: If you want to always send certain extra headers (HTTP-Referer, X-Title, etc.)
        # you can store them as class attributes or pass them at predict-time
        self.extra_headers = {
            "HTTP-Referer": "<YOUR_SITE_URL>",  # Replace <YOUR_SITE_URL> or remove if not needed
            "X-Title": "<YOUR_SITE_NAME>"       # Replace <YOUR_SITE_NAME> or remove if not needed
        }

    def load_model(self):
        """
        No local model loading required; everything is handled via OpenRouter's API calls.
        """
        pass

    def predict(self, context: str, question: str) -> dict:
        """
        Use the OpenAI client (pointing to OpenRouter) for question answering.
        :param context: The context/passage text.
        :param question: The question to ask about that context.
        :return: A dict with {"answer": <str>, "score": <float>}
        """
        if not context.strip():
            return {"answer": "No context provided.", "score": 0.0}

        # Build the messages for a chat completion request
        messages = [
            {
                "role": "user",
                "content": f"Context: {context}\nQuestion: {question}"
            }
        ]

        try:
            # Create a chat completion against the OpenRouter endpoint
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=1024,
                extra_headers=self.extra_headers,  # optional
            )
            print("DEBUG: completion =", completion)

            # Extract the response text
            answer = completion.choices[0].message.content.strip()
            return {"answer": answer, "score": 1.0}

        except Exception as e:
            # Handle potential network/JSON parsing errors
            return {"answer": f"Error calling API: {e}", "score": 0.0}
