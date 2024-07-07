import os
import data_engine as de
import encryption_engine as ee

try:
    import pandas as pd
except ImportError:
    print("Pandas Library Not Found. Please Install it to Run the Program.")
    exit()
try:
    import zxcvbn
except ImportError:
    print("Module 'zxcvbn' not found. Install it with 'pip install zxcvbn-python'.")
    exit()



global fieldNames
fieldNames = de.fieldNames
global defaultFieldNames
defaultFieldNames = de.defaultFieldNames
global data
data = de.data



def progressivePrint ( string:str , delay:float , end:str = "\n" ):
    # funzione che stampa una stringa in modo progressivo
    import time
    for char in string:
        print( char , end="" , flush=True )
        time.sleep(delay)
    print(end , end="")
    
def waitBeforeProceeding ():
    # funzione che attende che l'utente prema un tasto prima di proseguire
    input("\nPress Enter to Continue")
    clearScreen()

def clearScreen ():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    
def printData ( rawToPrintData:list , printTotEntries:bool = True , printPercentage:bool = True ):
    # funzione che stampa tutti i dati

    global fieldNames

    if len(rawToPrintData) == 0:
        print("No Entries Found to Print.")
        print("TOT. ENTRIES: 0")
        return

    toPrintData = []
    for entry in rawToPrintData:
        toPrintEntry = {}
        for field in fieldNames:
            toPrintEntry[field] = entry[field]
        toPrintData.append(toPrintEntry)

    # in tutte le entry sposto il campo "ID" in prima posizione e il campo "Notes" in ultima posizione
    for entry in toPrintData:
        id_value = entry.pop("ID")
        notes_value = entry.pop("Notes")
        
        # Ricreo l'ordine desiderato dei campi
        new_entry = {"ID": id_value}
        new_entry.update(entry)  # Aggiungo gli altri campi mantenendo il loro ordine
        new_entry["Notes"] = notes_value
        
        # Aggiorno l'entry con il nuovo dizionario
        entry.clear()
        entry.update(new_entry)

    df = pd.DataFrame(toPrintData)
    df = df.to_string(index=False)
    
    print(df)
    
    if printTotEntries == True:
        print("\nTOT. ENTRIES: " + str(len(toPrintData)))
        
    if printPercentage == True:
        percentOfEntries = len(toPrintData) / len(de.data) * 100
        percentOfEntries = round(percentOfEntries, 2)
        if printTotEntries == False:
            print("\nPERCENTAGE: " + str(percentOfEntries) + "%")
        else:
            print("PERCENTAGE: " + str(percentOfEntries) + "%")   
        
        
        
