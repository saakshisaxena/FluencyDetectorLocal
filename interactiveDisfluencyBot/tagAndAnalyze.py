# coding: utf-8
class disfluencyTagger:
    def __init__(self):
        pass
    def run(self):
        pass
    def getEditTerms(self):
        pass


class tagAndAnalyze(disfluencyTagger):
    def __init__(self):
        self.map = {}
        self.edit_Terms = {}
        self.words = []
        self.wordIndex=0
        self.rmStart = {} # id and position
        self.rpEnd = {} # id and position###the id in the tag is where the repair ends!!!!!! #### General cases not mentioned in research work!
        self.rpStart = {}
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
        # Tag each word incrementally
        # Notice the incremental diff
        # Set diff_only to False if you want the whole utterance's tag each time
        with_pos = False
        text=""
        total_words=0
        print "tagging..."
        # opening the text file
        with open('output.txt','r') as file:
            # reading each line
            for line in file:
                # reading each word
                for word in line.split():
                    # tag and save each word
                    total_words+=1
                    # if there is a hesitation found change it to uh ###can be caused by STT API settings variation
                    if word=="%HESITATION" or word=="%HESITATION." :
                        text+="uh"+" "
                        print self.disf.tag_new_word("uh")
                    else:
                        text+=word+" "
                        print self.disf.tag_new_word(word)

        print "final tags:"
        for w, t in zip(text.split(), self.disf.output_tags): # go through all words and their tags

            if t not in self.map: # keep the tag and its count in map variable
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

            # Fill out the id and position variables here while looping through tags.
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
            if w.find(".")!=-1:# If you find a full stop then the index of start of new sentence will be
                self.sentenceIndex = self.wordIndex
            print w, "\t", t
        self.disf.reset()  # resets the whole tagger for new utterance

        ################ Store data ####### serialization
        toStore = [self.words, self.rmStart, self.rpStart, self.rpnsub, self.rpnrep, self.rpndel, self.repairSentence, self.map, self.edit_Terms]
        import pickle
        f=open("pickled.txt","wb")
        pickle.dump(toStore,f)
        f.close()
