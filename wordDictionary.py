from . import databaseManager
class dictionaryManager:
    def __init__(self,Type):
        self.wordCollection = []
        self.wordDictionary = {}
        self.Type = Type
    
    def dictionaryGenerator(self):

        """this function generates the dictionary from which the auto complete algorithm will
           provide suggestions to the user"""

        dbManagerObject = databaseManager.databaseManager("december2019","31/12/19",self.Type)
        dbManagerObject.createConnection()
        dataList = dbManagerObject.executeQuery("SELECT")
        #collection variable will contain the words with same rank and use_count
        collection = []
        i = 0
        breakFlag = 0
        while(i<=len(dataList)-1):
            collection.append(list(dataList[i]))
            for j in range(i+1,len(dataList)):
                if(dataList[j][0]==dataList[i][0]):
                    collection.append(list(dataList[j]))
                else:
                    i = j
                    breakFlag = 1
                    break
            self.wordCollection.append(collection)
            collection = []
            if(breakFlag==0):
                break
            else:
                breakFlag = 0
        for i in range(len(self.wordCollection)):
            self.wordDictionary[i] = self.wordCollection[i]
        return self.wordDictionary

    def addNewWord(self,word,useCount):

        #this function is used to add a new word to the dictionary
        #wordData variable is containing the new word with its use count and its rank will updated later
        wordData = [useCount,word]
        #useCountDifference contains the difference b/w the use_count of new word and the use_count of the first word of the last collection
        useCountDifference = useCount-self.wordCollection[len(self.wordCollection)-1][0][1]
        if(useCountDifference==0):
            """when this code block is executed then the new word is inserted into the last collection of the dictionary"""
            wordData.insert(0,self.wordCollection[len(self.wordCollection)-1][0][0])
            self.wordCollection[len(self.wordCollection)-1].append(wordData)
        elif(useCountDifference<0):
            #when this code block is executed then the new word is appended to the dictionary with its own collection
            wordData.insert(0,self.wordCollection[len(self.wordCollection)-1][0][0]+1)
            self.wordCollection.append([wordData])
        else:
            """when this code block is executed then the new word is added in one of the existing collections
               or is added to the dictionary with rank 1 with its new collection"""
            correctIndex = self.findCorrectIndex(0,len(self.wordCollection)-1,useCount)
            if(correctIndex[1]==0):
                wordData.insert(0,1)
                self.wordCollection.insert(correctIndex[0],[wordData])
                for i in range(1,len(self.wordCollection)):
                    for j in range(len(self.wordCollection[i])):
                        self.wordCollection[i][j][0] += 1
            elif(correctIndex[1]==1):
                wordData.insert(0,self.wordCollection[correctIndex[0]][0][0])
                self.wordCollection[correctIndex[0]].append(wordData)
            #this return statement below is executed whenever the new word is added to one of the existing collections except in the last collection or creates its new collection with rank 1
            return correctIndex[0],wordData,correctIndex[1]
        #this return statement below is executed when the new word is added to the last collection or if the new word has the lowest rank and creates its own collection with the lowest rank
        return len(self.wordCollection)-1,wordData
    
    def updateUseCount(self,position,useCount):
        
        #this function is used to update the use_count of the existing word and update its collection according to its rank
        #updatedUseCount variable contains the new use_count of the word to be updated
        #position parameter is the x,y where x is the old collection position and y is the old index of the word updated in that x collection
        #useCount is the total no. of times the word is used in the recent input

        updatedUseCount = self.wordCollection[position[0]][position[1]][1]+useCount
        correctIndex = self.findCorrectIndex(0,position[0],updatedUseCount)
        self.wordCollection[position[0]][position[1]][1] = updatedUseCount
        wordData = None
        if(correctIndex[1]==0):
            
            """when this code block is executed then the existing updated word is updated with the
               rank of 1 and added to the start of the collection and to the dictionary"""
            #wordData contains the new collection along with the word in the collection which is updated
            """correctIndex contains 3 values : at index 0 it has the index for the new collection that this
                word will create, at index 1 it contains the value of breakFlag and at index 2 it has the 
                new rank of the word."""
            wordData = [self.wordCollection[position[0]][position[1]]]
            del(self.wordCollection[position[0]][position[1]])
            print("collection after deletion : ",self.wordCollection)
            print("\n")
            wordData[0][0] = correctIndex[0]+1
            self.wordCollection.insert(correctIndex[0],wordData)
            for i in range(correctIndex[0]+1,len(self.wordCollection)):
                for j in range(len(self.wordCollection[i])):
                    self.wordCollection[i][j][0] += 1
        elif(correctIndex[1]==1):
            
            """when this code block is executed then the updated word is added to a new collection
               from the existing group of collections according to its new rank and use_count and if the
               updated word's old collection gets empty it is deleted and the collections following it are
               promoted 1 rank up to avoid the void in the dictionary."""
            
            wordData = self.wordCollection[position[0]][position[1]]
            del(self.wordCollection[position[0]][position[1]])
            if(len(self.wordCollection[position[0]])==0):
                print("True")
                del(self.wordCollection[position[0]])
                for i in range(position[0],len(self.wordCollection)):
                    for collection in self.wordCollection[i]:
                        collection[0] -= 1
                        print(collection)
            wordData[0] = self.wordCollection[correctIndex[0]][0][0]
            self.wordCollection[correctIndex[0]].append(wordData)
            print("word collection after updating the existing word : ",self.wordCollection)
        return correctIndex[0],wordData,position[0],position[1],correctIndex[1]
        
        #correctIndex[0] contains the new index of the word in the new collection
        #wordData contains the rank,usecount and the word itself
        #position[0] contains the old collection position of the updated word
        #position[1] contains the old index of the word in its old collection
        #correctIndex[1] contains the breakFlag which indicates whether the updated word is promoted to one of the existing collection or it has the highest useCount and has created the new collection with rank 1
    
    def findCorrectIndex(self,startingIndex,lastIndex,useCount):
        correctIndex = 0
        breakFlag = 0
        midIndex = 0
        while(startingIndex<=lastIndex):
            midIndex = (startingIndex+lastIndex)//2
            print("wordCollection : ",self.wordCollection)
            print("\n")
            if(useCount==self.wordCollection[midIndex][0][1]):
                correctIndex = midIndex
                breakFlag = 1
                break
            elif(useCount>self.wordCollection[midIndex][0][1]):
                lastIndex = midIndex-1
            elif(useCount<self.wordCollection[midIndex][0][1]):
                startingIndex = midIndex+1
        if(breakFlag==0):
            #return statement snippet : return (key,breakFlag,rank)
            if(useCount>self.wordCollection[0][0][1]):
                return (0,breakFlag)
            elif(useCount>self.wordCollection[midIndex][0][1]):
                return (midIndex,breakFlag)
            elif(useCount<self.wordCollection[midIndex][0][1]):
                return (midIndex+1,breakFlag)
        elif(breakFlag==1):
            return (correctIndex,breakFlag)
    
    def updateWordDictionary(self,position,wordData,oldCollectionPosition = None,oldWordPosition = None,breakFlag = None):
        #this function is used to update the dictionary of collections of words
        #position is the current index of the new collection to which the new word or the updated existing word will belong
        #wordData is the list of rank,useCount and the word itself
        #oldCollectionPosition is the index of the old collection to which the updated word belonged
        #oldWordPosition is the index of the updated word in its old collection
        #breakFlag is used as an indicator for whether the updated word goes into one of the existing collection or not
        if(breakFlag==None):
            #when this code block is executed then the new word is appended to the dictionary with its own collection
            if(position==len(self.wordDictionary.keys())):
                self.wordDictionary[position] = [wordData]
        else:
            if(breakFlag==1):
                print("breakFlag = 1")
                print("\n")
                #when this code block is executed then either the new word has the rank equal to a existing collection or an existing word is updated to a new existing position
                if(oldCollectionPosition!=None and oldWordPosition!=None):
                    if(len(self.wordDictionary[oldCollectionPosition])==0):
                        print("old collection in dictionary : ",self.wordDictionary[oldCollectionPosition])
                        #self.wordDictionary.pop(oldCollectionPosition)
                        keys = list(self.wordDictionary.keys())
                        print("keys : ",keys)
                        for key in keys[oldCollectionPosition:len(keys)-1]:
                            self.wordDictionary[key] = self.wordDictionary[key+1]
                        del(self.wordDictionary[keys[-1]])
                    else:
                        del(self.wordDictionary[oldCollectionPosition][oldWordPosition])
                else:
                    self.wordDictionary[position].append(wordData)
            elif(breakFlag==0):
                #this code block updates the dictionary when a new word is added or if any updated existing did not get placed in a existing collection then it creates its new collection using its own new collection index 
                print(self.wordCollection)
                print("\n")
                updatedDictionary = {}
                for i,collection in enumerate(self.wordCollection):
                    updatedDictionary[i] = collection
                self.wordDictionary = updatedDictionary
        return self.wordDictionary