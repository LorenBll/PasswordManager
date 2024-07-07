import os
import datetime
import encryption_engine as ee

try:
    import Levenshtein as lev
except ImportError:
    print("Module 'Levenshtein' not found. Install it with 'pip install Levenshtein'.")
    exit()
import hashlib


global fieldNames
fieldNames = []
global defaultFieldNames
defaultFieldNames = ["ID" , "creationDate" , "modificationDate" , "Notes"]
global data
data = []



def pathExists( path:str ) -> bool:
    return os.path.exists(path)

def isSimilar( s1:str , s2:str ) -> bool:
    # funzione che calcola la distanza di Levenshtein tra due stringhe
    
    maximumDistance = max(len(s1) , len(s2))
    
    if lev.distance(s1 , s2) < maximumDistance/2:
        return True
    return False



def load_data ( key:str , path:str="./data/data.txt" ) -> str:
    # funzione che carica i dati dal file
    
    global fieldNames
    global data
    
    if not pathExists(path):\
        return "FNF" # file not found
    
    try:
        with open( path , "r" ) as file:
            
            #. lettura dei nomi dei campi
            fieldNames = file.readline().split(";")
            
            if fieldNames[-1] == "\n":
                fieldNames.pop()
                
            # decifro i nomi dei campi
            for i in range(len(fieldNames)):
                fieldNames[i] = ee.decrypt(fieldNames[i] , key)
                
            #. lettura dei dati
            for line in file:
                
                # leggo i valori della entry
                values = line.split(";")
                if values[-1] == "\n":
                    values.pop()
                    
                # decifro i valori della entry  
                for i in range(len(values)):
                    values[i] = ee.decrypt(values[i] , key)
                    
                # creo un dizionario con i valori della entry e la memorizzo
                currentEntry = {}
                for i in range(len(fieldNames)):
                    currentEntry[fieldNames[i]] = values[i]
                data.append(currentEntry)
                
        # sposto il campo "ID" in prima posizione e ripeto l'operazione per le entry
        fieldNames.remove("ID")
        fieldNames.insert(0 , "ID")
        
        # sposto i campi "creationDate", "modificationDate" e "Notes" in fondo e ripeto l'operazione per le entry
        for currentDefaultFieldName in defaultFieldNames:
            if currentDefaultFieldName != "ID":
                fieldNames.remove(currentDefaultFieldName)
                fieldNames.append(currentDefaultFieldName)
            
        
        
    except Exception as e:
        print(e)
        exit() # unhandlable error
    
    return "OK" # success
    
    
    
def save_data ( key:str , path:str="./data/data.txt" ) -> str:
    # funzione che salva i dati nel file
    
    global fieldNames
    global data
    
    if not pathExists(path):
        return "FNF" # file not found
    
    # riordino i campi in modo che siano in ordine alfabetico, ripetendo l'operazione per le entry
    fieldNames.sort()
    for entry in data:
        entry = dict(sorted(entry.items())) 
        
    try:
        with open( path , "w" ) as file:
            
            #. scrittura dei nomi dei campi
            for i in range(len(fieldNames)):
                file.write(ee.encrypt(fieldNames[i] , key))
                if i < len(fieldNames)-1:
                    file.write(";")
            file.write("\n")
            
            #. scrittura dei dati
            for entry in data:
                for i in range(len(fieldNames)):
                    file.write(ee.encrypt(entry[fieldNames[i]] , key))
                    if i < len(fieldNames)-1:
                        file.write(";")
                file.write("\n")
                
    except Exception as e:
        print(e)
        exit() # unhandlable error
        
    return "OK" # success



def get_data () -> list:
    # funzione che restituisce i dati
    global data
    return data

def get_fieldNames () -> list:
    # funzione che restituisce i nomi dei campi
    global fieldNames
    return fieldNames

def get_defaultFieldNames () -> list:
    # funzione che restituisce i nomi dei campi di default
    global defaultFieldNames
    return defaultFieldNames



