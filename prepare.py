
import re


with open("Qdata/index.txt", "r", encoding="cp1252") as f:
    lines = f.readlines()

question_data = [''] * 2035
#intialise the question data
encodings = ["utf-8", "cp1252", "utf-16"]
#started from the index 0 to 2034 to read all the files till first time the word "Example"
#used try and catch method to handle errors
for index in range(0, 2034, 1):
    encoded_index = str(index+1)
    file_path = f"Qdata/{encoded_index}/{encoded_index}.txt"

    for encoding in encodings:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                content = f.read()
                match = re.search(r'\bExample\b', content)
                if match:
                    question_data[index] = content[:match.start()].lower().split()
                else:
                    question_data[index] = content.lower().split()
                break
        except UnicodeDecodeError:
            continue

# print(len(lines))
# print(len(question_data))

def preprocess(line):
    terms = [term.lower() for term in line.split()[1:]]
    return terms

documents = []
vocab = {}

for index, line in enumerate(lines):
    tokens = preprocess(line)
    question_lines = question_data[index]
    combined_tokens = tokens + [line.strip() for line in question_lines]
    documents.append(combined_tokens)
    for token in tokens:
        if token not in vocab:
            vocab[token] = 1
        else:
            vocab[token] += 1

vocab = dict(sorted(vocab.items(), key=lambda item: item[1], reverse=True))
#sorting the vocab

with open("vocab.txt", "w", encoding="utf-8-sig") as f:
    for key in vocab.keys():
        f.write(key + '\n')

with open("idf-values.txt", "w", encoding="utf-8-sig") as f:
    for key in vocab.keys():
        f.write("%s\n" % vocab[key])

with open("documents.txt", "w", encoding="utf-8-sig") as f:
    for document in documents:
        f.write("%s\n" % ' '.join(document))
#saving the terms and number of occurence and getting the documnets 
inverted_index = {}

for index, document in enumerate(documents):
    for token in document:
        if token not in inverted_index:
            inverted_index[token] = [index]
        else:
            inverted_index[token].append(index)

with open("inverted_index.txt", "w", encoding="utf-8-sig") as f:
    for key in inverted_index.keys():
        f.write("%s\n" % key)
        f.write("%s\n" % ' '.join([str(doc_id) for doc_id in inverted_index[key]]))
