from collections import defaultdict
import time
from graphviz import Digraph

abParentesis, cerrParentesis = '(', ')'
alfabeto = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + [chr(i) for i in range(ord('a'), ord('z') + 1)] + [chr(i) for i in range(ord('0'), ord('9') + 1)]
epsilon = 'ε'
kleene = '*'
union = '|'
concat = '·'

class Automata:
    def __init__(self, simbolo = set([])):
        self.estados = set()
        self.simbolo = simbolo    
        self.transiciones = defaultdict(defaultdict)
        self.estadoInicial = None
        self.estadosAceptados = []

    def iniciarAutomata(self, estado):
        self.estadoInicial = estado
        self.estados.add(estado)

    def aceptarEstado(self, estado):
        if isinstance(estado, int):
            estado = [estado]
        for s in estado:
            if s not in self.estadosAceptados:
                self.estadosAceptados.append(s)

    def crearTransicion(self, desdeEstado, haciaEstado, inputch):   
        if isinstance(inputch, str):
            inputch = set([inputch])
        self.estados.add(desdeEstado)
        self.estados.add(haciaEstado)
        if desdeEstado in self.transiciones and haciaEstado in self.transiciones[desdeEstado]:
            self.transiciones[desdeEstado][haciaEstado] = self.transiciones[desdeEstado][haciaEstado].union(inputch)
        else:
            self.transiciones[desdeEstado][haciaEstado] = inputch

    def guardarTransiciones(self, transiciones):  
        for desdeEstado, haciaEstados in transiciones.items():
            for estado in haciaEstados:
                self.crearTransicion(desdeEstado, estado, haciaEstados[estado])

    def actualizarEstados(self, startnum):
        translations = {}
        for i in self.estados:
            translations[i] = startnum
            startnum += 1
        actualizar = Automata(self.simbolo) # nuevo automata con mismos simbolos
        actualizar.iniciarAutomata(translations[self.estadoInicial]) # nuevo estado inicial
        actualizar.aceptarEstado(translations[self.estadosAceptados[0]]) # nuevo estado aceptado
        
        for desdeEstado, haciaEstados in self.transiciones.items():
            for estado in haciaEstados:
                actualizar.crearTransicion(translations[desdeEstado], translations[estado], haciaEstados[estado])
        return [actualizar, startnum]

    def actualizarEstadosIguales(self, equivalent, pos):
        actualizar = Automata(self.simbolo)
        for desdeEstado, haciaEstados in self.transiciones.items():
            for estado in haciaEstados:
                actualizar.crearTransicion(pos[desdeEstado], pos[estado], haciaEstados[estado])
        actualizar.iniciarAutomata(pos[self.estadoInicial])
        for s in self.estadosAceptados:
            actualizar.aceptarEstado(pos[s])
        return actualizar

    def cerraduraEpsilon(self, findstate):
        allEstados = set()
        estados = [findstate]
        while len(estados):
            estado = estados.pop()
            allEstados.add(estado)
            if estado in self.transiciones:
                for tos in self.transiciones[estado]:
                    if epsilon in self.transiciones[estado][tos] and \
                        tos not in allEstados:
                        estados.append(tos)
        return allEstados

    def getMovimiento(self, estado, skey):
        if isinstance(estado, int):
            estado = [estado]
        trstates = set()
        for st in estado:
            if st in self.transiciones:
                for tns in self.transiciones[st]:
                    if skey in self.transiciones[st][tns]:
                        trstates.add(tns)
        return trstates

    def display(self, fname, pname):
        fa = Digraph(pname, filename = fname, format = 'png')
        fa.attr(rankdir='LR')

        fa.attr('node', shape = 'doublecircle')
        for fst in self.estadosAceptados:
            fa.node('s' + str(fst))

        fa.attr('node', shape = 'circle')
        for desdeEstado, haciaEstados in self.transiciones.items():
            for estado in haciaEstados:
                tmp = ''
                for s in haciaEstados[estado]:
                    tmp += s + '|'
                fa.edge('s' + str(desdeEstado), 's' + str(estado), label = tmp[:-1])

        fa.attr('node', shape = 'point')
        fa.edge('', 's' + str(self.estadoInicial))

        fa.view()

