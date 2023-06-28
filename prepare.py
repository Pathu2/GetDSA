
# Read the file and get the lines
with open("Qdata/index.txt", "r") as f:
    # encoding nhi likha hi
    lines = f.readlines()
    # print(lines)


def preprocess(line):
    terms = [term.lower() for term in line.split()[1:]]
    # .strip() ka use nhi hai toh nhi likh raha
    return terms


documents = []
vocab = {}
# consider vocab like a json like, which has the key value pairs, key is the word and values
# is how many times it being there in all the documents
for line in lines:
    tokens = preprocess(line)
    documents.append(tokens)
    for token in tokens:
        if token not in vocab:
            vocab[token] = 1
        else:
            vocab[token] = vocab[token] + 1

#resverse sorting the vocab
vocab = dict(sorted(vocab.items(), key = lambda item: item[1], reverse=True ))

# saving the key and value in two different text files
with open("vocab.txt", "w") as f:
    for key in vocab.keys():
        f.write(key + '\n')

with open("idf-values.txt", "w") as f:
    for key in vocab.keys():
        f.write("%s\n" % vocab[key])


with open("documents.txt", "w") as f:
    for document in documents:
        f.write("%s\n" % ' '.join(document))
#We have a document in documents as the array of wrods
#to save them as a single line we had use ' '.join() 
#which will join them 

inverted_index = {}

for index, document in enumerate(documents):
    for token in document:
        if token not in inverted_index:
            inverted_index[token] = [index]
            #if you normally write index instead of [] brackets, you will not able to append
            #as it will be considered as single element
        else:
            inverted_index[token].append(index)

with open("inverted_index.txt", "w") as f:
    for key in inverted_index.keys():
        f.write("%s\n" % key)
        f.write("%s\n" % ' '.join([str(doc_id) for doc_id in inverted_index[key]]))