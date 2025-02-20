from BaseOpenAIManager import BaseOpenAIManager

class AssistantManager(BaseOpenAIManager):
    """
    Handles creation and management of OpenAI Assistants for different companies.
    """
    def create_vector_store(self, company_id: str) -> dict:
        """Creates a vector store for a company."""
        try:
            vector_store = self.client.beta.vector_stores.create(
                name=f"{company_id}_vector_store"
            )
            return {"vector_store_id": vector_store.id, "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "failure"}
    
    def create_assistant(self, company_id: str, description: str = None, model: str = "gpt-4o-mini") -> dict:
        """Creates an OpenAI Assistant for a company and ensures a vector store exists."""
        vector_response = self.create_vector_store(company_id)
        vector_store_id = vector_response.get("vector_store_id")
        
        # Generate optimized assistant description if provided
        if description:
            description = self.generate_assistant_description(description)
        else:
            description = "You are a knowledgeable assistant designed to help users with their queries."
        
        try:
            assistant = self.client.beta.assistants.create(
                name=f"{company_id}_assistant",
                model=model,
                instructions=description,
                tools=[{"type": "file_search"}],  # Enable file search
                tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}}  # Correctly attach vector store
            )
            return {
                "assistant_id": assistant.id, 
                "vector_store_id": vector_store_id, 
                "status": "success"
            }
        except Exception as e:
            return {"error": str(e), "status": "failure"}
    
    def generate_assistant_description(self, company_description: str) -> str:
        """Uses GPT-4o to generate an optimized assistant description based on the company info, ensuring document priority."""
        try:
            prompt = (
                "You are an AI that helps craft optimized assistant descriptions. "
                "The assistant is designed for a company and must STRICTLY prioritize answering questions using uploaded company documents. "
                "If relevant information exists in a document, it should ALWAYS be used and CITED. "
                "Only provide general knowledge if no relevant document information exists. "
                "Ensure the response is structured, concise, and always references sources when possible. "
                "\n\nCompany Description:\n"
                f"{company_description}\n\n"
                "Generate a clear and effective assistant description that enforces these rules."
            )
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You create assistant descriptions that strictly enforce document-based responses."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return (
                "I am an AI assistant designed to prioritize answering questions using uploaded company documents. "
                "If relevant information is found in a document, I will always use it and cite the source. "
                "Only when no relevant document information is available, I will provide general knowledge. "
                "I ensure responses are structured, concise, and provide sources where applicable."
            )

        


    def update_assistant_instructions(self, assistant_id: str, new_instructions: str) -> dict:
        """Updates the assistant's instructions dynamically."""
        try:
            assistant = self.client.beta.assistants.update(
                assistant_id=assistant_id,
                instructions=new_instructions
            )
            return {"status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "failure"}


    
    def get_assistant(self, assistant_id: str) -> dict:
        """Retrieves assistant details by ID."""
        return self.handle_api_call(
            self.client.beta.assistants.retrieve,
            assistant_id
        )
    
    def delete_assistant(self, assistant_id: str) -> dict:
        """Deletes an OpenAI Assistant."""
        return self.handle_api_call(
            self.client.beta.assistants.delete,
            assistant_id
        )