class RegexToNFA:

    def __init__(self, regex):
        self.regex = regex
        self.crearNFA()

    @staticmethod
    def compPrecedencia(op):
        if op == union:
            return 1
        elif op == concat:
            return 2
        elif op == kleene:
            return 3
        else:       
            return 0

    @staticmethod
    def handleSimbolo(inputch):   
        primerEstado = 1
        siguienteEstado = 2
        basic = Automata(set([inputch]))
        basic.iniciarAutomata(primerEstado)
        basic.aceptarEstado(siguienteEstado)
        basic.crearTransicion(primerEstado, siguienteEstado, inputch)
        return basic

    @staticmethod
    def handleUnion(a, b):   
        [a, m1] = a.actualizarEstados(2)
        [b, m2] = b.actualizarEstados(m1)
        primerEstado = 1
        siguienteEstado = m2
        unionFA = Automata(a.simbolo.union(b.simbolo))
        unionFA.iniciarAutomata(primerEstado)
        unionFA.aceptarEstado(siguienteEstado)
        unionFA.crearTransicion(unionFA.estadoInicial, a.estadoInicial, epsilon)
        unionFA.crearTransicion(unionFA.estadoInicial, b.estadoInicial, epsilon)
        unionFA.crearTransicion(a.estadosAceptados[0], unionFA.estadosAceptados[0], epsilon)
        unionFA.crearTransicion(b.estadosAceptados[0], unionFA.estadosAceptados[0], epsilon)
        unionFA.guardarTransiciones(a.transiciones)
        unionFA.guardarTransiciones(b.transiciones)
        return unionFA

    @staticmethod
    def handleConcat(a, b):    
        [a, m1] = a.actualizarEstados(1)
        [b, m2] = b.actualizarEstados(m1)
        primerEstado = 1
        siguienteEstado = m2 - 1
        concatFA = Automata(a.simbolo.union(b.simbolo))
        concatFA.iniciarAutomata(primerEstado)
        concatFA.aceptarEstado(siguienteEstado)
        concatFA.crearTransicion(a.estadosAceptados[0], b.estadoInicial, epsilon)
        concatFA.guardarTransiciones(a.transiciones)
        concatFA.guardarTransiciones(b.transiciones)
        return concatFA

    @staticmethod
    def handleKleene(a):  
        [a, m1] = a.actualizarEstados(2)
        primerEstado = 1
        siguienteEstado = m1
        kleeneFA = Automata(a.simbolo)
        kleeneFA.iniciarAutomata(primerEstado)
        kleeneFA.aceptarEstado(siguienteEstado)
        kleeneFA.crearTransicion(kleeneFA.estadoInicial, a.estadoInicial, epsilon)
        kleeneFA.crearTransicion(kleeneFA.estadoInicial, kleeneFA.estadosAceptados[0], epsilon)
        kleeneFA.crearTransicion(a.estadosAceptados[0], kleeneFA.estadosAceptados[0], epsilon)
        kleeneFA.crearTransicion(a.estadosAceptados[0], a.estadoInicial, epsilon)
        kleeneFA.guardarTransiciones(a.transiciones)
        return kleeneFA

    def crearNFA(self):
        temp = ''
        prev = ''
        simbolo = set()

        # Procesar el regex
        for ch in self.regex:
            if ch in alfabeto:
                simbolo.add(ch)
            if ch in alfabeto or ch == abParentesis:
                if prev != concat and (prev in alfabeto or prev in [kleene, cerrParentesis]): 
                    temp += concat
            temp += ch
            prev = ch
        self.regex = temp

        # Convertir a postfix
        temp = ''
        stack = []
        for ch in self.regex:
            if ch in alfabeto:
                temp += ch 
            elif ch == abParentesis:
                stack.append(ch) 
            elif ch == cerrParentesis:
                while(stack[-1] != abParentesis):
                    temp += stack[-1]
                    stack.pop()
                stack.pop()    
            else:
                while(len(stack) and RegexToNFA.compPrecedencia(stack[-1]) >= RegexToNFA.compPrecedencia(ch)):
                    temp += stack[-1]
                    stack.pop()
                stack.append(ch) 
        while(len(stack) > 0):
            temp += stack.pop() 
        self.regex = temp

        # Construir NFA
        self.automata = []
        for ch in self.regex:
            if ch in alfabeto:
                self.automata.append(RegexToNFA.handleSimbolo(ch)) 
            elif ch == union:
                b = self.automata.pop()
                a = self.automata.pop()
                self.automata.append(RegexToNFA.handleUnion(a, b)) 
            elif ch == concat:
                b = self.automata.pop()
                a = self.automata.pop()
                self.automata.append(RegexToNFA.handleConcat(a, b))
            elif ch == kleene:
                a = self.automata.pop()
                self.automata.append(RegexToNFA.handleKleene(a))
        self.nfa = self.automata.pop()
        self.nfa.simbolo = simbolo

    def AnalysisNFA(self, string):
        print('\n------------\nSimulacion de NFA')
        start_time = time.time()
        string = string.replace('@', epsilon)
        curst = self.nfa.estadoInicial
        curst = self.nfa.cerraduraEpsilon(curst)

        for ch in string:
            if ch == epsilon:
                continue
            st = self.nfa.getMovimiento(curst, ch)
            print(f"Estados de la cerradura: {st}, Simbolo de entrada: {ch}, Siguiente estado: {st}")
            curst = set()
            for s in st:
                curst = curst.union(self.nfa.cerraduraEpsilon(s))
            print(f"Estados de la cerradura: {curst}, Simbolo de entrada: {epsilon}, Siguiente estado: {curst}")
        if len(curst.intersection(self.nfa.estadosAceptados)):
            print(f"\nCadena '{string}' aceptada.")
        else:
            print(f"\nCadena '{string}' no aceptada. Se detiene en el estado {curst}.")
        elapsed_time = time.time() - start_time
        print(f"Tiempo transcurrido de simulacion: {elapsed_time} segundos\n")
        return len(curst.intersection(self.nfa.estadosAceptados))


    def mostrarNFA(self):
        self.nfa.display('nfa.gv', 'nondeterministic_finite_state_machine')

