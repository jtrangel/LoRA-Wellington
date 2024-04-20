import os
from dotenv import load_dotenv
import google.generativeai as genai


class DataPrepper:
    """
    Prepares image data for usage with a LoRA training model via Dreambooth.

    Attributes:
        data_path (str): path where the data is stored locally.
    """
    def __init__(self, data_path: str):
        # Environment
        load_dotenv()
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
        self.data_path = data_path

    def describe_img(self, img_path: str) -> list[str]:
        """
        Calls Gemini API to retrieve keyword descriptions of an image.

        Args:
            img_path (str): Image path, specifically the name.

        Returns:
            list[str]: List of adjectives/keywords describing image.
        """
        text_prompt = ["Describe the image using 15 parameters/keywords. Output an array of these keywords as strings.\
                       Try to use as many adjectives as possible"]

        # Upload file to Gemini API
        sample_file = genai.upload_file(path=img_path, display_name="test file")
        print(f"Uploaded jpg file as: {sample_file.uri}")

        response = self.model.generate_content(contents=text_prompt + [sample_file])

        # Delete file after response. By default it takes 2 days for Google to delete your temp files.
        genai.delete_file(sample_file.name)
        print('Deleted file')

        cleaned_text = response.text.replace("`", "")
        desc = eval(cleaned_text)

        return desc

    def write_file(self, file_name: str, text_list: list[str]) -> None:
        """
        Utility function to write out the descriptions of images to corresponding text files.

        Args:
            file_name (str): Name of the file to be written.
            text_list (list[str]): List of adjectives describing file/image
        """
        text_content = ", ".join(text_list) + "\n"

        with open(f"{self.data_path}/{file_name}.txt", "w") as file:
            file.write(text_content)

        print(f"Wrote {file_name}.txt")

    def setup_dir(self) -> None:
        """
        Utility function to format a directory with the correct filenames.
        """

        counter = 1

        # Loop through all files in the directory
        for filename in os.listdir(self.data_path):

            # No need to rename if file is already in format
            if self.is_integer(os.path.splitext(filename)[0]):
                break

            extension = os.path.splitext(filename)[1]  # .jpg in this case
            new_filename = f"{counter}{extension}"

            os.rename(os.path.join(self.data_path, filename), os.path.join(self.data_path, new_filename))
            counter += 1

        print("Directory set up.")

    @staticmethod
    def is_integer(text: str) -> bool:
        """
        This function checks if a string can be converted to an integer.

        Args:
            text (str): The string to be checked.

        Returns:
            True if the string can be converted to an integer, False otherwise.
        """
        try:
            int(text)
            return True
        except ValueError:
            return False
