from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

'''
bodies from 2-preprocessing data frame's body column
'''


if __name__ == '__main__' :

    #1. make lower case, regulazation
    l_bodies=[]
    for body in bodies :
        
        body = str(body).lower()
        l_bodies.append(body)

        
    #2. removing stop words, tokenize
    stop_words = set(stopwords.words('english'))

    token_sentence = []
    for words in l_bodies:
        word_tokens= word_tokenize(words)
        filter_sentence = [fw for fw in word_tokens if not fw in stop_words]
        
        for n in range(len(filter_sentence)) :
            if filter_sentence[n] == 'collapse' :
                filter_sentence[n]  = 'collapsed'
        
        ## fall + fell => fall (less frequency of fall just go with fell) , collapsed +collapse => collapse
        #filter_sentence = nltk.pos_tag(filter_sentence)
        token_sentence.append(filter_sentence)
    