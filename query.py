import math

def load_vocab():
    vocab = {}
    with open('vocab.txt', 'r') as f:
        vocab_terms = f.readlines()
        
    with open('idf-values.txt', 'r') as f:
        idf_values = f.readlines()
        
    
    for (term,idf_value) in zip(vocab_terms, idf_values):
        vocab[term.strip()] = int(idf_value.strip())
    
    return vocab

def load_documents():
    documents = []
    with open('documents.txt', 'r') as f:
        documents = f.readlines()
    documents = [document.strip().split() for document in documents]

    
    return documents

def load_links():
    links=[]
    with open('Qdata/Qindex.txt', 'r') as f:
        links = f.readlines()
    links = [link.strip() for link in links]
    return links

def load_inverted_index():
    inverted_index = {}
    with open('inverted_index.txt', 'r') as f:
        inverted_index_terms = f.readlines()
    print(len(inverted_index_terms))
    for row_num in range(0,len(inverted_index_terms),2):
        term = inverted_index_terms[row_num].strip()
       
        #this the term, that the word
        documents = inverted_index_terms[row_num+1].strip().split()
        #this is the array of documets in which the word term is their
        inverted_index[term] = documents
        #storing the array as value for the term as key
    
    return inverted_index



vocab_idf_values = load_vocab()

documents = load_documents()

inverted_index = load_inverted_index()

links = load_links()

#Now what i have in this
#1st I have the documets and their index
#2nd I have the vocab of each word, like how many times a word is repeated
#3rd I have the inverted_index, like i have the key is the word and the value as the
#index of document in which it apperas..Its also like a JSON file.


def get_tf_dictionary(term):
    tf_values = {}
    if term in inverted_index:
         for document in inverted_index[term]:
             if document not in tf_values:
                 tf_values[document] = 1
             else:
                 tf_values[document] += 1

         
    for document in tf_values:
         tf_values[document] /= len(documents[int(document)])
    
    return tf_values


def get_idf_value(term):
     return math.log(len(documents)/vocab_idf_values[term])

def calculate_sorted_order_of_documents(query_terms):
     potential_documents = {}
     for term in query_terms:
         if vocab_idf_values[term] == 0:
             continue
         tf_values_by_document = get_tf_dictionary(term)
         idf_value = get_idf_value(term)
    
         for document in tf_values_by_document:
             if document not in potential_documents:
                 potential_documents[document] = tf_values_by_document[document] * idf_value
             potential_documents[document] += tf_values_by_document[document] * idf_value

    #   divite by the length of the query terms
     for document in potential_documents:
         potential_documents[document] /= len(query_terms)

     potential_documents = dict(sorted(potential_documents.items(), key=lambda item: item[1], reverse=True))

     for document_index in potential_documents:
         print('Document: ', ' '.join(documents[int(document_index)]), links[int(document_index)], ' Score: ', potential_documents[document_index])


query_string = input('Enter your query: ')
query_terms = [term.lower() for term in query_string.strip().split()]


calculate_sorted_order_of_documents(query_terms)