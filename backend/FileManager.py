from BaseOpenAIManager import BaseOpenAIManager

class FileManager(BaseOpenAIManager):
    """
    Handles document uploads for OpenAI Assistants.
    """
    def upload_file(self, file_path: str) -> dict:
        """Uploads a file and returns its file ID."""
        try:
            with open(file_path, "rb") as file:
                uploaded_file = self.client.files.create(
                    file=file,
                    purpose="assistants"
                )
            return {"file_id": uploaded_file.id, "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "failure"}

    def upload_file_to_vector_store(self, file_path: str, vector_store_id: str) -> dict:
        """Uploads a file and links it to a vector store."""
        try:
            upload_response = self.upload_file(file_path)
            if "file_id" in upload_response:
                return self.handle_api_call(
                    self.client.beta.vector_stores.files.create,
                    vector_store_id=vector_store_id,
                    file_id=upload_response["file_id"]
                )
            return upload_response
        except Exception as e:
            return {"error": str(e), "status": "failure"}

    def list_files(self) -> dict:
        """Lists all uploaded files."""
        return self.handle_api_call(self.client.files.list)

    def delete_file(self, file_id: str) -> dict:
        """Deletes an uploaded file."""
        return self.handle_api_call(
            self.client.files.delete,
            file_id
        )