def add_entry () -> str:
    # funzione che aggiunge una entry ai dati
    
    global fieldNames
    global data
    
    #. inserimento entry
    newEntry = {}
    for currentFieldName in fieldNames:
        
        # genero l'ID dell'entry iterando su tutti gli ID già presenti e scegliendo il primo ID disponibile
        if currentFieldName == "ID":
            generatedID = 0
            for i in range(len(data)):
                if data[i]["ID"] == str(generatedID):
                    generatedID += 1
            newEntry["ID"] = str(generatedID)
            
        # scrivo la data di creazione dell'entry
        elif currentFieldName == "creationDate":
            newEntry["creationDate"] = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            continue
        
        # scrivo la data di modifica dell'entry
        elif currentFieldName == "modificationDate":
            newEntry["modificationDate"] = "NULL"
            continue
        
        # inserisco tutti gli altri campi
        else:
            inputBuffer = input("Insert " + currentFieldName + " (Type CANCELOP to Cancel Insertion): ")
            if inputBuffer == "" or inputBuffer == " ":
                inputBuffer = "NULL"
            elif inputBuffer == "CANCELOP":
                return "CANCELOP"
            newEntry[currentFieldName] = inputBuffer
            
    #. validazione entry
    isNull = True
    for currentFieldName in fieldNames:
        if currentFieldName in defaultFieldNames:
            continue
        if newEntry[currentFieldName] != "NULL":
            isNull = False
            break
        
    if isNull:
        return "NULL"
    
    #. aggiunta entry
    data.append(newEntry)
    
    return "OK" # success



def edit_entry () -> str:
    # funzione che modifica una entry
    
    global fieldNames
    global defaultFieldNames
    global data
    
    #. scelta dell'entry da modificare
    while True:
        entryID = input("Insert the ID of the entry to edit (Type CANCELOP to Cancel Edit): ")
        
        if entryID == "CANCELOP":
            return "CANCELOP"
        
        # controllo che l'ID sia valido
        isFound = False
        for i in range(len(data)):
            if data[i]["ID"] == entryID:
                isFound = True
                break
        if isFound:
            break
        else:
            print("Invalid Entry ID. Please Retry.")
            
    print()
            
    #. modifica entry
    toEditEntry = data[i]
    modificationCounter = 0
        
    for currentField in fieldNames:
        if currentField in defaultFieldNames and currentField != "Notes":
            continue
        inputBuffer = input("Insert the new value for " + currentField + " (Type CANCELOP to Cancel Edit, ENTER to keep \"" + toEditEntry[currentField] + "\"): ")
        if inputBuffer == "CANCELOP":
            return "CANCELOP"
        elif inputBuffer != "":
            toEditEntry[currentField] = inputBuffer
            modificationCounter += 1
            
    if modificationCounter == 0:
        return "NOEDIT"
        
    #. modifica data di modifica
    toEditEntry["modificationDate"] = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    return "OK" # success



def delete_entry () -> str:
    # funzione che elimina una entry chiedendo conferma
    
    global data
    
    #. scelta dell'entry da eliminare
    while True:
        entryID = input("Insert the ID of the entry to delete (Type CANCELOP to Cancel Deletion): ")
        
        if entryID == "CANCELOP":
            return "CANCELOP"
        
        # controllo che l'ID sia valido
        isFound = False
        for i in range(len(data)):
            if data[i]["ID"] == entryID:
                isFound = True
                break
        if isFound:
            break
        else:
            print("Invalid Entry ID. Please Retry.")
            
    #. conferma eliminazione
    while True:
        confirm = input("Are you Sure you Want to Delete the Entry? This Operation is Irreversibile. (Y/N): ")
        confirm = confirm.upper()
        if confirm == "Y":
            break
        elif confirm == "N":
            return "CANCELOP"
        else:
            print("Invalid Input. Please Retry.")
            
    #. eliminazione entry
    data.pop(i)
    return "OK" # success



def search_entry ():
    # funzione che cerca delle entry
    
    global fieldNames
    global data
    
    #. sottooperazioni di ricerca
    while True:
        print()
        print( "1) Search and Show Entries with String-Similar Inputted Value in Inputted Field" )  # ricerca per valore simile inserito in campo inserito
        print( "2) Search and Show Entries with String-Similar Inputted Value in Any Field" )       # ricerca per valore simile inserito in qualsiasi campo
        print( "3) Search and Show Entries with Same Inputted Value in Inputted Field" )            # ricerca per valore esatto inserito in campo inserito
        
        print( "4) Search and Show Entries with String-Similar Value in Inputted Field" )           # ricerca per valore simile in campo inserito
        print( "5) Search and Show Entries with Same Value in Inputted Field" )                     # ricerca per valore esatto ripetuto in campo inserito
        
        print( "6) Search and Show List of Entries Selected by ID" )                                # ricerca per ID
        
        inputBuffer = input("Choose the Search Operation (Type CANCELOP to Cancel Search): ")
        if inputBuffer == "CANCELOP":
            return "CANCELOP"
        elif inputBuffer == "1":
            return search_entries_bySimilarInsertedValue_inInsertedField()
        elif inputBuffer == "2":
            return search_entry_bySimilarInsertedValue_inAnyField()
        elif inputBuffer == "3":
            return search_entry_bySameInsertedValue_inInsertedField()
        elif inputBuffer == "4":
            return search_entries_bySimilarValue_inInsertedField()
        elif inputBuffer == "5":
            return search_entry_bySameValue_inInsertedField()
        elif inputBuffer == "6":
            return search_entry_byID()
        
        print("Invalid Input. Please Retry.")
        
