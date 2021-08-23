import numpy as np

def detemine_sub_cost (str1_ch, str2_ch, defaultSubCost, subCostList):

    subCost_ch1_ch2 = subCostList.get((str1_ch, str2_ch))
    subCost_ch2_ch1 = subCostList.get((str2_ch, str1_ch))

    if subCost_ch1_ch2 is not None:
        return subCost_ch1_ch2
    elif subCost_ch2_ch1 is not None:
        return subCost_ch2_ch1
    return defaultSubCost

def editDistance(str1, str2, deleteCost = 1, defaultSubCost = 2, subCostList = {}):
    
    if (deleteCost < 0 or defaultSubCost < 0 or any(value < 0 for value in subCostList.values())):
        return 'not a valid delete or sub cost' #an exception can be thrown as well.
    
    #Convert Strings to lowercase
    str1_lowercase = str1.lower()
    str2_lowercase = str2.lower()

    number_of_columns = len(str1_lowercase) + 1
    number_of_rows = len(str2_lowercase) + 1

    distance_matrix = np.zeros([number_of_columns, number_of_rows])
    
    #init the first row and first and the first column
    for index in range(1 , number_of_columns):
        distance_matrix [index, 0] = distance_matrix [index -1, 0] + deleteCost
    for index in range(1, number_of_rows):
        distance_matrix [0, index] = distance_matrix [0, index -1] + deleteCost

    for i in range (1, number_of_columns):
        for j in range (1 , number_of_rows ):
            if str1_lowercase[i -1] == str2_lowercase[j -1]:
                distance_matrix[i, j] = distance_matrix[i - 1 , j -1]
            else:
                distance_matrix[i, j] = min(distance_matrix[i-1,j] + deleteCost,
                                        distance_matrix[i-1,j-1] + detemine_sub_cost(str1_lowercase[i -1],
                                                                                     str2_lowercase[j -1], 
                                                                                     defaultSubCost,
                                                                                     subCostList),
                                        distance_matrix[i, j-1] + deleteCost)    
    return distance_matrix[number_of_columns -1, number_of_rows -1]

class myDict:
    wordlist = []
    matches = []
    def __init__(self, w):
        self.wordlist = [x for x in w]
        self.wordlist = sorted(self.wordlist)
    def print(self):
        for x in self.wordlist:
            #return the list in alphabetical format
            print(x)
    def search(self, str, maxDistance, deleteCost = 1, defaultSubCost = 2,
        subCostList = {}):
        self.matches = []
        for word in self.wordlist:
             if editDistance(word, str, deleteCost, defaultSubCost ,subCostList) <= maxDistance:
                 self.matches.append(word.lower())
        return sorted(self.matches)