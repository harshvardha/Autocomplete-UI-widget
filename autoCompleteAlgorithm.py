import sys
import os
from . import wordDictionary
class storageNode:

    """this class object is used to store the filterList through which the suggestions will be returned
        and will be stored in the stackList and will be filtered accordingly the inputs.
        This class object consist of a filterList variable which will be used to store the filterList
        at every single input character to remember each and every change in the filter list on every
        single input character.
        
        second variable is the hintString which will store the hintString used to filter the filterList
        according to the input character appended to it so that we can know at each and every step what
        user has typed or inputted
        
        last is the IS_SORTED constant variable which stores 0 if the respective filterList is not
        sorted and stores 1 if the respective filterList is sorted."""

    def __init__(self,filterList,hintString):
        self.filterList = filterList
        self.hintString = hintString
        self.IS_SORTED = 0
    
    def getFilterList(self):
        return self.filterList
    
    def getHintString(self):
        return self.hintString

    def setFilterList(self,filterList):
        #if the length of the filterList is equal to the not sorted filterList and not equal to 0 then only it can be replaced
        if(len(filterList)>0 and len(filterList)==len(self.filterList)):
            self.filterList = filterList
            self.IS_SORTED = 1

class autoCompleteAlgo:
    def __init__(self,Type):
        self.Type = Type
        self.dictionaryObject = wordDictionary.dictionaryManager(self.Type)
        self.dictionary = self.getDictionary()
        self.dictionaryKeys = list(self.dictionary.keys())
        self.hintString = ""
        self.inputStorageVariable = ""
        self.lastSpaceCharacterIndex = -1
        self.filterList = []
        self.stackList = []
    
    def getDictionary(self):
        return self.dictionaryObject.dictionaryGenerator()
    
    def getTopSuggestions(self):

        """This function will return the list of the words which are used most rank wise or
            use_count wise as both the things are same and its not neccesary to return exactly atmost
            5 words it can return less than 5 also but not more than 5 and this function will be 
            executed only one when the respective input widget gets the focus and as soon as widget gets the focus
            this function will be called and it will return the most frequently used words list to display"""
        
        key_index = 0
        value_index = 0
        while((key_index<=self.dictionaryKeys[-1] or value_index<len(self.dictionary[key_index])) and len(self.filterList)<5):
            try:
                self.filterList.append(self.dictionary[self.dictionaryKeys[key_index]][value_index])
            except:
                value_index = 0
                key_index += 1
                if(key_index<=self.dictionaryKeys[-1]):
                    self.filterList.append(self.dictionary[self.dictionaryKeys[key_index]][value_index])
                else:
                    break
            value_index += 1
        if(len(self.filterList)!=0):
            self.stackList.insert(0,storageNode(self.filterList.copy(),""))
            print(self.stackList[0])
            self.filterList.clear()
            return self.stackList[0].getFilterList()

    def returnSuggestion(self,event,currentCursorPosition,lastIndex):

        """This function is the core part of this algorithm because after the input widget gets the
            focus and the getTopSuggestion function is executed after then when user will start giving
            the input character and using those inputs this function will construct the hint string
            and using that hint string it will filter the results to be displayed."""

        char = event.char
        dummyFilterList = self.filterList.copy()
        if(char!="\x08" and char!="\t" and char!="\r" and char!="" and char!=" "):

            """This block of code is executed each time user enters any character except the
                'backspace','tab','return','empty string' and 'space character' and this block is
                responsible for the building of the hintString which is used to filter the results.
                Because hint string cannot contain the above mentioned characters thats why they
                are neglected and also because they are special characters that cannot act as
                a part of hintString.
                
                Here inputStorageVariable is used to store all the characters that user has
                entered during its input session with the widget so that we can extract out any
                word which needs to be updated to a new collection due to its increase use count
                which will further result in rank increase of the respective word or to extract
                out if any new word is used and add it to the dictionary."""
            if(currentCursorPosition>self.lastSpaceCharacterIndex):
                if(currentCursorPosition-lastIndex==1):
                    self.hintString = self.hintString+char
                    self.inputStorageVariable = self.inputStorageVariable+char
                    lastIndex = len(self.inputStorageVariable)-1
                else:
                    self.inputStorageVariable = self.inputStorageVariable[:currentCursorPosition]+char+self.inputStorageVariable[currentCursorPosition+1:]
                    self.lastSpaceCharacterIndex += 1
                    self.hintString = self.inputStorageVariable[self.lastSpaceCharacterIndex+1:]
            else:
                self.inputStorageVariable = self.inputStorageVariable[:currentCursorPosition]+char+self.inputStorageVariable[currentCursorPosition+1:]
                self.lastSpaceCharacterIndex += 1
                return None
        elif(char=="\x08" and len(self.stackList)!=0):

            """This block of code is executed when the user presses the backspace button or if the
                stackList is empty.
                
                when user presses the backspace button then the last character from the hintString
                is removed and the length of the hintString is reduced by one and the same is done to
                the inputStorageVariable so that it remains synced with the hintString. After the
                reduction of a character from the hintString the respective storage object is
                removed from the stackList and the filterList is changed and the length of the
                stackList is reduced by one and at this moment the storage object at index 0 of
                the stackList returns the filterList compatible with the hintString stored in the
                storage object"""
                
            if(currentCursorPosition<self.lastSpaceCharacterIndex):
                currentCursorPosition -= 2
                self.inputStorageVariable = self.inputStorageVariable[:currentCursorPosition+1]+self.inputStorageVariable[currentCursorPosition+2:]
                self.lastSpaceCharacterIndex -= 1
                return None
            
            if(len(self.stackList[0].getHintString())>=1 and currentCursorPosition>self.lastSpaceCharacterIndex):
                if(currentCursorPosition-lastIndex==1):
                    currentCursorPosition = lastIndex-1
                    self.hintString = self.stackList[0].getHintString()[:currentCursorPosition+1]
                    self.inputStorageVariable = self.inputStorageVariable[:currentCursorPosition+1]
                else:
                    currentCursorPosition -= 2
                    self.hintString = self.stackList[0].getHintString()[:currentCursorPosition+1]+self.stackList[0].getHintString()[currentCursorPosition+2:]
                    self.inputStorageVariable = self.inputStorageVariable[:currentCursorPosition+1]+self.inputStorageVariable[currentCursorPosition+2:]
                #self.hintString = self.stackList[0].getHintString()[:len(self.stackList[0].getHintString())-1]
                #self.inputStorageVariable = self.inputStorageVariable[:len(self.inputStorageVariable)-1]
            print(self.stackList[0].getFilterList())
            del(self.stackList[0])
            if(len(self.stackList)!=0):
                self.filterList = self.stackList[0].getFilterList()
            else:
                self.filterList.clear()
        elif(char==" "):

            """This block of code is executed when the user completes its word and presses space button to
                input the next word. After the user presses the space button this function first extracts
                the word user inputted recently from the inputStorageVariable and then checks if the
                filterList stored in the storage object at the index 0 of stackList is empty or not.
                If the filterList is empty then the inputted word is a new word and then it perfroms the
                neccesary operations to add that new word to the dictionary and if the filterList is not
                empty then the inputted word is a existing word in one of the collections of the dictionary
                so it takes neccesary steps to update the use count and rank of that word and put it in
                the appropriate collection according to its rank after updation.
                
                After the above task is done it empties the hintString and adds the space character to
                the inputStorageVariable so that we can have the complete input of the user tracked.
                It empties the hintString because the user is now going to enter the new word which will
                be independent of the previous given input characters and now the new hintString will be
                built and filter process will continue according to the new hintString.
                
                Similary the filterList is cleared or emptied so that new words can be added to it based
                on the new hintString built.
                
                lastSpaceCharacterIndex variable stores the index of the previous recent space character
                inputted so that we can get the starting index of the next word user is going to input
                because the next word will start from lastSpaceCharacterIndex+1 index and it will help us
                to extract the next word user will enter.
                
                extraction works as follows:
                            suppose inputStorageVariable = 'harsh jaydev ...'
                            here if we want to extract the word harsh we can get it by using the substring method
                            
                            extracted_word = inputStorageVariable[lastSpaceCharacterIndex+1:len(inputStorageVariable)-1]"""

            self.inputStorageVariable = self.inputStorageVariable+char
            if(len(self.stackList[0].getFilterList())==0):
                newWord = self.inputStorageVariable[self.lastSpaceCharacterIndex+1:len(self.inputStorageVariable)-1]
                print("newWord : ",newWord)
                returnStatus = self.dictionaryObject.addNewWord(newWord,1)
                print("returnStatus : ",returnStatus)
                if(len(returnStatus)==2):
                    self.dictionary = self.dictionaryObject.updateWordDictionary(returnStatus[0],returnStatus[1])
                elif(len(returnStatus)==3):
                    self.dictionary = self.dictionaryObject.updateWordDictionary(position = returnStatus[0],wordData = returnStatus[1],breakFlag = returnStatus[2])
                self.dictionaryKeys = list(self.dictionary.keys())
            else:
                updateExistingWord = self.inputStorageVariable[self.lastSpaceCharacterIndex+1:len(self.inputStorageVariable)-1]
                wordCollectionkey = self.findThePosition(updateExistingWord)
                print("wordCollectionKey : ",wordCollectionkey)
                wordPosition = self.findWordPosition(updateExistingWord,wordCollectionkey)
                print("wordPosition : ",wordPosition)
                print("\n")
                returnTuple = self.dictionaryObject.updateUseCount((wordCollectionkey,wordPosition),1)
                print("return tuple : ",returnTuple)
                print("\n")
                self.dictionary = self.dictionaryObject.updateWordDictionary(returnTuple[0],returnTuple[1],returnTuple[2],returnTuple[3],returnTuple[4])
                self.dictionaryKeys = list(self.dictionary.keys())
                print("dictionary : ",self.dictionary)
                print("\n")
                print("dictionary keys : ",self.dictionaryKeys)
                print("\n")
            self.hintString = ""
            self.filterList.clear()
            self.lastSpaceCharacterIndex = len(self.inputStorageVariable)-1
            lastIndex = len(self.inputStorageVariable)-1
        if(len(self.filterList)!=0 and char!="\x08"):

            """This block of code is executed when the filterList is not empty and inputted character
                is not the space character. This block of code simply removes the word whose substring
                does not equal to hintString even if any single character is different the word is
                removed from the filterList and the filtered list is pushed to the stack with its
                storage object at index 0."""

            for word in dummyFilterList:
                if(self.hintString!='' and len(word[2])>=len(self.hintString)):
                    if(word[2][:len(self.hintString)]!=self.hintString):
                        self.filterList.remove(word)
                else:
                    self.filterList.remove(word)
            self.stackList.insert(0,storageNode(self.filterList.copy(),self.hintString))
        else:

            """This block of code is executed when the length of the filterList is 0. This block
                of code is executed when the filterList is empty and this block of code simply
                adds all the words to the filterList whose first character matches with the first
                character in the hintString after it is empty i.e. when either the user starts
                providing the input or the hintString gets empty when the user presses the space
                button as user will start inputting a new word.
                
                for ex- when hintString = '' and filterList is empty then when user inputs first
                character like if user inputs 'h' then hintString = 'h' so now this block of code
                will find all the words starting with 'h' in the dictionary and add them to the
                filterList and push the filterList to the top of the stack i.e. on index 0
                
                This block of code will not execute if user presses backspace button or any
                other button. It will only execute one time when the hintString = '' or empty."""

            if(char!="\x08" and char!=""):
                for key in self.dictionaryKeys:
                    collection = self.dictionary[key]
                    for word in collection:
                        if(word[2][:len(self.hintString)]==self.hintString):
                            self.filterList.append(word)
                self.stackList.insert(0,storageNode(self.filterList.copy(),self.hintString))
        if(len(self.stackList)!=0):
            print(self.stackList[0].getFilterList())
            return (self.stackList[0].getFilterList(),lastIndex)
    
    def findThePosition(self,updatedWord):
        #This function finds the position of the collection to which the word to be updated belongs currently.
        #updatedWord contains the word whose use_count and rank needs to be updated
        if(self.stackList[0].IS_SORTED==0):
            print("not sorted")
            """This block checks if the filterList at the top of the stackList is sorted using the 
                IS_SORTED constant of the storage object of the respective filterList.
                If the IS_SORTED constant is 0 then filterList is not sorted and if it is 1 then
                it is sorted and can be used directly to be searched because we are using the
                binary search algorithm to find the oldCollectionPosition of the word"""

            collectionList = self.stackList[0].getFilterList()
            collectionList = self.mergeSort(collectionList[:len(collectionList)//2],collectionList[len(collectionList)//2:])
            self.stackList[0].setFilterList(collectionList.copy())
        if(self.stackList[0].IS_SORTED==1):
            print("sorted")
        else:
            return
        collectionList = self.stackList[0].getFilterList()
        print("collectionList : ",collectionList)
        print("\n")
        start = 0
        last = len(collectionList)-1
        correctIndex = -1
        while(last>=start and correctIndex==-1):
            midIndex = (start+last)//2
            if(collectionList[midIndex][2]==updatedWord):
                correctIndex = collectionList[midIndex][0]-1
                print("correct index : ",correctIndex)
                print("\n")
                break
            elif(len(collectionList[midIndex][2])>len(updatedWord)):
                last = midIndex-1
            elif(len(collectionList[midIndex][2])<len(updatedWord)):
                start = midIndex+1
        return correctIndex
        #correctIndex is the rank of the word to be updated in the current collection or old collection
        #this return statement returns the key for the old collection to which the word currently belongs
    
    def mergeSort(self,leftSubPart,rightSubPart):
        if(len(leftSubPart)>1):
            leftSubPart = self.mergeSort(leftSubPart[:len(leftSubPart)//2],leftSubPart[len(leftSubPart)//2:])
        if(len(rightSubPart)>1):
            rightSubPart = self.mergeSort(rightSubPart[:len(rightSubPart)//2],rightSubPart[len(rightSubPart)//2:])
        sortedList = self.sortSubPart(leftSubPart,rightSubPart)
        print(sortedList)
        return sortedList
    
    def sortSubPart(self,leftPart,rightPart):
        combinedList = leftPart+rightPart
        for i in range(len(combinedList)):
            for j in range(0,len(combinedList)-1-i):
                if(len(combinedList[j][2])>len(combinedList[j+1][2])):
                    temp = combinedList[j+1]
                    combinedList[j+1] = combinedList[j]
                    combinedList[j] = temp
        print("combined list : ",combinedList)
        print("\n")
        return combinedList

    def findWordPosition(self,word,wordCollectionKey):
        #word contains the word that needs to be updated.
        #wordCollectionKey contains the key for the old collection to which the word currently belongs
        """This function finds the index of the word in its old collection. Since the collection
            will not be sorted so first we will sort the collection using mergeSort algo and then
            using the binary search algo we will find the index of the word."""
        sortedCollection = self.dictionary[wordCollectionKey]
        print("sorted collection before sorting : ",sortedCollection)
        print("\n")
        sortedCollection = self.mergeSort(sortedCollection[:len(sortedCollection)//2],sortedCollection[len(sortedCollection)//2:])
        self.dictionary[wordCollectionKey] = sortedCollection
        print("length of dictionaryObject.wordCollection : ",len(self.dictionaryObject.wordCollection))
        print("\n")
        print("dictionaryObject.wordCollection : ",self.dictionaryObject.wordCollection)
        self.dictionaryObject.wordCollection[wordCollectionKey] = self.dictionary[wordCollectionKey]
        print("\n")
        print("sortedCollection : ",sortedCollection)
        print("\n")
        print("sortedCollection in dictionary : ",self.dictionary[wordCollectionKey])
        print("\n")
        start = 0
        last = len(sortedCollection)-1
        wordIndex = -1
        while(last>=start and wordIndex==-1):
            midIndex = (start+last)//2
            if(sortedCollection[midIndex][2]==word):
                wordIndex = midIndex
                break
            elif(len(sortedCollection[midIndex][2])>len(word)):
                start = midIndex+1
            elif(len(sortedCollection[midIndex][2])<len(word)):
                last = midIndex-1
        return wordIndex

    def updateHintString(self,string):
        self.hintString = string
        #if(len(self.inputStorageVariable)>0):
        print(self.lastSpaceCharacterIndex)
        self.inputStorageVariable = self.inputStorageVariable+self.hintString
        #else:
            #self.inputStorageVariable += self.hintString

# if __name__=="__main__":
#     obj = autoCompleteAlgo("nameDictionary")
#     print(obj.getTopSuggestions())