def search_entries_bySimilarInsertedValue_inInsertedField ():
    # funzione che cerca delle entry con un valore simile in un campo specifico
    
    global fieldNames
    global data
    
    #. scelta del campo
    while True:
        
        inputBuffer = input("Insert the Field to Search in (Type CANCELOP to Cancel Search): ")
        if inputBuffer == "CANCELOP":
            return "CANCELOP"
        elif inputBuffer in fieldNames:
            break
        print("Invalid Field Name. Please Retry.")
    toSearchField = inputBuffer
            
    #. scelta del valore
    while True:
            
        inputBuffer = input("Insert the Value to Search for (Type CANCELOP to Cancel Search): ")
        if inputBuffer == "CANCELOP":
            return "CANCELOP"
        if inputBuffer != "":
            break
        
        print("Invalid Value. Please Retry.")
    toSearchValue = inputBuffer
        
    #. ricerca e visualizzazione delle entry
    searchResult = []
    for entry in data:
        if isSimilar(toSearchValue,entry[toSearchField]):
            searchResult.append(entry)
            
    return searchResult

def search_entry_bySimilarInsertedValue_inAnyField ():
    # funzione che cerca delle entry con un valore simile in qualsiasi campo
    
    global fieldNames
    global data
    
    #. scelta del valore
    while True:
            
        inputBuffer = input("Insert the Value to Search for (Type CANCELOP to Cancel Search): ")
        if inputBuffer == "CANCELOP":
            return "CANCELOP"
        if inputBuffer != "":
            break
        
        print("Invalid Value. Please Retry.")
        
    #. ricerca e visualizzazione delle entry
    searchResult = []
    for entry in data:
        for currentField in fieldNames:
            if currentField == "ID":
                continue
            if isSimilar(inputBuffer,entry[currentField]):
                searchResult.append(entry)
                break
            
    return searchResult

def search_entry_bySameInsertedValue_inInsertedField ():
    # funzione che cerca delle entry con un valore esatto in un campo specifico
    
    global fieldNames
    global data
    
    #. scelta del campo
    while True:
        
        inputBuffer = input("Insert the Field to Search in (Type CANCELOP to Cancel Search): ")
        if inputBuffer == "CANCELOP":
            return "CANCELOP"
        elif inputBuffer in fieldNames:
            break
        print("Invalid Field Name. Please Retry.")
    toSearchField = inputBuffer
            
    #. scelta del valore
    while True:
            
        inputBuffer = input("Insert the Value to Search for (Type CANCELOP to Cancel Search): ")
        if inputBuffer == "CANCELOP":
            return "CANCELOP"
        if inputBuffer != "":
            break
        
        print("Invalid Value. Please Retry.")
    toSearchValue = inputBuffer
        
    #. ricerca e visualizzazione delle entry
    searchResult = []
    for entry in data:
        if toSearchValue == entry[toSearchField]:
            searchResult.append(entry)
            
    return searchResult

def search_entries_bySimilarValue_inInsertedField ():
    # funzione che cerca delle entry con un valore simile in un campo specifico
    
    global fieldNames
    global data
    
    #. scelta del campo
    while True:
        
        inputBuffer = input("Insert the Field to Search in (Type CANCELOP to Cancel Search): ")
        if inputBuffer == "CANCELOP":
            return "CANCELOP"
        elif inputBuffer in fieldNames:
            break
        print("Invalid Field Name. Please Retry.")
    toSearchField = inputBuffer
            
    #. ricerca e visualizzazione delle entry
    searchResult = []
    for entry in data:
        if entry in searchResult:
            continue
        for entry2 in data:
            if entry2 in searchResult:
                continue
            if entry["ID"] == entry2["ID"]:
                continue
            if isSimilar(entry[toSearchField],entry2[toSearchField]):
                searchResult.append(entry)
                searchResult.append(entry2)
                
    return searchResult

