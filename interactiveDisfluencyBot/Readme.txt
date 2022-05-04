This is my submission for Final Year Project 2021/22.

HOW TO RUN MY CODE
1.	Make an anaconda virtual environment with python 2.0
2.	Git clone deep disfluency and install all its requirements (as much as possible, don’t follow the installation for ASR, as it doesn’t work)
3.	Replace the demo folder with interactiveDisfluencyBot (submission for supporting material)
4.	Cd into deep disfluency/ interactiveDisfluencyBot
5.	Then run: python server.py
6.	The server is now running
7.	Now, on a new anaconda terminal, create a virtual environment with python 3
8.	Cd into deep disfluency/ interactiveDisfluencyBot
9.	And try to run python main.py
You will need to install dependencies like IBM Watson and sounddevice and others. If you see the error like dependency not found, just install it using conda.
You will also need to check what device you are using, because I used windows and am using windows sub system to run a couple sub tasks like opening notepad.
Also make sure to check the channels number in main.py for sound recording, depending on your device it changes.

GitHub repo:  https://github.com/saakshisaxena/FluencyDetectorLocal
