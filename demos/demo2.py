# coding: utf-8

# In[1]:
class demo2:
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
        print "final tags:"
        for w, t in zip(text.split(), self.disf.output_tags):
            if t not in map:
                map[t] = 1
            else:
                map[t]+=1
            print w, "\t", t
        self.disf.reset()  # resets the whole tagger for new utterance

        print(map)
        with open('map.txt', 'w') as out:
             out.writelines(str(map))
        if '<f/>' in map.keys():
            naive_fluency_score = int(map['<f/>'])*100/total_words
        else:
            naive_fluency_score = 0
        print("Naive fluency score: ", naive_fluency_score)