def search_entry_bySameValue_inInsertedField ():
    # funzione che cerca delle entry con un valore ripetuto in un campo specifico
    
    global fieldNames
    global data
    
    #. scelta del campo
    while True:
            
        inputBuffer = input("Insert the Field to Search in (Type CANCELOP to Cancel Search): ")
        if inputBuffer == "CANCELOP":
            return "CANCELOP"
        elif inputBuffer in fieldNames:
            break
        print("Invalid Field Name. Please Retry.")
        
    #. ricerca e visualizzazione delle entry
    searchResult = []
    for entry in data:
        if entry in searchResult:
            continue
        for entry2 in data:
            if entry2 in searchResult:
                continue
            if entry["ID"] == entry2["ID"]:
                continue
            if entry[inputBuffer] == entry2[inputBuffer]:
                searchResult.append(entry)
                searchResult.append(entry2)
                
    return searchResult    

def search_entry_byID ():
    # funzione che cerca delle entry per ID
    
    global data
    
    #. scelta degli ID
    while True:
        
        inputBuffer = input("Insert the IDs of the Entries to Search for (Separate the IDs with a comma. Type CANCELOP to Cancel Search): ")
        if inputBuffer == "CANCELOP":
            return "CANCELOP"
        inputBuffer = inputBuffer.split(",")
        
        isFound = True
        wrongID = ""
        for currentID in inputBuffer:
            isFound = False
            for entry in data:
                if currentID == entry["ID"]:
                    isFound = True
                    break
            if not isFound:
                wrongID = currentID
                break
        if isFound:
            break
        print("Invalid ID Input (" + wrongID + "). Please Retry.")
        
    #. ricerca e visualizzazione delle entry
    searchResult = []
    for currentID in inputBuffer:
        for entry in data:
            if currentID == entry["ID"]:
                searchResult.append(entry)
                break
            
    return searchResult



def add_field () -> str:
    # funzione che aggiunge un campo ai dati
    
    global fieldNames
    global data
    
    #. inserimento campo
    while True:
        newField = input("Insert the New Field Name (Type CANCELOP to Cancel Insertion): ")
        
        if newField == "CANCELOP":
            return "CANCELOP"
        
        if newField in fieldNames:
            print("Field Already Exists. Please Retry.")
        elif "temp_" in newField:
            print("Field Name Cannot Start with \"temp_\". Please Retry.")
        else:
            break
            
    #. aggiunta campo
    fieldNames.append(newField)
    for entry in data:
        entry[newField] = "NULL"
        
    return "OK" # success



def rename_field () -> str:
    # funzione che rinomina un campo
    
    global fieldNames
    global data
    
    #. scelta del campo da rinominare
    while True:
        oldField = input("Insert the Field Name to Rename (Type CANCELOP to Cancel Renaming): ")
        
        if oldField == "CANCELOP":
            return "CANCELOP"
        
        if oldField in defaultFieldNames:
            print("Field is Default. Please Retry.")
        elif oldField not in fieldNames:
            print("Field Not Found. Please Retry.")
        else:
            break
        
    #. rinomina campo
    while True:
        newField = input("Insert the New Field Name (Type CANCELOP to Cancel Renaming): ")
        
        if newField == "CANCELOP":
            return "CANCELOP"
        
        if newField in fieldNames:
            print("Field Already Exists. Please Retry.")
        elif "temp_" in newField:
            print("Field Name Cannot Start with \"temp_\". Please Retry.")
        else:
            break
        
    for i in range(len(fieldNames)):
        if fieldNames[i] == oldField:
            fieldNames[i] = newField
            break
    for entry in data:
        entry[newField] = entry.pop(oldField)
        
    return "OK" # success



def delete_field () -> str:
    # funzione che elimina un campo
    
    global fieldNames
    global data
    
    #. scelta del campo da eliminare
    while True:
        field = input("Insert the Field Name to Delete (Type CANCELOP to Cancel Deletion): ")
        
        if field == "CANCELOP":
            return "CANCELOP"
        
        if field in defaultFieldNames:
            print("Field is Default. Please Retry.")
        elif field not in fieldNames:
            print("Field Not Found. Please Retry.")
        else:
            break
        
    #. eliminazione campo
    for i in range(len(fieldNames)):
        if fieldNames[i] == field:
            fieldNames.pop(i)
            break
    for entry in data:
        entry.pop(field)
        
    return "OK" # success



