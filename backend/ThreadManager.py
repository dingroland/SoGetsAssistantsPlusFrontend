from BaseOpenAIManager import BaseOpenAIManager
import time
#from EventHandler import EventHandler



class ThreadManager(BaseOpenAIManager):
    """
    Handles creation and management of chat threads.
    """
    def create_thread(self) -> dict:
        """Creates a new chat thread and ensures correct return format."""
        try:
            thread = self.client.beta.threads.create()
            return {"id": thread.id, "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "failure"}
    
    def send_message(self, thread_id: str, message: str) -> dict:
        """Sends a message in an existing chat thread."""
        try:
            message_response = self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message
            )
            return {"id": message_response.id, "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "failure"}
        



    def stream_assistant_response(self, thread_id: str, assistant_id: str):
        """Simulates streaming by retrieving the response and printing it line by line."""
        try:
            # Run the assistant and wait for completion
            run_response = self.client.beta.threads.runs.create_and_poll(
                thread_id=thread_id,
                assistant_id=assistant_id
            )
            
            # Retrieve the completed messages
            messages = self.client.beta.threads.messages.list(thread_id=thread_id, run_id=run_response.id)
            
            # Get the assistant's last message
            assistant_message = next((msg for msg in messages.data if msg.role == "assistant"), None)
            
            if assistant_message:
                response_text = assistant_message.content[0].text.value
                for line in response_text.split(". "):  # Split by sentence for smooth printing
                    print(line.strip() + ".", flush=True)
                    time.sleep(0.2)  # Simulate streaming delay
            else:
                print("Error: No assistant response found.")
        
        except Exception as e:
            yield(f"Error: {str(e)}")




    
    def get_thread_messages(self, thread_id: str) -> dict:
        """Retrieves all messages from a chat thread."""
        try:
            messages = self.client.beta.threads.messages.list(thread_id=thread_id)
            return {"messages": messages.data, "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "failure"}
    
    def run_assistant(self, thread_id: str, assistant_id: str) -> dict:
        """Executes the assistant on a thread to generate a response."""
        try:
            run_response = self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id
            )
            return {"run_id": run_response.id, "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "failure"}
        

    
    def delete_thread(self, thread_id: str) -> dict:
        """Deletes a chat thread and all its messages."""
        try:
            self.client.beta.threads.delete(thread_id=thread_id)
            return {"status": "success", "message": f"Thread {thread_id} deleted."}
        except Exception as e:
            return {"error": str(e), "status": "failure"}
        




    def get_assistant_response(self, thread_id: str, assistant_id: str) -> str:
        """Retrieves the latest assistant message from a thread using v2 API."""
        try:
            # ✅ Create a new run
            run_response = self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id
            )
            run_id = run_response.id

            # ✅ Poll for completion
            while True:
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run_id
                )
                print(f"🟡 Assistant Run Status: {run_status.status}")  # Debugging output

                if run_status.status == "completed":
                    break
                elif run_status.status in ["failed", "cancelled"]:
                    return f"⚠ Error: Assistant run failed with status {run_status.status}"
                
                time.sleep(0.5)

            # ✅ Retrieve the messages correctly
            messages = self.client.beta.threads.messages.list(thread_id=thread_id)
            assistant_message = next((msg for msg in messages.data if msg.role == "assistant"), None)

            if assistant_message:
                return assistant_message.content[0].text.value.strip()
            else:
                return "⚠ No response from assistant."
        
        except Exception as e:
            return f"⚠ Error retrieving response: {str(e)}"