class NFAToDFA:

    def __init__(self, nfa):
        self.construirDFA(nfa)

    def mostrarDFA(self):
        self.dfa.display('dfa.gv', 'deterministic_finite_state_machine')

    def mostrarMinDFA(self):
        self.minDFA.display('mindfa.gv', 'min_deterministic_finite_state_machine')

    def construirDFA(self, nfa):    
        allEstados = dict()  
        ecerradura = dict()   
        primerEstado = nfa.cerraduraEpsilon(nfa.estadoInicial)
        ecerradura[nfa.estadoInicial] = primerEstado
        cnt = 1 
        dfa = Automata(nfa.simbolo)
        dfa.iniciarAutomata(cnt)
        estados = [[primerEstado, dfa.estadoInicial]] 
        allEstados[cnt] = primerEstado
        cnt += 1
        while len(estados):
            [state, desdeIndex] = estados.pop()
            for ch in dfa.simbolo:
                trstates = nfa.getMovimiento(state, ch)
                for s in list(trstates):    
                    if s not in ecerradura:
                        ecerradura[s] = nfa.cerraduraEpsilon(s)
                    trstates = trstates.union(ecerradura[s])
                if len(trstates):
                    if trstates not in allEstados.values():
                        estados.append([trstates, cnt])
                        allEstados[cnt] = trstates
                        haciaIndex = cnt
                        cnt += 1
                    else:
                        haciaIndex = [k for k, v in allEstados.items() if v  ==  trstates][0]
                    dfa.crearTransicion(desdeIndex, haciaIndex, ch)
            for value, state in allEstados.items():
                if nfa.estadosAceptados[0] in state:
                    dfa.aceptarEstado(value)
            self.dfa = dfa

    @staticmethod
    def estadoRepetido(estados, pos):  
        cnt = 1
        change = dict()
        for st in estados:
            if pos[st] not in change:
                change[pos[st]] = cnt
                cnt += 1
            pos[st] = change[pos[st]]

    def minimizar(self): 
        estados = list(self.dfa.estados)
        haciaestado = dict(set()) 

        
        for st in estados:
            for sy in self.dfa.simbolo:
                if st in haciaestado:
                    if sy in haciaestado[st]:
                        haciaestado[st][sy] = haciaestado[st][sy].union(self.dfa.getMovimiento(st, sy))
                    else:
                        haciaestado[st][sy] = self.dfa.getMovimiento(st, sy)
                else:
                    haciaestado[st] = {sy : self.dfa.getMovimiento(st, sy)}
                if len(haciaestado[st][sy]):
                    haciaestado[st][sy] = haciaestado[st][sy].pop()
                else:
                    haciaestado[st][sy] = 0

        equal = dict()  
        pos = dict()    

        
        equal = {1: set(), 2: set()}
        for st in estados:
            if st not in self.dfa.estadosAceptados:
                equal[1] = equal[1].union(set([st]))
                pos[st] = 1
        for fst in self.dfa.estadosAceptados:
            equal[2] = equal[2].union(set([fst]))
            pos[fst] = 2

        sinCheck = []
        cnt = 3 
        sinCheck.extend([[equal[1], 1], [equal[2], 2]])
        while len(sinCheck):
            [equalst, id] = sinCheck.pop()
            for sy in self.dfa.simbolo:
                diff = dict()
                for st in equalst:
                    if haciaestado[st][sy] == 0:
                        if 0 in diff:
                            diff[0].add(st)
                        else:
                            diff[0] = set([st])
                    else:
                        if pos[haciaestado[st][sy]] in diff:
                            diff[pos[haciaestado[st][sy]]].add(st)
                        else:
                            diff[pos[haciaestado[st][sy]]] = set([st])
                if len(diff) > 1:
                    for k, v in diff.items():
                        if k:
                            for i in v:
                                equal[id].remove(i)
                                if cnt in equal:
                                    equal[cnt] = equal[cnt].union(set([i]))
                                else:
                                    equal[cnt] = set([i])
                            if len(equal[id]) == 0:
                                equal.pop(id)
                            for i in v:
                                pos[i] = cnt
                            sinCheck.append([equal[cnt], cnt])
                            cnt += 1
                    break
        if len(equal) == len(estados):
            self.minDFA = self.dfa
        else:
            NFAToDFA.estadoRepetido(estados, pos)
            self.minDFA = self.dfa.actualizarEstadosIguales(equal, pos)

    def Analysis(self, string):
        print("------------\nSimulacion de DFA")
        start_time = time.time()
        string = string.replace('@', epsilon)
        curst = self.dfa.estadoInicial
        for ch in string:
            if ch == epsilon:
                continue
            st = list(self.dfa.getMovimiento(curst, ch))
            if len(st) == 0:
                print(f"Cadena '{string}' no aceptada. Se traba en el estado {curst} con la entrada '{ch}'")
                elapsed_time = time.time() - start_time
                print(f"Tiempo transcurrido: {elapsed_time} segundos")
                return False
            next_state = st[0]
            print(f"Estado actual: {curst}, Simbolo de entrada: {ch}, Siguiente estado: {next_state}")
            curst = next_state
        if curst in self.dfa.estadosAceptados:
            print(f"\nCadena '{string}' aceptada.")
        else:
            print(f"\nCadena '{string}' no aceptada. Se detiene en el estado {curst}.")
        elapsed_time = time.time() - start_time
        print(f"Tiempo transcurrido de simulacion: {elapsed_time} segundos\n")
        return curst in self.dfa.estadosAceptados


    def AnalysisMinimizedDFA(self, string):
        print("------------\nSimulacion de Minimized DFA")
        start_time = time.time()
        string = string.replace('@', epsilon)
        curst = self.minDFA.estadoInicial
        for ch in string:
            if ch == epsilon:
                continue
            st = list(self.minDFA.getMovimiento(curst, ch))
            if len(st) == 0:
                print(f"Cadena '{string}' no aceptada. Se traba en el estado {curst} con la entrada '{ch}'")
                elapsed_time = time.time() - start_time
                print(f"Tiempo transcurrido: {elapsed_time} segundos")
                return False
            next_state = st[0]
            print(f"Estado actual: {curst}, Simbolo de entrada: {ch}, Siguiente estado: {next_state}")
            curst = next_state
        if curst in self.minDFA.estadosAceptados:
            print(f"\nCadena '{string}' aceptada.")
        else:
            print(f"\nCadena '{string}' no aceptada. Se detiene en el estado {curst}.")
        elapsed_time = time.time() - start_time
        print(f"Tiempo transcurrido de simulacion: {elapsed_time} segundos\n")
        return curst in self.minDFA.estadosAceptados