def main ():
    
    global fieldNames
    global defaultFieldNames
    global data
    
    #! accensione del programma
    clearScreen()
    
    #. chiedo all'utente di individuare il file da cui caricare i dati
    while True:
        pathOf_data = input("Enter the path of the file containing the data (Type in NEW to initialize a new Dataset): ")
        if de.pathExists(pathOf_data) and os.path.isfile(pathOf_data):
            break
        elif de.pathExists(pathOf_data) and os.path.isdir(pathOf_data):
            print("The path you entered is a directory. Please enter the path of the file containing the data.")
            continue
        elif pathOf_data == "":
            pathOf_data = "./data/data.dat"
            break
        elif pathOf_data == "NEW":
            break
        else:
            print("File not found. Please try again.")
            continue
    
    #. creazione di un nuovo dataset
    if pathOf_data == "NEW":
        de.initialize_dataset()
        
    #. chiedo all'utente di inserire la chiave di cifratura
    else:
        while True:
            # input del file contenente la chiave
            keyPath = input("Enter the path of the first encryption key: ")
            if de.pathExists(keyPath) and os.path.isfile(keyPath):    
                pass
            elif de.pathExists(keyPath) and os.path.isdir(keyPath):
                print("The path you entered is a directory. Please enter the path of the file containing the key.")
                continue
            else:
                print("File not found. Please try again.")
                continue
            
            # validazione della chiave
            key = ee.get_key(keyPath)
            if key == "FNF":
                print("The key could not be read. File not found. Please try again.")
                continue
            elif key == "ERR":
                print("The key could not be read. An error occurred. Please try again.")
                continue
            else:
                break
            
        load_data_result = de.load_data(key , pathOf_data)
        if load_data_result == "FNF":
            print("File not found. Please try again.")
            exit()
    
        # ultimo il caricamento dei dati
        data = de.get_data()
        fieldNames = de.get_fieldNames()
        defaultFieldNames = de.get_defaultFieldNames()
    
    progressivePrint("Loading Data", 0.05, end="")
    progressivePrint(" ...", 0.35)
    progressivePrint("Data Loaded Succesfully", 0.05)
    clearScreen()
    
    
    
    #! utilizzo del programma
    while True:
        print( "0. Exit" )
        print( "1. Insert a New Entry" )
        print( "2. Edit an Entry" )
        print( "3. Delete an Entry" )
        
        print( "4. Search for an Entry" )
        print( "5. Print All Entries" )
        
        print( "6. Add Field" )
        print( "7. Rename Field" )
        print( "8. Delete Field" )
        
        print( "9. Backup Data" )
        print( "10. Invalidate Data" )
        print( "11. Rate Safety of a Field Using \"zxcvbn\" Algorithm" )
        
        choice = input("Insert the Number of the Operation you want to Perfrom: ")
        
        
        
        #. exit
        if choice == "0":
            break
        
        #. insert a new entry
        elif choice == "1":
            print()
            add_entry_result = de.add_entry()
            print()
            if add_entry_result == "OK":
                print("Entry Added Successfully.")
                
                # salvo i dati
                save_data_result = de.save_data(key , pathOf_data)
                if save_data_result == "OK":
                    waitBeforeProceeding()
                    continue
                elif save_data_result == "FNF":
                    print("Data File Not found. Please Try Again.")
                    waitBeforeProceeding()
                    continue
                else:
                    print("An Unknown Error Occurred. Please Try Again.")
                    waitBeforeProceeding()
                    continue
                
            elif add_entry_result == "CANCELOP":
                print("Operation Cancelled Successfully.")
                waitBeforeProceeding()
                continue
            elif add_entry_result == "NULL":
                print("Entry Not Added (All Fields are Null).")
                waitBeforeProceeding()
                continue
            else:
                print("An Unknown Error Occurred. Please Try Again.")
                waitBeforeProceeding()
                continue
        
        
        
        #. edit an entry
        elif choice == "2":
            print()
            edit_entry_result = de.edit_entry()
            print()
            if edit_entry_result == "OK":
                print("Entry Edited Successfully.")
                
                # salvo i dati
                save_data_result = de.save_data(key , pathOf_data)
                if save_data_result == "OK":
                    waitBeforeProceeding()
                    continue
                elif save_data_result == "FNF":
                    print("Data File Not found. Please Try Again.")
                    waitBeforeProceeding()
                    continue
                else:
                    print("An Unknown Error Occurred. Please Try Again.")
                    waitBeforeProceeding()
                    continue
                
            elif edit_entry_result == "CANCELOP":
                print("Operation Cancelled Successfully.")
                waitBeforeProceeding()
                continue
            elif edit_entry_result == "NOEDIT":
                print("Entry Not Edited (No Fields were Modified).")
                waitBeforeProceeding()
                continue
            else:
                print("An Unknown Error Occurred. Please Try Again.")
                waitBeforeProceeding()
                continue
        
        
        
        #. delete an entry
        elif choice == "3":
            print()
            delete_entry_result = de.delete_entry()
            print()
            if delete_entry_result == "OK":
                print("Entry Deleted Successfully.")
                
                # salvo i dati
                save_data_result = de.save_data(key , pathOf_data)
                if save_data_result == "OK":
                    waitBeforeProceeding()
                    continue
                elif save_data_result == "FNF":
                    print("Data File Not found. Please Try Again.")
                    waitBeforeProceeding()
                    continue
                else:
                    print("An Unknown Error Occurred. Please Try Again.")
                    waitBeforeProceeding()
                    continue
                
            elif delete_entry_result == "CANCELOP":
                print("Operation Cancelled Successfully.")
                waitBeforeProceeding()
                continue
            else:
                print("An Unknown Error Occurred. Please Try Again.")
                waitBeforeProceeding()
                continue
        
        
        
        #. search for an entry
        elif choice == "4":
            search_entry_result = de.search_entry()
            print()
            if type(search_entry_result) == list and len(search_entry_result) > 0:
                printData(search_entry_result , printTotEntries=True , printPercentage=True)
                waitBeforeProceeding()
                continue
            elif type(search_entry_result) == list and len(search_entry_result) == 0:
                print("No Entries Found.")
                waitBeforeProceeding()
                continue
            elif search_entry_result == "CANCELOP":
                print("Operation Cancelled Successfully.")
                waitBeforeProceeding()
                continue
            else:
                print("An Unknown Error Occurred. Please Try Again.")
                waitBeforeProceeding()
                continue
        
        
        
        #. print all entries
        elif choice == "5":
            print()
            printData(data , printTotEntries=True , printPercentage=False)
            waitBeforeProceeding()
            continue
            
            
            
        #. add field
        elif choice == "6":
            print()
            add_field_result = de.add_field()
            print()
            if add_field_result == "OK":
                print("Field Added Successfully.")
                
                # salvo i dati
                save_data_result = de.save_data(key , pathOf_data)
                if save_data_result == "OK":
                    waitBeforeProceeding()
                    continue
                elif save_data_result == "FNF":
                    print("Data File Not found. Please Try Again.")
                    waitBeforeProceeding()
                    continue
                else:
                    print("An Unknown Error Occurred. Please Try Again.")
                    waitBeforeProceeding()
                    continue
                
            elif add_field_result == "CANCELOP":
                print("Operation Cancelled Successfully.")
                waitBeforeProceeding()
                continue
            else:
                print("An Unknown Error Occurred. Please Try Again.")
                waitBeforeProceeding()
                continue
        
        
        
        #. rename field
        elif choice == "7":
            print()
            rename_field_result = de.rename_field()
            print()
            if rename_field_result == "OK":
                print("Field Renamed Successfully.")
                
                # salvo i dati
                save_data_result = de.save_data(key , pathOf_data)
                if save_data_result == "OK":
                    waitBeforeProceeding()
                    continue
                elif save_data_result == "FNF":
                    print("Data File Not found. Please Try Again.")
                    waitBeforeProceeding()
                    continue
                else:
                    print("An Unknown Error Occurred. Please Try Again.")
                    waitBeforeProceeding()
                    continue
                
            elif rename_field_result == "CANCELOP":
                print("Operation Cancelled Successfully.")
                waitBeforeProceeding()
                continue
            else:
                print("An Unknown Error Occurred. Please Try Again.")
                waitBeforeProceeding()
                continue
        
        
        
        #. delete field
        elif choice == "8":
            print()
            remove_field_result = de.delete_field()
            print()
            if remove_field_result == "OK":
                print("Field Removed Successfully.")
                
                # salvo i dati
                save_data_result = de.save_data(key , pathOf_data)
                if save_data_result == "OK":
                    waitBeforeProceeding()
                    continue
                elif save_data_result == "FNF":
                    print("Data File Not found. Please Try Again.")
                    waitBeforeProceeding()
                    continue
                else:
                    print("An Unknown Error Occurred. Please Try Again.")
                    waitBeforeProceeding()
                    continue
                
            elif remove_field_result == "CANCELOP":
                print("Operation Cancelled Successfully.")
                waitBeforeProceeding()
                continue
            else:
                print("An Unknown Error Occurred. Please Try Again.")
                waitBeforeProceeding()
                continue
        
        
        
        #. backup data
        elif choice == "9":
            print()
            backup_data_result = de.backup_data(key)
            print()
            if backup_data_result == "OK":
                print("Data Backed Up Successfully.")
                waitBeforeProceeding()
                continue
            elif backup_data_result == "CANCELOP":
                print("Operation Cancelled Successfully.")
                waitBeforeProceeding()
                continue
            elif backup_data_result == "FNF":
                print("Backup File Not Found. Please Try Again.")
                waitBeforeProceeding()
                continue
            else:
                print("An Unknown Error Occurred. Please Try Again.")
                waitBeforeProceeding()
                continue
        
        
        
        #. invalidate data
        elif choice == "10":
            
            # chiedo conferma 2 volte
            print()
            while True:
                firstConfirmation = ("WARNING: This operation will invalidate the data and make it unreadable. This operation is irreversible. Are you sure you want to proceed? (Y/N)")
                if input(firstConfirmation).upper() != "Y":
                    break
                else:
                    firstConfirmation = True
                    
            if firstConfirmation == False:
                print("Operation Cancelled Successfully.")
                waitBeforeProceeding()
                continue
            
            print()
            while True:
                secondConfirmation = ("WARNING: This operation will invalidate the data and make it unreadable. This operation is irreversible. Are you sure you want to proceed? (Y/N)")
                if input(secondConfirmation).upper() != "Y":
                    break
                else:
                    secondConfirmation = True
                    
            if secondConfirmation == False:
                print("Operation Cancelled Successfully.")
                waitBeforeProceeding()
                continue
            
            invalidate_data_result = de.invalidate_data(pathOf_data)
            print()
            if invalidate_data_result == "OK":
                print("Data Invalidated Successfully.")
                progressivePrint("Farewell, Master", 0.05, end="")
                
                # salvo i dati
                save_data_result = de.save_data(key , pathOf_data)
                if save_data_result == "OK":
                    waitBeforeProceeding()
                    continue
                elif save_data_result == "FNF":
                    print("Data File Not found. Please Try Again.")
                    waitBeforeProceeding()
                    continue
                else:
                    print("An Unknown Error Occurred. Please Try Again.")
                    waitBeforeProceeding()
                    continue
                
            elif invalidate_data_result == "CANCELOP":
                print("Operation Cancelled Successfully.")
                waitBeforeProceeding()
                continue
            else:
                print("An Unknown Error Occurred. Please Try Again.")
                waitBeforeProceeding()
                continue
            
            
            
        #. rate safety
        elif choice == "11":    
            
            #. preparazione ed elaborazione
            # chiedo in input un campo
            print()
            while True:
                field = input("Enter the Field to Rate the Safety of: ")
                if field in defaultFieldNames:
                    print("Default Fields cannot be rated. Please Retry.")
                    continue
                elif field in fieldNames and field not in defaultFieldNames:
                    break
                else:
                    print("Invalid Field. Please Retry.")
                    continue
                
            # aggiungo il campo che conterrà il risultato
            fieldNames.insert(fieldNames.index(field) + 1 , "temp_safety")
            
            # riempio il campo di ciascuna entry con il risultato
            for entry in data:
                entry["temp_safety"] = zxcvbn.zxcvbn(entry[field])["score"]
                
            #. output
            # sorto i dati (in ordine crescente) in base al campo temporaneo
            data.sort(key=lambda x: x["temp_safety"])
            # stampo i risultati
            print()
            printData(data , printTotEntries=False , printPercentage=False)
            print()
            
            #. pulizia >>> ripristino l'ordine originale
            # rimuovo il campo temporaneo
            fieldNames.remove("temp_safety")
            for entry in data:
                entry.pop("temp_safety")
            data.sort(key=lambda x: x["ID"]) # sorto i dati (in ordine crescente) in base all'ID
                
            waitBeforeProceeding()


            
        else:
            print("Invalid Choice. Please Retry.")
            waitBeforeProceeding()
            continue
        
    
    clearScreen()
    progressivePrint("Exiting Program", 0.05, end="")
    progressivePrint(" ...", 0.35)
    return

        
                
if __name__ == "__main__":
    main()