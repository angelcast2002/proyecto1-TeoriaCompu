def base(caracter):
    fragmento = []
    fragmento.append([0, caracter, 1, True])
    return fragmento

def concatenacion(fragmentoInicial, fragmentoFinal):
    fragmento = []
    esConcatenacion = False
    for i in range(len(fragmentoInicial)):
        fragmento.append(fragmentoInicial[i][:])
    for i in range(len(fragmentoFinal)):
        if 'ε' not in fragmentoFinal[i]:
            esConcatenacion = True
    if esConcatenacion:   
        valor = fragmento[-1][2]
        for i in range(len(fragmentoFinal)):
            if i == 0:
                fragmentoFinal[i][0] = valor
            else:
                fragmentoFinal[i][0] = fragmentoFinal[i - 1][-2]
            fragmentoFinal[i][2] = fragmentoFinal[i][0] + 1
        for i in range(len(fragmentoFinal)):
            fragmento.append(fragmentoFinal[i])
    else:
        pass
    for i in range(len(fragmento)):
        if i == len(fragmento) - 1:
            fragmento[i][-1] = True
        else:
            fragmento[i][-1] = False
    return fragmento

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

def afnToAfd(afn, caracteres):
    afd = []
    estadosAcepatadosAFN = []
    for i in range(len(afn)):
        if afn[i][-1] == True:
            estadosAcepatadosAFN.append(afn[i][-2])
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
            if newState != []:
                afdTransiciones.append([afd[i], caracteres[j], newState])
            if newState not in afd:
                afd.append(newState)
        i += 1
    
    for i in range(len(afdTransiciones)):
        afdTransiciones[i][0].sort()
        afdTransiciones[i][2].sort()

    estadosAcepatadosAFD = []
    for i in range(len(afdTransiciones)):
        for j in range(len(afdTransiciones[i][-1])):
            if afdTransiciones[i][-1][j] in estadosAcepatadosAFN:
                if afdTransiciones[i][0] not in estadosAcepatadosAFD:
                    estadosAcepatadosAFD.append(afdTransiciones[i][0])
                    if afdTransiciones[i][-1] not in estadosAcepatadosAFD:
                        estadosAcepatadosAFD.append(afdTransiciones[i][-1])
    
    return afdTransiciones, estadosAcepatadosAFD

def regexToCaracteres(regexp):
    caracteres = []
    for i in regexp:
        if i.isalnum() and i not in caracteres:
            caracteres.append(i)
    return caracteres

def main():
    # correcto
    # print(concatenacion(base('a'), concatenacion(base('a'), base('b'))))
    # incorrecto
    #print(concatenacion(base('a'), kleene(base('b'))))
    # incorrecto
    #print(concatenacion(base('a'), union(base('b'), base('c'))))
    operandos = []
    regexp = input("Expresión regular en notacion postfix: ")
    caracteres = regexToCaracteres(regexp)
    for i in range(len(regexp)):
        if regexp[i].isalnum():
            operandos.append(base(regexp[i]))
        elif regexp[i] == '+':
            operando2 = operandos.pop()
            operando1 = operandos.pop()
            operandos.append(union(operando1, operando2))
        elif regexp[i] == '.':
            operando2 = operandos.pop()
            operando1 = operandos.pop()
            operandos.append(concatenacion(operando1, operando2))
        elif regexp[i] == '*':
            operandos.append(kleene(operandos.pop()))

    print('AFN -->')
    print(operandos[0])

    with open('proyecto1-TeoriaCompu/afn.txt', 'w') as f:
        f.write(str(operandos[0]))
    
    afd, estadosAceptados = afnToAfd(operandos[0], caracteres)

    with open('proyecto1-TeoriaCompu/afd.txt', 'w') as d:
        d.write(str(afd))
        d.write('\n')
        d.write('Estados aceptados --> ')
        d.write(str(estadosAceptados))
    
    print('AFD -->')
    for i in range(len(afd)):
        print(afd[i])

    print('Estados aceptados -->', estadosAceptados)


if __name__ == "__main__":
    main()


"""parte1 = base('a')
parte2 = base('b')
parte3 = base('c')
parte4 = base('d')

parentesis = kleene(union(parte3, parte4))
concatenacion1 = concatenacion(parte4, parte3)

ejemplo = concatenacion(parentesis, parte4)
ejemplo = concatenacion(ejemplo, parte3)

#ejemplo = concatenacion(parentesis, concatenacion1)
caracteres = ['c', 'd']
afd, estadosAceptados = afnToAfd(ejemplo, caracteres)

print('AFD -->')
for i in range(len(afd)):
    print(afd[i])

print('Estados aceptados -->', estadosAceptados)"""
