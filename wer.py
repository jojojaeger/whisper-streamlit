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

with open('hyp.txt', 'w') as f:
    f.write(hypothesis)

args = ['wer', 'ref.txt', 'hyp.txt', '-c']

# Call the wer script with the specified arguments
process = Popen(args, stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()

# Print the output to the console

outtext = stdout.decode('latin-1')

# Sperate strings for each section (not tested yet)
outtext = outtext.split("INSERTIONS:")[0]
insertions, rest = outtext.split("DELETIONS:")
deletions, rest = rest.split("SUBSTITUTIONS:")
substitutions, wer_info = rest.split("Sentence Count:")

# TODO: write each string to a text file
with open('result.txt', 'w', encoding="UTF-8") as f:
    f.write(outtext)

csv = pd.read_csv("result.txt", sep=" ")
csv.to_csv(r'result.csv', index=None)
#print('stdout:', stdout.decode('latin-1'))
#print('stderr:', stderr.decode())
