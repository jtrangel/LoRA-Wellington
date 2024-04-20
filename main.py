import os
from dotenv import load_dotenv
import google.generativeai as genai


class DataPrepper:
    def __init__(self, data_path: str):
        # Environment
        load_dotenv()
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
        self.data_path = data_path

    def describe_img(self, img_path: str) -> list[str]:
        text_prompt = ["Describe the image using 15 parameters/keywords. Output an array of these keywords as strings.\
                       Try to use as many adjectives as possible"]

        # Upload file to Gemini API
        sample_file = genai.upload_file(path=img_path, display_name="test file")
        print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")

        response = self.model.generate_content(contents=text_prompt + [sample_file])
        print(response.text)

        # Delete file after response. By default it takes 2 days for Google to delete your temp files.
        genai.delete_file(sample_file.name)
        print(f'Deleted {sample_file.display_name}.')

        return response.text

    def setup_dir(self) -> None:

        counter = 1

        # Loop through all files in the directory
        for filename in os.listdir(self.data_path):

            extension = os.path.splitext(filename)[1]  # .jpg in this case
            new_filename = f"{counter}{extension}"

            os.rename(os.path.join(self.data_path, filename), os.path.join(self.data_path, new_filename))

            counter += 1

        print("Files renamed successfully!")
