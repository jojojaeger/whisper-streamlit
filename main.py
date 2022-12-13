import whisper
import sys
import docx
from datetime import datetime

#get datetime
date = datetime.today().strftime('%Y-%m-%d')

# define doc
doc = docx.Document()
doc.add_heading('Transcript')

model = whisper.load_model("large")
result = model.transcribe(sys.argv[1], language='german')
print(result["text"])
doc.add_paragraph(result["text"])

doc.save("C:/Users/jaeger/Transcripts/" + sys.argv[1] + date + ".docx")
