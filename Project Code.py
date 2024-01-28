 def Help():  #menu to help user perform tasks
    print()
    print("S - See stock")
    print("P - Purchase")
    print("R - Replenish inventory ")
    print("B - Show bakery profit")
    print("Q - Quit") 
    print()

def See():  #view the inventory in tabular format
    
    lines()
    print("ASTER inventory - ")
    print()
    
    import mysql.connector as mysql
    mydb = mysql.connect(host="localhost", user="root", \
                               password="adwaiy2912", database="ASTER")
    mycursor = mydb.cursor()
    mycursor.execute("select * from inventory;")
    
    print ("{:<9} {:<24} {:<7} {:<7} {:<7}".format('ID','Name', 'Qty', 'CP', 'SP')) 
    for record in mycursor:
        ID, Name, Qty, CP, SP = record[0], record[1], record[2], record[3], record[4]
        print ("{:<9} {:<24} {:<7} {:<7} {:<7}".format(ID, Name, Qty, CP, SP))
    #display the content of the inventory in evenly seperated rows and columns
    lines()    
    
 
def Purchase():  #make a purchase from the inventory
    
    bill={}
    totalPrice = 0
    
    import mysql.connector as mysql
    mydb = mysql.connect(host="localhost", user="root", \
                               password="adwaiy2912", database="ASTER")
    mycursor = mydb.cursor()
    mycursor.execute("select * from inventory;")
    inventory = mycursor.fetchall()
    
    Exit1 = False
    while (Exit1 == False):
        
        itemID = input("Enter item ID: ")
        x,y,z = itemID[0:1], itemID[1:3], itemID[3:6]
        itemID = x.upper() + y.lower() + z  #confims that itemid is in correct format
        
        flag = False
        for record in range(len(inventory)):
            if (itemID in inventory[record][0]):
    
                Exit2 = False
                while (Exit2 == False):
                    item = inventory[record]
                    print()
                    print(item[1], "is available for ₹", item[4], "each")
                    itemQty = int(input("Enter item Quantity: "))
                    
                    if (itemQty <= item[2] and itemQty > 0):
                        Exit2 = True
                        ID = (itemQty,item[0])
                        mycursor.execute("update inventory set quantity = quantity - %s \
                                         where product_id = %s",ID)
                        mydb.commit()
                        itemTotal = itemQty * item[4]
                        totalPrice += itemTotal
                        
                        if (itemID not in bill):
                            bill[itemID] = {}
                            bill[itemID]["Name"] = item[1] 
                            bill[itemID]["Qty"] = itemQty
                            bill[itemID]["IP"] = item[4]
                            bill[itemID]["SubT"] = itemQty * item[4]
                            
                        elif bill[itemID]["Qty"] + itemQty > item[2]:
                            print()
                            print("Total item quantity exceeds inventory limit. \
                                  Thus transaction declined")
                            ID = (itemQty,item[0])
                            mycursor.execute("update inventory set quantity = quantity + %s \
                                         where product_id = %s",ID)
                            mydb.commit()
                            
                        else:
                            bill[itemID]["Qty"] += itemQty
                            bill[itemID]["SubT"] += itemQty * item[4]
                        print()
                        
                        print ("{:<23} {:<7} {:<7} {:<7}".format('Name', 'Qty', 'IP', 'SubTotal'))  
                        for key, val in bill.items(): 
                            Name, Qty, IP, SubT = val["Name"], val["Qty"], val["IP"], val["SubT"]
                            print ("{:<23} {:<7} {:<7} {:<7}".format(Name, Qty, IP, SubT))
                        print() 
                        print("Total (not including taxes) = ₹", totalPrice)
                        #prints bill in tabular format
                        
                        Exit3 = False
                        while (Exit3 == False):
                             
                            print()
                            print("Press A to Add more items")
                            print("Press C to Checkout")
                            print()
                            choice = input("Enter your choice: ")
                            choice = choice.upper()
                            
                            if (choice == "A"):
                                Exit3 = True
                                flag = True
                                break
                                
                            elif (choice == "C"):
                                Exit1 = True
                                Exit3 = True
                                GST = totalPrice * 5/100
                                finalPrice = totalPrice + 2 * GST
                                print()
                                print("CGST = ₹", GST)
                                print("SGST = ₹", GST)
                                print()
                                print("Final total (including tax) = ₹", finalPrice)
                                print()
                                print("Thank you for shopping with us")
                                lines()
                                return totalPrice
                                
                            else:
                                print("Invalid input. Try again")
                                
                    
                    elif (itemQty != 0 and item[2] != 0):
                        print()
                        print("Sorry. We only have", item[2], item[1], "available")
                        print()
                    
                    elif (itemQty <= 0):
                        print()
                        print("Error. Invalid input")
                        print()
                            
                    else:
                        Exit2 = True
                        print()
                        print("Sorry. We are out of stock")
                        print()
                        
            else:
                pass
        
        else:
            if flag == True:
                pass
            else:
                print("Invalid item ID. Try again")
                

