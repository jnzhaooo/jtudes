import random

def func2(amount , num):

    list3 = []
    num2 = num                           
    for i in range(0,num):
        if num2 != 1:                    
            mu = int(amount / num2)
            sigma = 1                    
            isnotpos = True
            while isnotpos:              
                a = random.normalvariate(mu,sigma)
                if a >= 1:
                    if (amount - a) > 0:
                        isnotpos = False
            a = int(a)
            list3.append(a)
            amount = amount - a        
            num2 = num2 - 1            
        else:                         
            a = amount
            list3.append(a)
    return list3


def func1(amount,num):
    list1 = []
    for i in range(0,num-1):
        a = random.randint(1,amount)    
        list1.append(a)
    list1.sort()                        
    list1.append(amount)                

    list2 = []
    for i in range(len(list1)):
        if i == 0:
            b = list1[i]                
        else:
            b = list1[i] - list1[i-1]   
        list2.append(b)

    return list2

def choose(maxValue, num):

    maxValue = int(maxValue)
    suiji_ser = random.sample(range(1,maxValue), k=num-1)
    suiji_ser.append(0)   
    suiji_ser.append(maxValue)
    suiji_ser = sorted(suiji_ser)
    per_all_persons = [ suiji_ser[i]-suiji_ser[i-1] for i in range(1, len(suiji_ser)) ]

    return per_all_persons


