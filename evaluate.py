# coding: utf8
import jiwer
import sys
import docx

def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

ground_truth = getText(sys.argv[1])
hypothesis = getText(sys.argv[2])

ground_truth = jiwer.RemovePunctuation()(ground_truth)

hypothesis = jiwer.RemovePunctuation()(hypothesis)
 
transformation = jiwer.Compose([
    jiwer.ToLowerCase(),
    jiwer.RemoveWhiteSpace(replace_by_space=True),
    jiwer.RemoveMultipleSpaces(),
    jiwer.ReduceToListOfListOfWords(word_delimiter=" ")
])

error = jiwer.wer(
    ground_truth,
    hypothesis,
    truth_transform=transformation,
    hypothesis_transform=transformation
)

print(error)
