from dotenv import load_dotenv
import openai
import json
import os

class OpenAIModel:
    """
    A class to interact with the OpenAI API for extracting the fields required from the pdf.

    Attributes
    ----------
    model : str
        The name of the OpenAI model. Ex. 'gpt-4o-mini', 'gpt-4o', etc.

    Methods
    -------
    get_fields(text: str) -> json
        Prompts the model to extract the required fields from the extracted text from the pdf.
    _load_prompt(**kwargs) -> str
        Loads the model prompt from the text file into a string, ready to be sent to the API.
    _parse_response(response: str) -> json
        Parses the response from the model into json format.
    """

    def __init__(self, model):
        # Load and set the openai key
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model # model to be used

    def get_fields(self, text):
        """
        Extracts:
            - All lab test names and their values
        By sending a query to the OpenAI API

        Arguments:
            text (str): The text to extract the fields from.

        Returns:
            final_response (json): The json response from the OpenAI API.

        Example Output:
            {
            "lab_results": [
                {"test_name": "Hemoglobin", "value": "14.2"},
                {"test_name": "HDL Cholesterol", "value": "50"}
            ]
            }
        """

        try:
            # Configure the OpenAI API call
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content":
                        "You are an AI assistant specialized in extracting structured data from text. Always respond "
                        "strictly in the JSON format provided by the user, without additional text, explanations, or "
                        "commentary. If a field is not present in the input, return 'not present' as the value for that field."},
                    {"role": "user", "content": str(self._load_prompt(extracted_text=text))}, # specialized prompt with text
                ],
                temperature=0 # Deterministic responses
            )

            # Parse the response from OpenAI into json
            final_response = self._parse_response(response)

            return final_response
        except Exception as e:
            raise RuntimeError(f"Failed to get response from OpenAI API: {e}")

    def _load_prompt(self, **kwargs):
        """
        Loads the model prompt from the text file into a string, ready to be sent to the API.

        Arguments:
            **kwargs: the extracted text from the pdf to insert into the prompt

        Returns:
            formatted_prompt (str): The formatted prompt for the model.

        Raises:
            RuntimeError: If the prompt failed to load.
        """
        try:
            prompt_path = os.path.join(os.path.dirname(__file__), "..", "..", "prompts", "open_ai_prompt.txt")
            prompt_path = os.path.abspath(prompt_path)
            with open(prompt_path, "r", encoding="utf-8") as prompt_file:
                prompt_template = prompt_file.read()

            # Insert the text into the prompt
            formatted_prompt = prompt_template.format(**kwargs)
            return formatted_prompt
        except Exception as e:
            raise RuntimeError(f"Failed to load prompt: {e}")

    def _parse_response(self, response):
        """
        Parses the response from the model into json format.

        Arguments:
            response (ChatCompletion): The response from the OpenAI API.

        Returns:
            parsed_response (json): The json format of the OpenAI API response.

        Raises:
            Exception: If the response could not be parsed into json format or missing fields in OpenAI API response.
        """
        try:
            # Parse the response into json
            parsed_response = json.loads(response.choices[0].message.content)

            # Check if 'lab_results' is in the json response
            if "lab_results" not in parsed_response:
                raise RuntimeError(f"'lab_results' field is not present in response: {parsed_response}")

            return parsed_response
        except Exception as e:
            raise RuntimeError(f"Failed to parse response into json: {e}")



