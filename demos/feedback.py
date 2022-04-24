import pickle
from speech import speech


class feedback:

    def __init__(self):
        ########## Load data #### data de-serialization
        f=open("pickled.txt","rb")
        data=pickle.load(f)
        print (data)
        f.close()

        self.words = data[0]
        self.rmStart = data[1]
        self.rpStart = data[2]
        self.rpnsub = data[3]
        self.rpnrep = data[4]
        self.rpndel = data[5]
        self.repairSentence = data[6]
        self.map = data[7]
        self.edit_Terms = data[8]

        self.speech = speech()

    def getAndSaveFeedbackWithScore(self):
        toSave=""
        if self.edit_Terms=={}:
            toSave+="No edit terms used \n"
        else:
            toSave+="Edit terms used: \n "+ str(self.edit_Terms) +"\n"

        if self.rmStart!={}: # only if you have disfluencies of repair type

            print("Reading the repairs:.......")

            toSave+="\n"+"Types of repairs detected: \n"
            id = 1
            if self.rpndel!={}:
                toSave+="\n"+"Deletion repairs: \n"
                for key in self.rpndel.keys():
                    mistake = self.getReparandum(key)
                    repair = self.getDeletion(key)
                    repairSent = self.getSentence(key)
                    toSave+=str(id)+". \nMistake: "+mistake+"\t \nIn the sentence: "+repairSent+"\n"
                    id +=1

            id = 1
            if self.rpnsub!={}:
                toSave+="\n"+"Substitution repairs: \n"
                for key in self.rpnsub.keys():
                    mistake = self.getReparandum(key)
                    repair = self.getSubstitution(key)
                    repairSent = self.getSentence(key)
                    toSave+=str(id)+". \nMistake: "+mistake+"\t \nCorrection: "+repair+"\t \nIn the sentence: "+repairSent+"\n"
                    id +=1

            id = 1
            if self.rpnrep!={}:
                toSave+="\n"+"Repetition repairs: \n"
                for key in self.rpnrep.keys():
                    mistake = self.getReparandum(key)
                    repair = self.getRepitition(key)
                    repairSent = self.getSentence(key)
                    toSave+=str(id)+". \nWord: "+mistake+"\t \nRepitition: "+repair+"\t \nIn the sentence: "+repairSent+"\n"
                    id +=1

                # if self.rpEnd=={}:
                #     for i in range(self.rpStart[key], len(self.words)):
                #         repair+=self.words[i]+" "
                # else:
                #     for i in range(self.rpStart[key], self.rpEnd[key]+1):
                #         repair+=self.words[i]+" "
                ####### If asked for the sentence in which the repair was done ######


            ###############################################################
            ###### Naive FLUENCY SCORE
            if '<f/>' in self.map.keys(): # set a weighted values for fluency score
                naive_fluency_score = int(int(self.map['<f/>'])*100/len(self.words) *100)/100.0
            else:
                naive_fluency_score = 0
            print("Naive fluency score: ", naive_fluency_score)

            ####Dislfuency SCORE
            ########
            totalDifluencyCount=0
            for k in self.edit_Terms.keys():
                totalDifluencyCount+=self.edit_Terms[k]
            totalDifluencyCount+=len(self.rmStart) # how many mistakes and Correction

            disfluencyScore=int((totalDifluencyCount*100)/len(self.words))
            print("Dislfuency Score: "+str(disfluencyScore))

            toSave+="\n"+"Naive Fluency Score: "+str(naive_fluency_score)+"\n"
            toSave+="\n"+"Disfluency Score: "+str(disfluencyScore)+"\n"

            ########################################
            ##### Write to tracking files
            ## use "a" to append the file
            with open("disfluencyScoreTracker.txt", "a") as disfluencyScoreTrackerFile:
                disfluencyScoreTrackerFile.write(str(disfluencyScore)+"\n")
            #######################################
            ### Save feedback in a text file ######
            with open('feedback.txt', 'w') as out:
                out.writelines(toSave)
                 # out.writelines(str(map))

    def getReparandum(self, key):
        mistake = ""
        for i in range(self.rmStart[key], self.rpStart[key]):
            mistake+=self.words[i]+" "
        return mistake


    def getRepitition(self, key):
        repair = ""
        for i in range(self.rpStart[key], self.rpnrep[key]+1):
            repair+=self.words[i]+" "
        return repair


    def getSubstitution(self, key):
        repair = ""
        for i in range(self.rpStart[key], self.rpnsub[key]+1):
            repair+=self.words[i]+" "
        return repair

    def getDeletion(self, key):
        repair = ""
        for i in range(self.rpStart[key], self.rpndel[key]+1):
            repair+="This is a deletion repair statement."
        return repair

    def getSentence(self, key):
        sent = ""
        for k in range(self.repairSentence[key], len(self.words)):
            sent+=self.words[k]+" "
            if self.words[k].find('.')!=-1:
                break
        return sent

    def readAll(self):
        with open('feedback.txt') as fp:
            for line in fp:
                self.speech.speak(line)

    def shortSummary(self):
        self.speech.speak("Edit terms used: \n "+ str(self.edit_Terms) +"\n")
        # Types of repairs found
        if self.rpnsub=={} and self.rpnrep=={} and self.rpndel=={}:
            self.speech.speak("No repair disfluency types are present in your speech.")
        else:
            self.speech.speak("Types of repair/s found are:")
            if self.rpnsub!={}:
                self.speech.speak("Substitution Repair")
            if self.rpnrep!={}:
                self.speech.speak("Repitition repair")
            if self.rpndel!={}:
                self.speech.speak("Deletion repair")

    def detailedReport(self):
        if self.rpnsub=={} and self.rpnrep=={} and self.rpndel=={}:
            self.speech.speak("No detailed report to be discussed.")
            return

        self.speech.speak("What type of disfluency would you like to hear the detailed report for")
        # if self.rpnsub!={}:
        #     self.speech.speak("Substitution Repair")
        # if self.rpnrep!={}:
        #     self.speech.speak("Repitition repair")
        # if self.rpndel!={}:
        #     self.speech.speak("Deletion repair")

        readWhat = self.speech.listen("Say the name, example: Substitution. Or say exit to exit feedback report discussion.").lower()

        correctAnswer=False
        exit=False

        while((not correctAnswer) and (not exit)):
            if readWhat=="substitution":
                self.readSub()
                correctAnswer=True

            elif readWhat=="repetition":
                self.readRep()
                correctAnswer=True

            elif readWhat=="deletion":
                self.readDel()
                correctAnswer=True

            elif readWhat=="exit" or readWhat=="bye" or readWhat=="quit":
                exit = True
                correctAnswer=True

            else:
                print("yes or no")
                readWhat = self.speech.listen("Say the name, example: Substitution. Or say exit to exit feedback report discussion.").lower()

            if exit==False and correctAnswer==True:
                correctAnswer = False
                readWhat = self.speech.listen("What would you like to discuss next, say the name of the repair type, example: Deletion or say exit or bye to quit feedback report discussion.").lower()


    def readSub(self):
        id = 1
        if self.rpnsub!={}:
            self.speech.speak("Substitution repairs: ")
            for key in self.rpnsub.keys():
                mistake = self.getReparandum(key)
                repair = self.getSubstitution(key)
                repairSent = self.getSentence(key)
                self.speech.speak(str(id)+". \nMistake: "+mistake+"\t \nCorrection: "+repair+"\t \nIn the sentence: "+repairSent+"\n")
                id +=1
        else:
            self.speech.speak("No Substitution repairs found.")

    def readRep(self):
        id = 1
        if self.rpnrep!={}:
            self.speech.speak("Repitition repairs: ")
            for key in self.rpnrep.keys():
                mistake = self.getReparandum(key)
                repair = self.getRepitition(key)
                repairSent = self.getSentence(key)
                self.speech.speak(str(id)+". \nWord: "+mistake+"\t \nRepitition: "+repair+"\t \nIn the sentence: "+repairSent+"\n")
                id +=1
        else:
            self.speech.speak("No Repitition repairs found.")

        def readDel(self):
            id = 1
            if self.rpndel!={}:
                self.speech.speak("Deletion repairs: ")
                for key in self.rpndel.keys():
                    mistake = self.getReparandum(key)
                    repair = self.getDeletion(key)
                    repairSent = self.getSentence(key)
                    self.speech.speak(str(id)+". \nMistake: "+mistake+"\t \nIn the sentence: "+repairSent+"\n")
                    id +=1
            else:
                self.speech.speak("No Deletion repairs found.")
