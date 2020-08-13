import copy
import os
import re

lockTableObjects = []
transactionTableObjects = []
waitingTransactions = []
OperationList = []
RL = "readlock"
WL = "writeLock"
A = "Abort "
W = "Waiting"
C = "Committed"
AC = "Active"
returnflag = 1



class transactionTable():
    def __init__(self, transactionID, transaction_timestamp, transactionState):
        self.transactionID = transactionID
        self.timestamp = transaction_timestamp
        self.transactionState = transactionState
        self.lockedResoures = []
        self.blockedOperation = []

    def changeTransactionState(self, state):
        self.transactionState = state

    def addBlockedOperation(self, operation):
        self.blockedOperation.append(operation)

    def addLockedResource(self, resourceName):
        self.lockedResoures.append(resourceName)



class lockTable:
    def __init__(self, lockedDataItem, transactionID, lockState):
        self.lockedDateItem = lockedDataItem
        self.lockState = lockState
        self.waitingTransactions = []
        self.lockHeldBy = []
        self.lockHeldBy.append(transactionID)

    def addWaitingTransaction(self, transactionID):
        self.waitingTransactions.append(transactionID)

    def addLockHeld(self, transactionID):
        self.lockHeldBy.append(transactionID)

    def changeLockState(self, LS):
        self.lockState = LS





# This function is used to identify the Transaction Number(digit) from the given string. 
def get_digit(str1):
    c = ""
    for i in str1:
        if i.isdigit():
           return int(c+i)

    


# This function adds a new object to the transactionTableObject every time a new transaction is started.
def TransactionBegin(str):
    tranNumber = get_digit(str)
    print("Begin Transaction %d " % (tranNumber))
    print("Transaction Timestamp %d " % (tranNumber))
    temp = int(len(transactionTableObjects)) + 1
    transactionTableObjects.append(transactionTable(tranNumber, temp, AC))


# This Function returns the resource name(A-Z) and the transactionID.
def resourcenID(inputLine):
    resource = re.findall('([A-Z])', inputLine)
    resourceName = ''.join(resource)
    transactionID = get_digit(inputLine)
    return resourceName, transactionID


# This Function take the transaction ID and searches it for the transaction in the transactionTable
def searchTransactionID(transactionID):
    for transaction in transactionTableObjects:
        if transaction.transactionID == transactionID:
            return transaction


# This function performs Read Operation for the specific transaction.
# It checks for the transaction state before performing the operation.
# Any conflicting locks are taken care by wound wait mechanism to avoid deadlocks.
def OperationRead(inputLine):
    if checkState(inputLine): # Checks the Transaction State.
        resourceName = resourcenID(inputLine)[0] 
        transactionID = resourcenID(inputLine)[1]
        flag = 0
        length = len(lockTableObjects)
        if length != 0:
            for i in range(0, length):
                if lockTableObjects[i].lockedDateItem == resourceName:
                    flag = 1
                    if lockTableObjects[
                        i].lockState == WL:  # This checks if the resource that's been requested in under a writeLock by any other transaction and if True, wound wait is called
                        print("Conflicting Write lock: data item " + resourceName + " is under WriteLock by Transaction %d" % (
                            lockTableObjects[i].lockHeldBy[0]))
                        print ("calling wound-wait mechanism")
                        woundWait(searchTransactionID(transactionID),
                                searchTransactionID(lockTableObjects[i].lockHeldBy[0]), lockTableObjects[i], inputLine)
                    elif lockTableObjects[
                        i].lockState == RL:  # if resources is just under readLock, the new transaction is added to the list of transactions that hold a readLock on the same resource.
                        lockTableObjects[i].addLockHeld(transactionID);
                        searchTransactionID(transactionID).addLockedResource(resourceName)
                        print ("Granting the ReadLock on the data item " + resourceName + " by Transaction %d" % (
                            lockTableObjects[i].lockHeldBy[-1]))
            if flag == 0:
                lockTableObjects.append(lockTable(resourceName, transactionID,
                                                RL))  # adding a new resource to the locktable if its not already in the lockTable
                searchTransactionID(transactionID).addLockedResource(resourceName)
                print ("Granting the ReadLock on the data item " + resourceName + " by Transaction %d" % transactionID)
        else:
            lockTableObjects.append(lockTable(resourceName, transactionID, RL))
            searchTransactionID(transactionID).addLockedResource(resourceName)
            print ("Granting the ReadLock on the data item " + resourceName + " by Transaction %d" % (
                lockTableObjects[0].lockHeldBy[0]))