def Replenish():  #fill items to its default value
    
    amount = 0
    import mysql.connector as mysql
    mydb = mysql.connect(host="localhost", user="root", \
                               password="adwaiy2912", database="ASTER")
    mycursor = mydb.cursor()
    mycursor.execute("select * from inventory;")
    inventory = mycursor.fetchall()
    
    for item in inventory:
        currQty = item[2]
        
        if (item[0][0:3] == "Bis" and currQty != 50):
            soldQty = 50 - currQty
            amount += item[3] * soldQty
            
        elif (item[0][0:3] == "Bre" and currQty != 30):
            soldQty = 30 - currQty
            amount += item[3] * soldQty
        
        elif (item[0][0:3] == "Bro" and currQty != 25):
            soldQty = 25 - currQty
            amount += item[3] * soldQty
            
        elif (item[0][0:3] == "Cak" and currQty != 15):
            soldQty = 15 - currQty
            amount += item[3] * soldQty
            
        elif (item[0][0:3] == "Coo" and currQty != 60):
            soldQty = 60 - currQty
            amount += item[3] * soldQty
            
        elif (item[0][0:3] == "Don" and currQty != 40):
            soldQty = 40 - currQty
            amount += item[3] * soldQty
            
        elif (item[0][0:3] == "Rol" and currQty != 20):
            soldQty = 20 - currQty
            amount += item[3] * soldQty
            
    if (amount == 0):
        print()
        print("Inventory is full and hence cannot be replenished")
        lines()
        return 0
    
    Exit = False
    while (Exit == False):
        print()
        print("Press Y to replenish inventory by paying ₹", amount)
        print("Press N to cancel the transaction")
        print()
        choice = input("Enter your choice: ")
        choice = choice.upper()
        
        if (choice == "Y"):
            Exit = True
            
            for item in inventory:
                ID = (item[0],)
                
                if (item[0][0:3] == "Bis"):
                    mycursor.execute("update inventory set quantity = 50 where \
                                     product_id = %s",ID)
                    mydb.commit()
                    
                elif (item[0][0:3] == "Bre"):
                    mycursor.execute("update inventory set quantity = 30 where \
                                     product_id = %s",ID)
                    mydb.commit()
            
                elif (item[0][0:3] == "Bro"):
                    mycursor.execute("update inventory set quantity = 25 where \
                                     product_id = %s",ID)
                    mydb.commit()
                    
                elif (item[0][0:3] == "Cak"):
                    mycursor.execute("update inventory set quantity = 15 where \
                                     product_id = %s",ID)
                    mydb.commit()
            
                elif (item[0][0:3] == "Coo"):
                    mycursor.execute("update inventory set quantity = 60 where \
                                     product_id = %s",ID)
                    mydb.commit()
            
                elif (item[0][0:3] == "Don"):
                    mycursor.execute("update inventory set quantity = 40 where \
                                     product_id = %s",ID)
                    mydb.commit()
            
                elif (item[0][0:3] == "Rol"):
                    mycursor.execute("update inventory set quantity = 20 where \
                                     product_id = %s",ID)
                    mydb.commit()
                    
            print()
            print("Transaction successful. Inventory replenished")
            lines()
            return amount
        
        elif (choice == "N"):
            Exit = True
            print()
            print("Transaction successfully cancelled")
            lines()
            return 0
            
        else:
            print("Invalid input. Try again")                     


def lines():  #for better and clear division of commands
    print()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print()

def Main():  #the main menu or parent function
    
    print()
    print("Welcome to ASTER BAKERY")
    comm = ""
    Esc = False
    
    while(Esc == False):
        Help()
        comm = input("What would you like to do? ") 
        comm = comm.upper()
        
        import mysql.connector as mysql
        mydb = mysql.connect(host="localhost", user="root", \
                               password="adwaiy2912", database="ASTER")

        mycursor = mydb.cursor()
        mycursor.execute("select * from totalprofit;")
        for tupProfit in mycursor:
            for intProfit in tupProfit:
                profit = intProfit  #converts bakery profit from nested tuple to integer
        
        if (comm == "S"):
            See()
                
        elif (comm == "P"):
            purchaseProfit = Purchase()
            purchaseProfit = (purchaseProfit,)
            mycursor.execute("update totalprofit set profit = profit + %s", purchaseProfit)
            mydb.commit()
            
        elif (comm == "R"):
            if (profit == 0):
                print()
                print("No profit earned and hence cannot replenish inventory")
                lines()
                
            else:
                replenishCost = Replenish()
                replenishCost = (replenishCost,)
                mycursor.execute("update totalprofit set profit = profit - %s", replenishCost)
                mydb.commit()
            
        elif (comm == "B"):
            print()
            print()
            print("Current Bakery profit = ₹", profit)
            lines()
            
        elif (comm == "Q"):
            Esc = True
            print()
            print()
            print("Thank you for your time")
            print()
            
        else:
            print()
            print("Error! Invalid Input. Try Again")
            
            
Main()