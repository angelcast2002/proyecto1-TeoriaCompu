def base(caracter):
    fragmento = []
    fragmento.append([0, caracter, 1, True])
    return fragmento

def concatenacion(fragmentoInicial, fragmentoFinal):
    fragmento = []
    fragmento = fragmentoInicial
    fragmentoFinal[0][0] = fragmento[-1][-2]
    max = ultimoEstado(fragmento)
    fragmentoFinal[-1][-2] = max + 1
    fragmento = fragmento + fragmentoFinal
    for i in range(len(fragmento)):
        if i == len(fragmento) - 1:
            fragmento[i][-1] = True
        else:
            fragmento[i][-1] = False
    return fragmento

"""def union(fragmento1, fragmento2):
    union = []
    union.append([0, 'ε', 1, False])
    for i in range(len(fragmento1)):
        fragmento1[i][0] = union[-1][-2]
        fragmento1[i][2] = union[-1][-2] + 1
    
    union = union + fragmento1
    ultimoEstadoFrag1 = union[-1][-2]

    union.append([0, 'ε', union[-1][-2] + 1, False])

    for i in range(len(fragmento2)):
        fragmento2[i][0] = union[-1][-2]
        fragmento2[i][2] = union[-1][-2] + 1

    union = union + fragmento2
    ultimoEstadoFrag2 = union[-1][-2]

    largoSemiFinal = union[-1][-2]

    union.append([ultimoEstadoFrag1, 'ε', largoSemiFinal + 1, True])
    union.append([ultimoEstadoFrag2, 'ε', largoSemiFinal + 1, True])

    for i in range(len(union)):
        condicion = ultimoEstadoFrag1 == union[i][0] and largoSemiFinal + 1 == union[i][-2] or ultimoEstadoFrag2 == union[i][-2] and largoSemiFinal + 1 == union[i][-2]
        if condicion:
            union[i][-1] = True
        else:
            union[i][-1] = False

    
    return union"""

def union(fragmento1, fragmento2):
    union = []
    union.append([0, 'ε', 1, False])
    for i in range(len(fragmento1)):
        fragmento1[i][0] += 1
        fragmento1[i][2] += 1

    for i in range(len(fragmento1)):
        union.append(fragmento1[i])

    max = ultimoEstado(union)
    max += 1
    union.append([0, 'ε', max, False])

    for i in range(len(fragmento2)):
        fragmento2[i][0] += max
        fragmento2[i][2] += max
    
    for i in range(len(fragmento2)):
        union.append(fragmento2[i])

    max = ultimoEstado(union)
    max += 1

    union.append([fragmento1[-1][2], 'ε', max, True])
    union.append([fragmento2[-1][2], 'ε', max, True])

    for i in range(len(union)):
        if i == len(union) - 1 or i == len(union) - 2:
            union[i][-1] = True
        else:
            union[i][-1] = False

    return union

def kleene(fragmento):
    kleene = []
    kleene.append([0, 'ε', 1, False])

    fragmento.append([fragmento[-1][2], 'ε', fragmento[0][0], False])
    for i in range(len(fragmento)):
        fragmento[i][0] += 1
        fragmento[i][2] += 1
    
    for i in range(len(fragmento)):
        kleene.append(fragmento[i])
    
    max = ultimoEstado(kleene)
    
    kleene.append([kleene[-1][0], 'ε', max + 1, True])

    kleene.append([0, 'ε', max + 1, True])

    max = ultimoEstado(kleene)
    for i in range(len(kleene)):
        if max == kleene[i][2]:
            kleene[i][-1] = True
        else:
            kleene[i][-1] = False
    
    return kleene
    
def ultimoEstado(fragmento):
    max = 0
    for i in range(len(fragmento)):
        if fragmento[i][-2] > max:
            max = fragmento[i][-2]
    return max

def transicion(afn, estado, caracter):
    trasiciones = [estado]
    for i in range(len(afn)):
        if (afn[i][0] == estado or afn[i][0] in trasiciones) and afn[i][1] in caracter:
            if afn[i][-2] not in trasiciones: 
                trasiciones.append(afn[i][-2])
    if len(trasiciones) == 0:
        return None
    else:
        return trasiciones

'''
def transicion(afn, estado, caracter):
    transiciones = []
    for i in range(len(afn)):
        if afn[i][0] == estado and afn[i][1] in caracter:
            transiciones.append(afn[i][-2])
    if len(transiciones) == 0:
        return None
    else:
        return transiciones'''

def afnToAfd(afn, caracteres):
    afd = []
    afd.append(transicion(afn, afn[0][0], caracteres[0]))
    for i in range(len(caracteres)):
        newTransicion = transicion(afn, afn[0][0], ['ε',caracteres[i]])
        if newTransicion is not None and not newTransicion in afd:
            afd.append(newTransicion)
        elif newTransicion is None and not newTransicion in afd:
            afd.append(None)
    #for i in range(len(caracteres)):
    #    afd.append(transicion(afn, afn[0][0], caracteres[i]))
    return afd


parte1 = base('a')
parte2 = base('b')
parte3 = base('c')
parte4 = base('d')

parentesis = kleene(union(parte3, parte4))
#concatenacion1 = concatenacion(parte4, parte3)

# ejemplo = concatenacion(parentesis, concatenacion1)

print(parentesis)
caracteres = ['ε', 'a', 'b', 'c']
#print(afnToAfd(ejemplo, caracteres))
