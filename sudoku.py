def askvalues():
    l = []
    while len(l) < 9:
        texte = "Ligne " + str(len(l) + 1) + " : "
        t = input(texte)
        if len(t) == 9 and t.isdigit():
            ligne = list(map(int, t))
            if pas_doublons(l[:], ligne[:]):
                l.append(ligne)
            else:
                print("Valeurs répétées")
        else:
            print("Nombre ou type de valeurs incorrect")
    sud = [ [[l[i][j]] if l[i][j]>0 else [v for v in range(1, 10)] for j in range(9)] for i in range(9)]
    return sud

def pas_doublons(l, ligne):
    l.append(ligne[:]) #La liste en entier
    nbl = len(l) #Nombre de lignes

    
    ligne.sort() #La derniere ligne
    for i in range(8): #On verifie que la dernière ligne horizontale n'a pas de doublons
        if ligne[i]>0 and ligne[i]==ligne[i+1]:
            print("Test horizontal, valeur :", ligne[i])
            return False
    if nbl == 1: #Si on a une seule ligne, pas besoin de plus de vérifications
        return True

    
    for i in range(9): #On verifie que les lignes verticales n'ont pas de doublons
        temp = []
        for j in range(nbl):
            temp.append(l[j][i])
        temp.sort()
        for k in range(len(temp)-1):
            if temp[k] != 0 and temp[k]==temp[k+1]:
                print("Test vertical, ligne :", i, ", valeur :", temp[k])
                return False

    
    if nbl in (1, 4, 7): drl = 1 #Lignes du dernier triplet
    elif nbl in (2, 5, 8): drl = 2
    else: drl = 3
    if drl>1: #Si drl = 1 ou 2
        for i in range(3): # --- --- --- trois carres
            temp = []
            for j in range(3): # - - - un carre, longueur (3 valeurs)
                for k in range(drl): #Un carre, hauteur (drl valeurs)
                    temp.append(l[-(k+1)][3*i + j])
            temp.sort()
            for m in range(len(temp)-1):
                if temp[m] != 0 and temp[m]==temp[m+1]:
                    print("Test derniers carres, carre :", i, "valeur :", temp[m])
                    return False
    return True
                
        

def show(sud):
    for i in range(9):
        if i%3==0 : print(" _____________________   _____________________   _____________________")
        lignes = [list(" _ _ _   _ _ _   _ _ _   _ _ _   _ _ _   _ _ _   _ _ _   _ _ _   _ _ _") for i in range(3)]
        for j in range(9):
            for x in range(len(sud[i][j])):
                dec = 1 + (j*8) + (x%3)*2 #decalage
                lignes[x//3][dec] = str(sud[i][j][x])
        print(''.join(lignes[0]), ''.join(lignes[1]), ''.join(lignes[2]), " ", sep="\n")
