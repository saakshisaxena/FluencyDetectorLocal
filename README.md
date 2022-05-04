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



# Deep Learning Driven Incremental Disfluency Detection

Code for Deep Learning driven incremental disfluency detection and related dialogue processing tasks.

## Functionality ##

The deep disfluency tagger consumes words (and optionally, POS tags and word timings) word-by-word and outputs xml-style tags for each disfluent word, symbolising each part of any repair or edit term detected. The tags are:

`<e/>` - an edit term word, not necessarily inside a repair structure

`<rms id=“N”/>` - reparandum start word for repair with ID number N

`<rm id=“N”/>` - mid-reparandum word for repair N

`<i id=“N”/>` - interregnum word for repair N

`<rps id=“N”/>` - repair onset word for repair N (where N is normally the 0-indexed position in the sequence)

`<rp id=“N”/>` - mid-repair word for repair N

`<rpn id=“N”/>` - repair end word for substitution or repetition repair N

`<rpndel id=“N”/>` - repair end word for a delete repair N

Every repair detected or in the gold standard will have at least the `rms`, `rps` and `rpn`/`rpndel` tags, but the others may not be present.

Some example output on Switchboard utterances is as below, where `<f/>` is the default tag for a fluent word:

```
	4617:A:15:h		1	uh          	UH	    <e/>
    				2	i	        PRP	    <f/>
    				3	dont	    	VBPRB	    <f/>
    				4	know	    	VB	    <f/>
    				
	4617:A:16:sd		1	the         	DT          <rms id="1"/>
    				2	the	        DT	    <rps id="1"/><rpn id="1"/>
    				3	things	    	NNS	    <f/>
    				4	they	    	PRP	    <f/>
    				5	asked	    	VBD         <f/>
    				6	to	        TO	    <f/>
    				7	talk	    	VB	    <f/>
    				8	about	    	IN          <f/>
    				9	were	    	VBD	    <f/>
    				10	whether	    	IN	    <rms id="12"/>
    				11	the	        DT	    <rm id="12"/>
    				12	uh	        UH	    <i id="12"/><e/>
    				13	whether	    	IN	    <rps id="12"/>
    				14	the	        DT	    <rpn id="12"/>
    				15	judge	    	NN	    <f/>
    				16	should	    	MD	    <f/>
    				17	be	        VB	    <f/>
    				18	the	        DT	    <f/>
    				19	one	        NN	    <f/>
    				20	that	    	WDT	    <f/>
    				21	does	    	VBZ	    <f/>
    				22	the	        DT	    <f/>
    				23	uh	        UH	    <e/>
				24	sentencing	NN	    <f/>
```

## Setup and basic use ##

To run the code here you need to have `Python 2.7` installed, and also [`pip`](https://pip.readthedocs.org/en/1.1/installing.html).

### Install option 1: using pip install ###

If you want to simply install the current PyPi library version, simply run the following(depending on your user status, you may need to prefix the below with `sudo` or use a virtual environment):

`pip install deep_disfluency`

### Install option 2: using setuptools ###

If you want to manually install using `setuptools` (depending on your user status, you may need to prefix the below with `sudo` or use a virtual environment):

`pip install setuptools`

Then need to run the below from the command line from inside this folder (again, depending on your user status, you may need to prefix the below with `sudo` or use a virtual environment):

`python setup.py install`

### Install option 3: (for development) getting requirements only ###

If you want to develop but do not want to install deep_disfluency as a package, then simply run the below from inside this folder to install the current requirements (again, depending on your user status, you may need to prefix the below with `sudo` or use a virtual environment):

`pip install -r requirements.txt`

If you use this option, in any code you use make sure this folder is on your python path.

### Demo ###

After you have completed any of the above three options you should now have installed deep_disfluency into the python distribution, or be able to path to this folder with the requirements installed. If you just want to use the tagger off-the-shelf see the usage in `demos/demo.py` or the notebook `demos/demo.ipynb`.


### Use with live ASR ###

If you would like to run a live ASR version using the IBM Watson speech-to-text recognizer, you need to also do the following: 

1. First install [PortAudio](http://www.portaudio.com/) - a free, cross-platform, open-source, audio I/O library.
2. Prepare your credentials from IBM Watson (free trials are available):
   * Visit the [IBM Watson projects](https://console.bluemix.net/developer/watson/projects) page.
   * Choose your project.
   * Copy the credentials to `credentials.json` into this directory.

The ASR live streaming demo at `demos/asr.py` can then be run with the location of the credentials file as its argument. I.e. from the `demos` directory you would run:

`python asr.py ../credentials.json`

After it sets up, you should start to see the recognized words, timings, POS tags, and disfluency tags appearing on the screen in real time as you speak into your microphone.


## Running experiments ##

The code can be used to run the experiments on Recurrent Neural Networks (RNNs) and LSTMs from:

```
Julian Hough and David Schlangen. Joint, Incremental Disfluency Detection and Utterance Segmentation from Speech. Proceedings of EACL 2017. Valencia, Spain, April 2017.
```

Please cite [the paper](http://aclweb.org/anthology/E17-1031) if you use this code.

If you are using our pretrained models as in the usage in `demo/demo.py` you can simply first install the experimental requirements for the experiments by running:

`pip install -r requirements.txt`

Then run `python deep_disfluency/experiments/EACL_2017.py`- but first ensuring the boolean variables at the top of the file to:

```python
download_raw_data = False
create_disf_corpus = False
extract_features = False
train_models = False
test_models = True
```

If that level of reproducibility does not satisfy you, you can set all those boolean values to `True` (NB: be wary that training the models for each experiment in the script can take 24hrs+ even with a decent GPU).

Once the script has been run, running the Ipython notebook at `deep_disfluency/experiments/analysis/EACL_2017/EACL_2017.ipynb` should process the outputs and give similar results to those recorded in the paper.

### Extra: using the Switchboard audio data ###

If you are satisfied just using lexical/POS/Dialogue Acts and word timing data alone, the above are sufficient, however if you want to use other acoustic data or generate ASR results from scratch, you must have access to the Switchboard corpus audio release. This is available for purchase from:

[[https://catalog.ldc.upenn.edu/ldc97s62]]

From the switchboard audio release, copy or move the folder which contains the .sph files (called `swbd1`) to within the `deep_disfluency/data/raw_data/` folder. Note this is very large at around 14GB.

## Future: Creating your own data ##

Training data is created through creating dialogue matrices (one per speaker in each dialogue), whereby the format of these for each row in the matrix is as follows, where `,` indicates a new column, and `...` means there are potentially multiple columns:

`word index, pos index, word duration, acoustic features..., lm features..., label`

There are methods for creating these in the `deep_disfluency/corpus` and `deep_disfluency/feature_extraction` modules.

## Resource Acknowledgments ##

This basis of these models is the disfluency and dialogue act annotated Switchboard corpus, based on that provided by Christopher Potts's 2011 Computational Pragmatics course ([[at http://compprag.christopherpotts.net/swda.html]]) or at [[https://github.com/cgpotts/swda]]. Here we use Julian Hough's fork which corrects some of the POS-tags and disfluency annotation:

[[https://github.com/julianhough/swda.git]]

The second basis is the word timings data for switchboard, which is a corrected version with word timing information to the Penn Treebank version of the MS alignments, which can be downloaded at:

[[http://www.isip.piconepress.com/projects/switchboard/releases/ptree_word_alignments.tar.gz]]