# This function performs Write Operation for the specific transaction.
# It checks for the transaction state before performing the operation.
# Any conflicting locks are taken care by wound wait mechanism to avoid deadlocks.
def OperationWrite(inputLine): 
    if checkState(inputLine):
        resourceName = resourcenID(inputLine)[0]     
        transactionID = resourcenID(inputLine)[1]   
        flag = 0
        length = len(lockTableObjects)
        if length != 0:
            for i in range(0, length):
                if lockTableObjects[i].lockedDateItem == resourceName: 
                    flag = 1 
                    if lockTableObjects[i].lockState == RL:
                        if len(lockTableObjects[i].lockHeldBy) == 1: 
                            if lockTableObjects[i].lockHeldBy[
                                0] == transactionID:  # checks to see if the resources is under readLock by the same transaction
                                lockTableObjects[i].lockState = WL
                                print ("Upgrading Readlock to WriteLock on data item " + resourceName + " for Transaction %d" % transactionID)
                            else:
                                print( "Data item " + resourceName + "is under ReadLock by multiple transaction. ")
                                print("calling wound-wait mechanism")  # call wound wait if its under readlock by another transaction
                                woundWait(searchTransactionID(transactionID),
                                        searchTransactionID(lockTableObjects[i].lockHeldBy[0]), lockTableObjects[i],
                                        inputLine)
                        else:
                            count = 0
                            for lockedresource in lockTableObjects:
                                if lockedresource.lockedDateItem == resourceName:
                                    for tempheldby in lockedresource.lockHeldBy:
                                        # print("temphelby : ", tempheldby)
                                        if tempheldby == transactionID:
                                            count += 1
                            woundWait(searchTransactionID(transactionID),
                                    searchTransactionID(lockTableObjects[i].lockHeldBy[count]), lockTableObjects[i],
                                    inputLine)
                    elif lockTableObjects[i].lockState == WL:
                        print ("Conflicting WriteLock: data item " + resourceName + " is under WriteLock by Transaction %d" % (
                            lockTableObjects[i].lockHeldBy[0]))
                        print ("calling wound-wait mechanism")
                        woundWait(searchTransactionID(transactionID),
                                searchTransactionID(lockTableObjects[i].lockHeldBy[0]), lockTableObjects[i], inputLine)
            if flag == 0:
                lockTableObjects.append(lockTable(resourceName, transactionID, WL))  # appending a new resource to the lockTable
                searchTransactionID(transactionID).addLockedResource(resourceName)
                print ("Data item " + resourceName + " is under WriteLock by Transaction %d" % (
                    lockTableObjects[0].lockHeldBy[0]))
        else:
            lockTableObjects.append(lockTable(resourceName, transactionID, WL))
            searchTransactionID(transactionID).addLockedResource(resourceName)


# the wound wait deadlock prevention mechanism
def woundWait(requestingTransaction, holdingTransaction, lockedResource, operation):
    if requestingTransaction.timestamp < holdingTransaction.timestamp:
        holdingTransaction.changeTransactionState(A)
        print("Aborting Transaction %d" % holdingTransaction.transactionID)
        requestingTransaction.changeTransactionState(W)
        requestingTransaction.addBlockedOperation(operation)
        waitingTransactions.append(requestingTransaction)
        unlock(
            holdingTransaction.transactionID)  # unlocking all the resources of the transaction that was aborted by wound wait
    else:
        requestingTransaction.changeTransactionState(W)  # adds the transaction to the waitingTransactions list
        print("Changing transaction state for Transaction %d to blocked" % requestingTransaction.transactionID)
        if checkDuplicateOperation(operation, requestingTransaction):
            requestingTransaction.addBlockedOperation(operation)
        if checkDuplicateTransaction(requestingTransaction):
            waitingTransactions.append(requestingTransaction)
        
        
        
        



# this method checks to see if the transaction is already in the waitingTransactions list
def checkDuplicateTransaction(requestingTransaction):
    for t in waitingTransactions:
        if t.transactionID == requestingTransaction.transactionID:
            return False
        elif t.timestamp > requestingTransaction.timestamp:# if the witing transcation timesstamp is more then the requesting timestamp. Waiting one aborts
            t.changeTransactionState(A)
            print("Aborting Transaction %d" % t.transactionID)
            unlock(t.transactionID)
    return True
    
    

