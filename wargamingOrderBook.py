"""
Wargaming Prague: OrderBook class Assignment
@author: Alperen Erol
"""

# Unsorted Linear Search
def seqSearch(arr,element):       
    pos=0
    found=False
    while pos<len(arr) and not found:
        if arr[pos][2]== element:
            found = True
        else:
            pos += 1
    return pos

# To find max value in array elements
def printMax(arr):   
    max = 0   
    n = len(arr)
    for i in range(n):
        if arr[i][-1]==None:
            continue
        if float(arr[i][-1]) > max:
            max = float(arr[i][-1]) 
    return max

# OrderBook class
class OrderBook(object):    
    def __init__(self):        
        self.orderList = [] # maintains a list of current orders that have been added but not deleted yet  
        self.intervalList = [] # maintains current intervals 
        
    # to add order and update intervals   
    def insert(self, order):        
        self.orderList.append(order) # insertion of current order to orderList
        
        # decide whether insert a new interval then insert 
        if len(self.intervalList) == 0: 
            self.intervalList.append([int(order[0]), float(order[3])])
        else:
            # to handle when None valued price exist 
            try: 
                if float(order[3]) > float(self.intervalList[-1][1]):
                    self.intervalList.append([int(order[0]), float(order[3])])
            except:
                self.intervalList.append([int(order[0]), float(order[3])])  
        
    # to delete an order and update intervals   
    def delete(self, unqID, ts):
        # sequential search to find the order to be deleted by its unique id
        pos = seqSearch(self.orderList, unqID) 
        del self.orderList[pos]  
        
        # decide whether insert a new interval then insert
        if len(self.orderList) == 0:
            self.intervalList.append([int(ts), None]) # insert last interval when no more order left
        else:
            maxDel = printMax(self.orderList) # max price in orderList after deletion of an order
            if maxDel > printMax(self.intervalList) or maxDel < printMax(self.intervalList) and len(self.orderList)==1: # takes max priced order after an order deleted decide wheter to insert a new interval and insert
                self.intervalList.append([int(ts), maxDel])  
                
    # calculates and returns time-weighted average maximum price    
    def currentMax(self, ts):
        # to handle when None valued price exist
        try: 
            # find current max price at any time. 
            currMax = [x[1] for x in self.intervalList if x[0] < ts+1][-1] 
            return currMax
        except:
            pass
        
    # getting the actual maximum price of the order at any time (microseconds) 
    def twAverage(self):        
        weighted_sum = []
        prices = []
        weights = []
        
        for i in range(len(self.intervalList)-1):
            # skips None priced interval
            if self.intervalList[i][1] == None: 
                continue
            
            # creation of prices and time interval arrays from intervalList
            prices.append(self.intervalList[i][1]) 
            weight = self.intervalList[i+1][0]-self.intervalList[i][0]
            weights.append(weight)
            
        # calculation of Time-weighted average maximum price      
        for p, t in zip(prices, weights):           
            weighted_sum.append(p * t)
        print ("Time-weighted average maximum price : %5.2f" % round(sum(weighted_sum) / sum(weights),2))
          
if __name__ == '__main__':
    # Initiate the class
    ob = OrderBook()
    
    # Read orders as lines from a text file 
    file1 = open('orderFile.txt', 'r')
    lines = file1.readlines()    
    for line in lines:
        order = line.strip().split(" ") 
        
        # decide the process by type of order(adding or deleting)
        if order[1] == 'I':
            ob.insert(order) 
        if order[1] == 'E':
            ob.delete(order[2],order[0])
            
    curPrice = ob.currentMax(19500) # actual maximum price of the order at any time in microseconds 
    ob.twAverage() # time-weighted average maximum price
   
    