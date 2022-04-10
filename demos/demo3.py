# coding: utf-8

# In[1]:
class demo3:
    def __init__(self):
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

        map = {}
        edit_Terms = {}
        words = []
        wordIndex=0
        rmStart = {} # id and position
        rpEnd = {} # id and position
        sentenceStart = {} # id and position ################################TO DO ~~~~~~~~~~~~~~
        sentenceIndex = 0 # start of the sentence
        repairSentence = {} # id and position of start os sentence
        print "final tags:"
        for w, t in zip(text.split(), self.disf.output_tags):
            if t not in map:
                map[t] = 1
            else:
                map[t]+=1
            if t.find('<e/>')!=-1: # to see what all edit terms we have and how many times each was repeated
                if w not in edit_Terms:
                    edit_Terms[w]=1
                else:
                    edit_Terms[w]+=1
            number_of_tags = len(t.split("> "))
            if number_of_tags<=1: # Works only if each word has less than one tag ############
            ###### do like a while or do while loop and see if there are more than one tagged index associated with the word.
                positionOfIndexNumStart = t.find("\"")
                positionOfIndexNumEnd = t.find("\"", positionOfIndexNumStart+1)
                indexNum = t[positionOfIndexNumStart+1: positionOfIndexNumEnd]
                if t.find("rms")!=-1:
                    rmStart[indexNum] = wordIndex
                    repairSentence[indexNum] = sentenceIndex
                if t.find("rpn")!=-1:
                    rpEnd[indexNum] = wordIndex
            words.append(w)
            wordIndex+=1
            if w.find(".")!=-1:
                sentenceIndex = wordIndex
            print w, "\t", t
        self.disf.reset()  # resets the whole tagger for new utterance

        print(map)
        print(rmStart)
        print(rpEnd)
        print(words)
        print(repairSentence)
        toSave=""
        print("Reading the repairs:.......")
        toSave+="Short Summary: \n "+ str(edit_Terms) +"\n"
        toSave+="Details of Repair in sentences: \n"
        for key in rmStart.keys():
            repair = ""
            repairSent = ""
            ######## if asked for the mistake and the correction
            for i in range(rmStart[key], rpEnd[key]+1):
                repair+=words[i]+" "
            ####### If asked for the sentence in which the repair was done ######
            for k in range(repairSentence[key], len(words)):
                repairSent+=words[k]+" "
                if words[k].find('.')!=-1:
                    break
            toSave+=str(key)+". Mistake+Correction: "+repair+" \t In the sentence: "+repairSent+"\n"
            print(repair)
            print(repairSent)
            print("-------------------------")
            print("Edit terms and their count:")
            print(edit_Terms)
        ### Save feedback in a text file ######
        with open('feedback.txt', 'w') as out:
            out.writelines(toSave)
             # out.writelines(str(map))
        if '<f/>' in map.keys():
            naive_fluency_score = int(map['<f/>'])*100/total_words
        else:
            naive_fluency_score = 0
        print("Naive fluency score: ", naive_fluency_score)
