from feedback import feedback
from speech import speech

speech = speech()

feedback = feedback()
feedback.getAndSaveFeedbackWithScore()

print("Do you want to read all feedback at once? Say yes or no")
readAll = speech.listen("Do you want to read all feedback at once? Say yes or no").lower()
correctAnswer=False
while(not correctAnswer):
    if readAll=="yes":
        feedback.readAll()
        correctAnswer=True

    elif readAll=="no":
        print("Okay here is a short summary with types of repairs found:")
        speech.speak("Okay, here is a short summary with types of repairs found:")
        feedback.shortSummary()
        correctAnswer=True
        feedback.detailedReport()

    else:
        print("yes or no")
        readAll = speech.listen("Say yes or no").lower()
