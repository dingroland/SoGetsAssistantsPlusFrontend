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
        



    def stream_assistant_response_gui(self, thread_id: str, assistant_id: str, chat_display):
        """Simulates streaming by retrieving the response and displaying it in the GUI chat window."""
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
                chat_display.append("🤖 Assistant: ")  # Initial placeholder

                for line in response_text.split(". "):  # Split by sentence for smooth printing
                    line = line.strip() + "."
                    print(line, flush=True)  # Still prints in terminal
                    chat_display.append(line)  # Show line in GUI
                    chat_display.ensureCursorVisible()
                    QApplication.processEvents()
                    time.sleep(0.2)  # Simulate streaming delay

            else:
                chat_display.append("🤖 Assistant: Error: No response found.")
        
        except Exception as e:
            chat_display.append(f"🤖 Assistant: Error: {str(e)}")



    def get_assistant_response(self, thread_id: str, assistant_id: str) -> str:
        """Retrieves the latest assistant message from a thread."""
        try:
            # Poll the assistant for a response
            run_response = self.client.beta.threads.runs.create_and_poll(
                thread_id=thread_id,
                assistant_id=assistant_id
            )

            # Retrieve the messages from the thread
            messages = self.client.beta.threads.messages.list(thread_id=thread_id, run_id=run_response.id)

            # Get the latest assistant message
            assistant_message = next((msg for msg in messages.data if msg.role == "assistant"), None)

            if assistant_message:
                return assistant_message.content[0].text.value.strip()
            else:
                return "⚠ No response from assistant."
        
        except Exception as e:
            return f"⚠ Error retrieving response: {str(e)}"