def checkDuplicateOperation(operation, transaction):
    for blockedOperation in transaction.blockedOperation:
        if blockedOperation == operation:
            return False
    return True


# This function checks the state of the transaction.
# This fnction is used to check if the transaction is aborted, the operation  can be ignored.
def checkState(operation):
    resourceName = resourcenID(operation)[0]
    transactionID = resourcenID(operation)[1]
    length = len(transactionTableObjects)
    if length != 0:
        for i in range(0, length):
            if transactionTableObjects[i].transactionID == transactionID and transactionTableObjects[
                i].transactionState == W:
                transactionTableObjects[i].addBlockedOperation(operation)
                print("Since Transaction is blocked "+operation+" is added to waiting operation.")
                return False
            elif transactionTableObjects[i].transactionID == transactionID and transactionTableObjects[i].transactionState == A:
                operation = ""
                print("Operation Ignored , Since Transaction %d is already Aborted. "%transactionID)
                return False
    return True


# This Function deletes and unlocks all the resourced held by the transactionID passed to it
def unlock(transactionID):
    print("Unlocking all resources held by transaction %d" % transactionID)
    for transaction in transactionTableObjects:
        if transaction.transactionID == transactionID:
            for lock in transaction.lockedResoures:
                for resource in lockTableObjects:
                    if resource.lockedDateItem == lock:
                        if len(resource.lockHeldBy) == 1:
                            lockTableObjects.remove(
                                resource)  # if the same sources is held by multiple transactions, remove this transaction from that list of transactions holding the lock
                        else:
                            resource.lockHeldBy.remove(
                                transactionID)  # if only this transaction has any kind of lock on the resource, remove the resource from the lockTable completely.
    startWaitingTrans()


# This function chekcs if any transactions that were waiting for resources can now be resumed or not.
def startWaitingTrans():
    for transaction in waitingTransactions:
        if transaction.transactionState == A or transaction.transactionState == C :
            waitingTransactions.remove(transaction)
        else:
            blockOpCopy = copy.deepcopy(transaction.blockedOperation)
            for blockedOperation in transaction.blockedOperation:
                transaction.transactionState = AC  # transaction in the waitingTransactions list gets activated and operations gets pulled that are in the waitlist
                print("Attempting operation " + blockedOperation)
                assignOperation(
                    blockedOperation)  # call the assignOperation method on the waiting operation and see if the transaction can now continue
                if transaction.transactionState != W:
                    blockOpCopy.remove(blockedOperation)
            transaction.blockedOperation = blockOpCopy
            if len(transaction.blockedOperation) == 0:
                waitingTransactions.remove(transaction)


# called when the function reaches its end. This method commits the transaction and frees all its resources.
def OperationEnd(operation):
    tranNumber = get_digit(operation)
    length = len(transactionTableObjects)
    if length != 0:
        for i in range(0, length):
            if transactionTableObjects[i].transactionID == tranNumber and transactionTableObjects[i].transactionState != A:
                print("Committing transaction %d" % tranNumber)
                transactionTableObjects[i].transactionState = C
                unlock(tranNumber)
            elif transactionTableObjects[i].transactionID == tranNumber and transactionTableObjects[i].transactionState == A:
                print("Transaction %d was Aborted." % tranNumber)

    
    


# This method scans the input operation and calls the required function accordingly.
def assignOperation(operation):
    print("-------------------------------------------------------------------------")
    print(operation)
    
    if operation.find('b') != -1:
        TransactionBegin(operation)
    elif operation.find('r') != -1:
        print ("Read operation")
        OperationRead(operation)
    elif operation.find('w') != -1:
        print ("write operation")
        OperationWrite(operation)
    elif operation.find("e") != -1:
        print ("end")
        OperationEnd(operation)


# Scans the nput File for all possible Operation.
for file in os.listdir(os.getcwd()):
    if file.endswith('.txt'):
        with open(file, 'r') as text:
            for line in text:
                OperationList.append(line) # Stores the operation in The operation List.
        for operation in OperationList:
            assignOperation(operation) # calls the assign Operation Function to perform the operation.
