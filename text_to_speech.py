import os
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import argparse
from dotenv import load_dotenv


load_dotenv()

class TextToSpeech:

    def __init__(self):

        self.client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    def text_to_speech_file(self,file_path) -> str:
        
        self.file = file_path

        self.text = ""

        with open(self.file , 'r' , encoding='utf-8') as f:
            self.text+=f.read()

        response = self.client.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB", 
            output_format="mp3_22050_32",
            text=self.text,
            model_id="eleven_turbo_v2_5", 
            
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
                speed=1.0,
            ),
        )

        
        save_file_path = self.file.replace('.txt','.mp3')

        with open(save_file_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)

        print(f"{save_file_path}: A new audio file was saved successfully!")

        return save_file_path



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Take the text file path and give the speech to text audio")
    parser.add_argument('path' , help="Enter the text file path for text to audio")

    args = parser.parse_args()

    model = TextToSpeech()
    response = model.text_to_speech_file(args.path)
    print(response)