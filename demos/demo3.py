# coding: utf-8
class disfluencyTagger:
    def __init__(self):
        pass
    def run(self):
        pass
    def getEditTerms(self):
        pass
    def getAndSaveFeedbackWithScore(self):
        pass

# In[1]:
class demo3(disfluencyTagger):
    def __init__(self):
        self.map = {}
        self.edit_Terms = {}
        self.words = []
        self.wordIndex=0
        self.rmStart = {} # id and position
        self.rpEnd = {} # id and position###the id in the tag is where the repair ends!!!!!! #### General cases not mentioned in research work!
        self.rpStart = {}
        # sentenceStart = {} # id and position ################################TO DO ~~~~~~~~~~~~~~
        self.sentenceIndex = 0 # start of the sentence
        self.repairSentence = {} # id and position of start os sentence
        self.rpnsub = {} # substitution repair
        self.rpnrep = {} # repetition repair
        self.rpndel = {} # deletion repair

        try:
            import deep_disfluency
        except ImportError:
            print "no installed deep_disfluency package, pathing to source"
            import sys
            sys.path.append("../")
        from deep_disfluency.tagger.deep_tagger import DeepDisfluencyTagger


        # In[2]:

        # Initialize the tagger from the config file with a config number
        # and saved model directory
        MESSAGE = """1. Disfluency tagging on pre-segmented utterances
        tags repair structure incrementally and other edit terms <e/>
        (Hough and Schlangen Interspeech 2015 with an RNN)
        """
        print MESSAGE
        self.disf = DeepDisfluencyTagger(
            config_file="../deep_disfluency/experiments/experiment_configs.csv",
            config_number=21,
            saved_model_dir="../deep_disfluency/experiments/021/epoch_40"
            )


    def run(self):

        # In[3]:

        # Tag each word incrementally
        # Notice the incremental diff
        # Set diff_only to False if you want the whole utterance's tag each time
        with_pos = False
        text=""
        total_words=0
        print "tagging..."
        if with_pos:
            # if POS is provided use this:
            print self.disf.tag_new_word("john", pos="NNP")
            print self.disf.tag_new_word("likes", pos="VBP")
            print self.disf.tag_new_word("uh", pos="UH")
            print self.disf.tag_new_word("loves", pos="VBP")
            print self.disf.tag_new_word("mary", pos="NNP")
        else:
            # else the internal POS tagger tags the words incrementally

            # opening the text file
            with open('output.txt','r') as file:
                # reading each line
                for line in file:
                    # reading each word
                    for word in line.split():
                        # displaying the words
                        total_words+=1
                        if word=="%HESITATION" or word=="%HESITATION." :
                            text+="uh"+" "
                            print self.disf.tag_new_word("uh")
                        else:
                            text+=word+" "
                            print self.disf.tag_new_word(word)

            # print disf.tag_new_word("john")
            # print disf.tag_new_word("likes")
            # print disf.tag_new_word("uh")
            # print disf.tag_new_word("loves")
            # print disf.tag_new_word("mary")

        # map = {}
        # edit_Terms = {}
        # words = []
        # wordIndex=0
        # rmStart = {} # id and position
        # rpEnd = {} # id and position###the id in the tag is where the repair ends!!!!!!
        # rpStart = {}
        # # sentenceStart = {} # id and position ################################TO DO ~~~~~~~~~~~~~~
        # sentenceIndex = 0 # start of the sentence
        # repairSentence = {} # id and position of start os sentence

        print "final tags:"
        for w, t in zip(text.split(), self.disf.output_tags):

            if t not in self.map:
                self.map[t] = 1
            else:
                self.map[t]+=1

            if t.find('<e/>')!=-1: # to see what all edit terms we have and how many times each was repeated
                if w not in self.edit_Terms:
                    self.edit_Terms[w]=1
                else:
                    self.edit_Terms[w]+=1

            tags = t.split(">")
            tags.pop() # as the last one is always blank
            number_of_tags = len(t.split(">"))

            # if number_of_tags<=1: # Works only if each word has less than one tag ############
            ###### do like a while or do while loop and see if there are more than one tagged index associated with the word.
            ## Tags should always follow the structure rms rps rpn/sub/rep/del
            for tag in tags:
                positionOfIndexNumStart = tag.find("\"")
                positionOfIndexNumEnd = tag.find("\"", positionOfIndexNumStart+1)
                indexNum = tag[positionOfIndexNumStart+1: positionOfIndexNumEnd]
                if tag.find("rms")!=-1:
                    self.rmStart[indexNum] = self.wordIndex
                    self.repairSentence[indexNum] = self.sentenceIndex
                if tag.find("rps")!=-1:
                    self.rpStart[indexNum] = self.wordIndex
                if tag.find("rpn")!=-1:
                    self.rpEnd[indexNum] = self.wordIndex
                if tag.find("rpnsub")!=-1:
                    self.rpnsub[indexNum] = self.wordIndex
                if tag.find("rpnrep")!=-1:
                    self.rpnrep[indexNum] = self.wordIndex
                if tag.find("rpndel")!=-1:
                    self.rpndel[indexNum] = self.wordIndex
            self.words.append(w)
            self.wordIndex+=1
            if w.find(".")!=-1:#### ? !
                self.sentenceIndex = self.wordIndex
            print w, "\t", t
        self.disf.reset()  # resets the whole tagger for new utterance


        toStore = [self.words, self.rmStart, self.rpStart, self.rpnsub, self.rpnrep, self.rpndel, self.repairSentence, self.map, self.edit_Terms]
        ################ Store data ####### serialization
        import pickle
        f=open("pickled.txt","wb")
        pickle.dump(toStore,f)
        f.close()
