#!/usr/bin/env python
import numpy
from numpy import zeros, float32
import sys, hmmtrain
import re
import math
import itertools as iter
class hmm:        
    def __init__(self):
        priors, transitions, emissions, states, symbols = hmmtrain.train()
        self.priors = priors
        self.transitions = transitions
        self.emissions = emissions
        self.states = states
        self.symbols = symbols

    def tagViterbi(self):
#Ask the file path
	filepath=raw_input("Enter file path")
#opens the file in read mode	
	input=open(filepath,'r')
#input line by line
	for line in input:
#call to decode by passing every line(String)
		self.decode(line.lower())

    def decode(self,askString):
#Initializing flag variable				
	flag=""	
#If the input enetred by the user is empty
	if(askString==""):
		flag='true'	
		askString=raw_input("Enter a string ")
	else:
#If the input string is not empty
		flag='false'
#Regular expression for finding valid words
	matches=re.findall("[A-Za-z0-9]+\-?[A-Za-z0-9]+|i|a|\.|\:|\,|\(|\)|\#|\$|''|``",askString)
#Creating a 2D floating point viterbi array x*y with number of states as x and number of input words as y 
	viterbi=zeros(shape=(len(self.states),len(matches)),dtype=float32)
#Creating Backpointer 2D integer array x*y with number of states as x and number of input words as y 
	backPointer=zeros(shape=(len(self.states),len(matches)),dtype=int)
#Setting the y value as 0 initially	
	obsCount=0
	for tags in range(0,len(self.states)):
#Setting the initial probabilities in viterbi array for first column of every state 
		viterbi[tags][obsCount]=(self.priors.prob(self.states[tags]))*(self.emissions[self.states[tags]].prob(matches[0]))
#Setting the frst column of every state to backpointer 0 
		backPointer[tags][obsCount]=0
#Initializing max variable to 0		
	max=0
	for observations in range(1,len(matches)):
		for stateSequence in range(0,len(self.states)):
			max=0
#Finding the maximum transition
			for innerStateSequence in range(0,len(self.states)):
				if((viterbi[innerStateSequence][observations-1]*self.transitions[self.states[innerStateSequence]].prob(self.states[stateSequence]))>max):					
					max=viterbi[innerStateSequence][observations-1]*self.transitions[self.states[innerStateSequence]].prob(self.states[stateSequence])
#Retaining the backpointer from where the maximum transtion took place.
					backTrackSequence=innerStateSequence
#Assigning each state/word combination the product of max with the emission probability						
			viterbi[stateSequence][observations]=max*(self.emissions[self.states[stateSequence]].prob(matches[observations]))
#Assigning the backpointer max sequence to every state/word combination 
			backPointer[stateSequence][observations]=backTrackSequence
	sequence=0
	max=0
#Backtracking, by first finding the max viterbi value state in last column		
	for stateSequence in range(0,len(self.states)-1):
			if(viterbi[stateSequence][len(matches)-1]>max):
				max=viterbi[stateSequence][len(matches)-1]
				sequence=stateSequence	
	#Creating an List for reversing the POS tags
#FinalTags for holding the final tags
	finalTags=[]
#Using last sequence as a refrence backtracking to the initial state for finding one state from each column
	for observations in range(len(matches)-1,-1,-1):
		finalTags.append(self.states[sequence])
		sequence=backPointer[sequence][observations]
	count=0	
	str=""
#Printing the corresponding tags from finalTags list
	if(flag=='true'):
		for tags in range(len(matches)-1,-1,-1):	
			str=str+finalTags[tags]+" "
		print str
	else:
		for tags in range(len(matches)-1,-1,-1):	
			str=str+matches[count]+"/"+finalTags[tags]+" "
			count=count+1
		print str	
    ####
    # ADD METHODS HERE
    ####
		
    def exhaustive(self):
#Input string from the user
	inputSentence=raw_input("Enter a string").lower()
#Regular expresion to extract words
	matches=re.findall("[A-Za-z0-9]+\-?[A-Za-z0-9]+|a|i|\.|\:|\,|\(|\)|\#|\$|''|``",inputSentence)
#Initializing max to resrver maximum probability
	max=0
#Initializing tagSeq for retaining the final tag sequence			
	tagSeq=[]
#Initializing custom tags to take the selctive tags.
	myCustomTags=[]
	myCustomTags.append(self.states[2])
	myCustomTags.append(self.states[7])
	myCustomTags.append(self.states[9])
	myCustomTags.append(self.states[11])
	myCustomTags.append(self.states[12])
	myCustomTags.append(self.states[14])
	myCustomTags.append(self.states[16])
	myCustomTags.append(self.states[17])
	myCustomTags.append(self.states[19])
	myCustomTags.append(self.states[21])
	myCustomTags.append(self.states[22])
	myCustomTags.append(self.states[25])
	myCustomTags.append(self.states[26])
	myCustomTags.append(self.states[27])
	myCustomTags.append(self.states[29])
	myCustomTags.append(self.states[37])
	myCustomTags.append(self.states[44])
	myCustomTags.append(self.states[45])
#Using itertools to genrate various permutations of the given tags of length equal to the input entered 
	for tagSequence in iter.product(myCustomTags,repeat=len(matches)):
#setting flag variable to true for valid tag sequence having probability >1e-4
		flag="true"
#Initializing prob vairbale used to calculate the product of emission*transition probabilities
		prob=0
#Iterating through the  tag sequence
		for iterations in range(0,len(tagSequence)):
#Checking if the emission probabilites of the corresponding word/tag is < 1e-4
			if(self.emissions[tagSequence[iterations]].prob(matches[iterations])<1e-4):
#Setting the flag to false for such tag/word
				flag="false"
				break
			if(flag=="true"):
#calculating the P(startProb)*P(emissionProb) for the start symbol/tag
				prob=self.priors.prob(tagSequence[0])*self.emissions[tagSequence[0]].prob(matches[0])		
#Iterating through the valid tag sequences
				for iteration in range(1,len(tagSequence)):
#Calculating sum of probabilities of all the sequences
					prob=prob*self.transitions[tagSequence[iteration-1]].prob(tagSequence[iteration])*self.emissions[tagSequence[iteration]].prob(matches[iteration])
#Finding max probability
				if(prob>max):
					max=prob
					tagSeq=tagSequence
#Printing the final tag sequence		
	print "Tag Sequence ",tagSeq
	print "Probability of the above tag sequence ",max	

def main():
    # Create an instance
     model = hmm()
     choice=raw_input("Enter 1 to decode, 2 to perform exhaustive search or 3 to call tagViterbi")
     if(choice=="1"):		
	model.decode("")
     if(choice=="2"):
	model.exhaustive()
     if(choice=="3"):
	model.tagViterbi()			 	
if __name__ == '__main__':
    main()
def exhaustive():
    print "Hi"
