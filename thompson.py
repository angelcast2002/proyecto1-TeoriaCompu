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
    
    kleene.append([kleene[-1][0], 'ε', len(kleene), True])

    kleene.append([0, 'ε', len(kleene) - 1, True])
    
    return kleene
    
def ultimoEstado(fragmento):
    max = 0
    for i in range(len(fragmento)):
        if fragmento[i][-2] > max:
            max = fragmento[i][-2]
    return max


parte1 = base('a')
parte2 = base('b')
parte3 = base('c')
parte4 = base('d')

#ejemplo = concatenacion(concatenacion(parte1, parte2), parte3)

#ejemplo = union(parte1, parte2)
#ejemplo = union(ejemplo, parte3)
# ejemplo = union(ejemplo, parte4)

#ejemplo = kleene(parte1)
#ejemplo = concatenacion(ejemplo, parte2)

# ejemplo1 = kleene(parte1)
# ejemplo1 = concatenacion(ejemplo1, parte2)

# ejemplo2 = kleene(parte3)
# ejemplo2 = concatenacion(ejemplo2, parte4)

# ejemplo = union(ejemplo1, ejemplo2)

ejemplo = union(kleene(concatenacion(parte1, parte2)), parte3)

print(ejemplo)