def write_to_file(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(data)

if __name__ == '__main__':
    regex = input('Ingrese la regex: ')
    a = RegexToNFA(regex)
    a.mostrarNFA()

    b = NFAToDFA(a.nfa)
    b.mostrarDFA()
    b.minimizar()
    b.mostrarMinDFA()
    
    nfa_data = ""
    nfa_data += f"ESTADOS: {{{', '.join(map(str, a.nfa.estados))}}}\n"
    nfa_data += f"SIMBOLOS: {{{', '.join(map(str, a.nfa.simbolo))}}}\n"
    nfa_data += f"ESTADO INICIAL: {{{a.nfa.estadoInicial}}}\n"
    nfa_data += f"ESTADOS DE ACEPTACION: {{{', '.join(map(str, a.nfa.estadosAceptados))}}}\n"
    transiciones = [f"({desde_estado}, {simbolo}, {hacia_estado})" for desde_estado, simboloTranscion in a.nfa.transiciones.items() for simbolo, hacia_estado in simboloTranscion.items()]
    nfa_data += f"TRANSICIONES: {{{', '.join(transiciones)}}}"
    write_to_file('nfa.txt', nfa_data)

    dfa_data = ""
    dfa_data += f"ESTADOS: {{{', '.join(map(str, b.dfa.estados))}}}\n"
    dfa_data += f"SIMBOLOS: {{{', '.join(map(str, b.dfa.simbolo))}}}\n"
    dfa_data += f"ESTADO INICIAL: {{{b.dfa.estadoInicial}}}\n"
    dfa_data += f"ESTADOS DE ACEPTACION: {{{', '.join(map(str, b.dfa.estadosAceptados))}}}\n"
    transiciones = [f"({desde_estado}, {simbolo}, {hacia_estado})" for desde_estado, simboloTranscion in b.dfa.transiciones.items() for simbolo, hacia_estado in simboloTranscion.items()]
    dfa_data += f"TRANSICIONES: {{{', '.join(transiciones)}}}\n"
    write_to_file('dfa.txt', dfa_data)
    
    min_dfa_data = ""
    min_dfa_data += f"ESTADOS: {{{', '.join(map(str, b.minDFA.estados))}}}\n"
    min_dfa_data += f"SIMBOLOS: {{{', '.join(map(str, b.minDFA.simbolo))}}}\n"
    min_dfa_data += f"ESTADO INICIAL: {{{b.minDFA.estadoInicial}}}\n"
    min_dfa_data += f"ESTADOS DE ACEPTACION: {{{', '.join(map(str, b.minDFA.estadosAceptados))}}}\n"
    transiciones = [f"({desde_estado}, {simbolo}, {hacia_estado})" for desde_estado, simboloTranscion in b.minDFA.transiciones.items() for simbolo, hacia_estado in simboloTranscion.items()]
    min_dfa_data += f"TRANSICIONES: {{{', '.join(transiciones)}}}\n"
    write_to_file('min_dfa.txt', min_dfa_data)

    while True:
        try:
            s = input('Ingrese una cadena para ver si es aceptada o no: ')
            if a.AnalysisNFA(s):
                print('Aceptada por NFA\n')
            else:
                print('No aceptada por NFA\n')
            if b.Analysis(s):
                print('Aceptada por DFA\n')
            else:
                print('No aceptada por DFA\n')
            if b.AnalysisMinimizedDFA(s):
                print('Aceptada por Minimized DFA\n')
            else:
                print('No aceptada por Minimized DFA\n')
        except EOFError:
            break
