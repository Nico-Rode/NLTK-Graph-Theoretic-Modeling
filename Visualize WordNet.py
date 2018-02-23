from nltk.corpus import wordnet as wn
import networkx as nx
import matplotlib.pyplot as plt
import pydot
import graphviz

def closure_graph(synset, fn):
    seen = set()
    graph = nx.DiGraph() #Setting the type of graph; this is a very useful library for visualizing different 
                            #types of graphs

    #This function goes through each node in our list and adds them to the graph along with edges it hasn't
    #already done so
    def recurse(s): 
        if not s in seen:
            seen.add(s)
            graph.add_node(s.name())
            for s1 in fn(s):
                graph.add_node(s1.name())
                graph.add_edge(s.name(), s1.name())
                recurse(s1)

    recurse(synset)
    return graph

    return G

#This functions primary use is to give the user different options to explore the realtionships between words
#in the wordnet corpus. Given different UI options like which word, which definition, and relation sought to be
#graphed it is a powerful visualiztion tool
def ui_interface():
    wn_word = None
    wn_word_s = None
    word = input('Enter a word: ')
    print("You entered: '%s'" % word)

    word_synsets = []
    try:
        wn_word = wn.synsets(word)#This essentially looks the word up in the WordNet Corpus
        # print wn_word
        print("Choose a Synset of your entry, '%s'" % (word,))
        for i, w in enumerate(wn_word):
            # import pdb; pdb.set_trace()
            print("{0}) '{1}' -- definition: '{2}'".format(i, w.name(), w.definition())) #Lists all of the definitions found
    except Exception:
        print('Please enter only one word')

    try:
        p = input('Your selection for first: ')
        wn_word = wn.synsets(word)[int(p)].name() #Once the user selects the preferred definition we can narrow our search down even further
        print(wn_word)
        wn_word_s = wn.synset(wn_word)
    except Exception as e:
        print(e)
        print('Please enter only a number value from the list.')


    # Store method call and description in one variable as a list of tuples...
    sel_relation = [
        ('root_hypernyms', 'The most abstract/general containing class for A'),
        ('hyponyms', 'A is a hyponym of B iff B is a type of A'),
        ('member_holonyms', 'A is a member holonym of B iff B-type things are member of A-type things'),
        ('substance_holonyms', 'A is a substance holonym of B iff B-type things are constituted of A-type things'),
        ('part_holonyms', 'A is a part holonym of B iff B-type things are subparts of A-type things'),
        ('member_meronyms', 'A is a member meronym of B iff A-type things are members of B-type things'),
        ('substance_meronyms', 'A is a substance meronym of B iff A-type things are consisted of B-type things'),
        ('part_meronyms', 'A chair is made up of legs and a back'),
        ('hypernyms', 'Which categories does dog belong to')
    ]

    for j, z in enumerate(sel_relation):
        print("%s) '%s' -- %s." % (j, z[0], z[1]))

    try:
        jj = input('Your selection for second: ')
        # Basic form of the call generating the graph,
        # graph = closure_graph(wn_word_s, lambda s: s.hypernyms())
        # The rest of the code just works to manage the list of tuples...
        sel = sel_relation[int(jj)][0]
        print(sel)
        graph = closure_graph(wn_word_s, lambda s: getattr(s, sel)())
        plot_graph(graph)
    except Exception as e:
        print(e)
        print('Please enter only a number value from the list.')

def plot_graph(G):
    plt.show()
    pos = nx.spring_layout(G, scale=G.size()*19)
    size = G.size()
    print(size)
    node = 0
    font = 0
    if size < 200:
        node = 50
        font = 3
    elif size < 500:
        node = .5
        font = .5
    else:
        node = .3
        font = .4


    nx.draw(G, width=.1, with_labels=True, pos=pos, node_size = node, font_size= font)
    plt.savefig("path2.pdf")

ui_interface()
