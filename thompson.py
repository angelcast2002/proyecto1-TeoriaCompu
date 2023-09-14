def base(caracter):
    fragmento = []
    fragmento.append([0, caracter, 1, True])
    return fragmento

def concatenacion(fragmentoInicial, fragmentoFinal):
    fragmento = []
    for i in range(len(fragmentoInicial)):
        fragmento.append(fragmentoInicial[i][:])
    valor = fragmento[-1][2]
    for i in range(len(fragmentoFinal)):
        if i == 0:
            fragmentoFinal[i][0] = valor
        else:
            fragmentoFinal[i][0] = fragmentoFinal[i - 1][-2]
        fragmentoFinal[i][2] = fragmentoFinal[i][0] + 1
    for i in range(len(fragmentoFinal)):
        fragmento.append(fragmentoFinal[i])
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
        union.append(fragmento1[i][:])

    max = ultimoEstado(union)
    max += 1
    union.append([0, 'ε', max, False])

    for i in range(len(fragmento2)):
        fragmento2[i][0] += max
        fragmento2[i][2] += max
    
    for i in range(len(fragmento2)):
        union.append(fragmento2[i][:])

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

    fragmento = fragmento[:]
    fragmento.append([fragmento[-1][2], 'ε', fragmento[0][0], False])
    for i in range(len(fragmento)):
        fragmento[i][0] += 1
        fragmento[i][2] += 1
    
    for i in range(len(fragmento)):
        kleene.append(fragmento[i][:])
    
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

def transicion(afn, estado):
    trasiciones = []
    for i in range(len(estado)):
        trasiciones.append(estado[i])
    
    i = 0
    while i < len(afn):
        if (afn[i][0] == estado or afn[i][0] in trasiciones) and afn[i][1] == 'ε':
            if afn[i][-2] not in trasiciones: 
                trasiciones.append(afn[i][-2])
                i = 0
            
        i += 1
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
    afd.append(transicion(afn, [afn[0][0]]))
    afdTransiciones = []
    i = 0
    while i < len(afd):
        for j in range(len(caracteres)):
            estadosIniciales = []
            for k in range(len(afn)):
                if caracteres[j] == afn[k][1] and afn[k][0] in afd[i]:
                    estadosIniciales.append(afn[k][2])
            newState = transicion(afn, estadosIniciales)
            afdTransiciones.append([afd[i], caracteres[j], newState])
            if newState not in afd:
                afd.append(newState)
        i += 1
    for i in range(len(afdTransiciones)):
        afdTransiciones[i][0].sort()
        afdTransiciones[i][2].sort()
    
    return afdTransiciones

def regexToCaracteres(regexp):
    caracteres = []
    for i in regexp:
        if i.isalnum() and i not in caracteres:
            caracteres.append(i)
    return caracteres

def main():
   regexp = input("Expresión regular en notacion postfix: ")
   caracteres = regexToCaracteres(regexp)
   print("Caracteres: ", caracteres)

if __name__ == "__main__":
    main()


'''parte1 = base('a')
parte2 = base('b')
parte3 = base('c')
parte4 = base('d')

parentesis = kleene(union(parte3, parte4))
concatenacion1 = concatenacion(parte4, parte3)

ejemplo = concatenacion(parentesis, parte4)
ejemplo = concatenacion(ejemplo, parte3)

#ejemplo = concatenacion(parentesis, concatenacion1)

print(ejemplo)
caracteres = ['c', 'd']
afd = afnToAfd(ejemplo, caracteres)

for i in range(len(afd)):
    print(afd[i])'''
