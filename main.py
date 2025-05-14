import os
from mistralai import Mistral
import argparse


class Model:

    '''
    Take pdf and extarct text from that and save that extracted text as a text file

    Args: take pdf path as a string 

    output : Save a text file with the extracted text from the pdf

    '''

    def __init__(self):

        api_key = os.environ.get("API_KEY_MISTRAL")
        self.model = "mistral-small-latest"
        self.client = Mistral(api_key=api_key)

    
    def extract(self , pdf_path : str , output_file : str)-> None:

        self.pdf_path = pdf_path
        self.output_file = output_file


        print(f"PDF_PATH {self.pdf_path} {type(self.output_file)} ")
        print(f"OUTPUT PDF PATH {self.output_file} {type(self.output_file)}")
        # If local document, upload and retrieve the signed url

        try:
            uploaded_pdf = self.client.files.upload(
                file={
                    "file_name": self.pdf_path,
                    "content": open(self.pdf_path, "rb"),
                },
                purpose="ocr"
            )
        except Exception as error:
            return f"{str(error)} upload file line 43"

        
        try:
            signed_url = self.client.files.get_signed_url(file_id=uploaded_pdf.id)
        except Exception as error:
            return f"{str(error)} signed url line 49"

        
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "give all the text from the pdf except special words and brackets"
                    },
                    {
                        "type": "document_url",
                        #"document_url": "https://arxiv.org/pdf/1805.04770"
                        "document_url": signed_url.url
                    }
                ]
            }
        ]

        # Mistral client
        chat_response = self.client.chat.complete(
            model=self.model,
            messages=messages
        )


        print(chat_response.choices[0].message.content)


        with open(self.output_file,"w",encoding="utf-8") as f:
            for i in chat_response.choices[0].message.content:
                f.write(i)

        root_folder = os.getcwd()
        saved_file_path = os.path.join(root_folder , self.output_file)
        return saved_file_path



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Take the pdf path")
    parser.add_argument('pdf_path',help="pdf path for the text extraction")
    parser.add_argument('--output' ,'-o' , help ="output file name for saving the extracted text from the pdf")
    args = parser.parse_args()

    pdf_path = args.pdf_path
    output_file = args.output

    print(pdf_path)
    print(output_file)

    model = Model()
    pdf_path = model.extract(pdf_path , output_file)
    print(f"Saved Extracted Text File{pdf_path}")