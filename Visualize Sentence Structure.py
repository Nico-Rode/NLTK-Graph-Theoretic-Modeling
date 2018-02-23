import nltk
from nltk.corpus import genesis
from nltk.tokenize import PunktSentenceTokenizer #simple library that does
                                                #most of the hard work for us

file1 = open('file1.txt') #These next few files open up the training data for
                            #which we are able to graph the sentences
file1 = file1.read()
print(file1)

train_text = file1

file2 = open('file2.txt')
file2 = file2.read()




sample_text = file2

custom_sent_tokenizer = PunktSentenceTokenizer(train_text) #this breaks up the
                                            #raw text into individual words
                                            #and sentences and tagged.
                                            #This is when we organize and label the
                                            #data for which the model learns from

tokenized = custom_sent_tokenizer.tokenize(sample_text) #This is the 'real'
                                    #chunking of the data, using what it learned
                                    #from the training text it break this down
                                    #into words and sentences and tags everything
                                    #nothing has been graphed yet


def process_content():
    try:
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}""" #This is the
            #particular phrase of sentence we are looking for. RB is adverb, NNP
            # is a proper noun, etc. A full, in-depth explanation can be found
            # here http://www.nltk.org/book/ch05.html
            chunkParser = nltk.RegexpParser(chunkGram)
            chunked = chunkParser.parse(tagged) #The chunking is where the actual
            #graphing relationship takes place. Whenever it finds a sentence
            #structure it create a subtree and graphs it, you have to exit out
            #of each graph indidually to see the next one

            for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):
                print(subtree)

            chunked.draw()

    except Exception as e:
        print(str(e))


process_content()
