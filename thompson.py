def base(caracter):
    fragmento = []
    fragmento.append([0, caracter, 1, True])
    return fragmento

def concatenacion(fragmentoInicial, fragmentoFinal):
    fragmento = {}
    fragmento = fragmentoInicial
    fragmentoFinal[0][0] = fragmento[-1][-2]
    fragmentoFinal[-1][-2] = len(fragmento) + len(fragmentoFinal)
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

    union.append([0, 'ε', len(union)+1, False])

    for i in range(len(fragmento2)):
        fragmento2[i][0] += len(union)
        fragmento2[i][2] += len(union)
    
    for i in range(len(fragmento2)):
        union.append(fragmento2[i])

    union.append([fragmento1[-1][2], 'ε', len(union) + 1, True])
    union.append([fragmento2[-1][2], 'ε', len(union), True])

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
    
    kleene.append([kleene[-1][0], 'ε', len(kleene), True])

    kleene.append([0, 'ε', len(kleene) - 1, True])
    
    return kleene
    



parte1 = base('a')
parte2 = base('b')
parte3 = base('c')
parte4 = base('d')

# ejemplo = concatenacion(concatenacion(parte1, parte2), parte3)

ejemplo = union(parte1, parte2)
ejemplo = union(ejemplo, parte3)

# ejemplo = concatenacion(kleene1, concatenacion1)

print(ejemplo)

