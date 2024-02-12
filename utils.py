from openai import OpenAI
import os

client = OpenAI()


def download_file(file):
    # Get file extension from the file_path
    extension = file.file_path.split('.')[-1]
    # download file
    file.download(f"downloads/message.{extension}")
    # path
    return f"downloads/message.{extension}"


def translation(path):
    resp = client.audio.translations.create(
      model="whisper-1", 
      file=open(path, "rb"),
    )
    text=resp.text
    print(text)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.0,
        messages=[
            {
                "role": "system",
                "content": "Du er en english-til-dansk tolk og oversætterekspert. Teksten nedenfor er en udskrift fra en lyd, der tales på english. Oversæt det til dansk og giv yderligere kommentarer, hvis de kunne hjælpe med at forstå konteksten af samtalen bedre."
            },
            {
                "role": "user",
                "content": text,
            }
        ]
    )
    return response.choices[0].message.content


def transcription(path):
    resp = client.audio.transcriptions.create(
      model="whisper-1", 
      file=open(path, "rb"),
      language="th",  
    )
    text=resp.text
    print(text)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.0,
        messages=[
            {
                "role": "system",
                "content": "Du er en thai-til-dansk tolk og oversætterekspert. Teksten nedenfor er en udskrift fra en lyd, der tales på thai. Oversæt det til dansk og giv yderligere kommentarer, hvis de kunne hjælpe med at forstå konteksten af samtalen bedre."
            },
            {
                "role": "user",
                "content": text,
            }
        ]
    )
    return response.choices[0].message.content


