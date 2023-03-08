# coding: utf8
from subprocess import Popen, PIPE
import jiwer
import sys
import docx
import pandas as pd


def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return ' '.join(fullText)

def transformation(text):
    text = jiwer.RemovePunctuation()(text)
    text = jiwer.ToLowerCase()(text)
    text = jiwer.RemoveWhiteSpace(replace_by_space=True)(text)
    text = jiwer.RemoveMultipleSpaces()(text)
    return text

ground_truth = transformation(getText(sys.argv[1]))

hypothesis = transformation(getText(sys.argv[2]))

measures = jiwer.compute_measures(ground_truth, hypothesis, truth_transform=jiwer.ReduceToListOfListOfWords(word_delimiter=" "),
                                  hypothesis_transform=jiwer.ReduceToListOfListOfWords(word_delimiter=" "))

print("WER", sys.argv[1], sys.argv[2], "=", measures["wer"])

print(measures["substitutions"])

with open('ref.txt', 'w') as f:
    f.write(ground_truth)
    f.close()

with open('hyp.txt', 'w') as f:
    f.write(hypothesis)
    f.close()

args = ['wer', 'ref.txt', 'hyp.txt', '-c']

# Call the wer script with the specified arguments
process = Popen(args, stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()

# Print the output to the console
outtext = stdout.decode('latin-1')
print(outtext)