def backup_data ( key:str ) -> str:
    # funzione che crea un backup dei dati
    
    global fieldNames
    global data
    
    #. inserimento del percorso del backup
    while True:
        backupPath = input("Insert the Path of the Backup File (Type CANCELOP to Cancel Backup): ")
        
        if backupPath == "CANCELOP":
            return "CANCELOP"
        
        if pathExists(backupPath) and os.path.isfile(backupPath):
            overwrite = input("The File Already Exists. Do You Want to Overwrite it? (Y/N): ")
            overwrite = overwrite.upper()
            if overwrite == "Y":
                break
            elif overwrite == "N":
                continue
            else:
                print("Invalid Input. Please Retry.")
        elif pathExists(backupPath) and os.path.isdir(backupPath):
            print("Invalid Path (also Insert the Backup File Name). Please Retry.")
        else:
            break
        
    #. creazione del backup
    save_result = save_data(key , backupPath)
    if save_result == "OK":
        return "OK" # success
    else:
        return save_result # eventual error (file not found, unhandlable error)
    
    
    
def invalidate_data ( path:str ) -> str:
    # funzione che invalida i dati

    global fieldNames
    global data
    
    #. invalidazione dei dati
    # itero su tutte le entry e invalido i campi tranne con la loro versione hashata
    for field in fieldNames:
        for entry in data:
            entry[field] = hashlib.sha256(entry[field].encode()).hexdigest()
    for entry in data:
        for currentField in fieldNames:
            entry[currentField] = hashlib.sha256(entry[currentField].encode()).hexdigest()
            
    #. salvataggio dei dati invalidati
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    key = key.decode() # restituisco la chiave generata come stringa
    
    save_result = save_data(key , path)
    return save_result



def initialize_dataset () -> str:
    # funzione che inizializza i dati
    
    global fieldNames
    global defaultFieldNames
    global data
    
    #. chiedo dove salvare la chiave
    print()
    print("Welcome to the Password Manager Initialization Wizard.")
    print("You will be asked to choose a location to save the encryption key. It is recommended to save the key in an external device.")
    print("The key will be saved in a file named \"key.key\" in the indicated path.")
    
    while True:
        # input del file contenente la chiave
        keyPath = input("Enter the path where you want to save the encryption key: ")
        if pathExists(keyPath) and os.path.isdir(keyPath):    
            pass
        else:
            print("Invalid Path. Please try again.")
            continue
        
        # validazione della chiave
        if ee.get_key(keyPath + "/key.key") == "FNF":
            if keyPath[-1] == "/" or keyPath[-1] == "\\":
                keyPath = keyPath + "key.key"
            else:
                keyPath = keyPath + "/key.key"
            break
        else:
            print("A key already exists in the indicated path. Please choose another path.")
            continue
        
    #. genero la chiave
    key = ee.generate_key(keyPath)
    print("Key Generated Successfully in \"" + keyPath + "\".")
    print()
    
    #. chiedo dove salvare i dati
    print("Now you will be asked to choose a location to save the data.")
    print("It is recommended to save the data in a different location from the key.")
    print("The data will be saved in a file named \"data.dat\" in the indicated path. Press Enter to use the default path.")
    
    while True:
        # input del file contenente i dati
        pathOf_data = input("Enter the path where you want to save the data: ")
        if pathExists(pathOf_data) and os.path.isdir(pathOf_data):
            if pathOf_data[-1] == "/" or pathOf_data[-1] == "\\":
                pathOf_data = pathOf_data + "data.dat"
            else:
                pathOf_data = pathOf_data + "/data.dat"
            pass
        elif pathOf_data == "":
            pathOf_data = "./data/data.dat"
        else:
            print("Invalid Path. Please try again.")
            continue
        
        # validazione del percorso
        if pathExists(pathOf_data) == False:
            break
        else:
            print("A data file already exists in the indicated path. Please choose another path.")
            continue
        
    #. inizializzo i dati
    data = []
    fieldNames = defaultFieldNames.copy()
    fieldNames.append("Username")
    fieldNames.append("Password")
    
    # creo il file dei dati
    open(pathOf_data , "x").close()
    
    save_data_result = save_data(key , pathOf_data)
    if save_data_result == "OK":
        print("Data Initialized Successfully in \"" + pathOf_data + "\".")
        print("Restart the Program to Use the Password Manager.")
        exit()
    elif save_data_result == "FNF":
        print("An Error Occurred during Data Initialization. File Not Found.")
        exit()
    else:
        print("An Error Occurred during Data Initialization. Please Retry.")
        exit()



if __name__ == "__main__":
    print("This is a module, import it in your code to use it.")
    exit()