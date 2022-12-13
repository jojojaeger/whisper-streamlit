import whisper
import sys
import docx
from datetime import datetime

# get datetime
date = datetime.today().strftime('%Y-%m-%d')

# define doc
doc = docx.Document()

# models: large, medium (2x), small (6x), base (16x), tiny (32x as fast as large one)
model = whisper.load_model("large")
result = model.transcribe(sys.argv[1])
print(result["text"])
doc.add_paragraph(result["text"])
# path 
doc.save("C:/Users/Anna/Transcripts/" + sys.argv[1] + date + ".docx")
