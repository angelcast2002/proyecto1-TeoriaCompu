from collections import defaultdict
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
        state1 = 1
        state2 = 2
        basic = Automata(set([inputch]))
        basic.iniciarAutomata(state1)
        basic.aceptarEstado(state2)
        basic.crearTransicion(state1, state2, inputch)
        return basic

    @staticmethod
    def handleUnion(a, b):   
        [a, m1] = a.actualizarEstados(2)
        [b, m2] = b.actualizarEstados(m1)
        state1 = 1
        state2 = m2
        unionFA = Automata(a.simbolo.union(b.simbolo))
        unionFA.iniciarAutomata(state1)
        unionFA.aceptarEstado(state2)
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
        state1 = 1
        state2 = m2 - 1
        concatFA = Automata(a.simbolo.union(b.simbolo))
        concatFA.iniciarAutomata(state1)
        concatFA.aceptarEstado(state2)
        concatFA.crearTransicion(a.estadosAceptados[0], b.estadoInicial, epsilon)
        concatFA.guardarTransiciones(a.transiciones)
        concatFA.guardarTransiciones(b.transiciones)
        return concatFA

    @staticmethod
    def handleKleene(a):  
        [a, m1] = a.actualizarEstados(2)
        state1 = 1
        state2 = m1
        kleeneFA = Automata(a.simbolo)
        kleeneFA.iniciarAutomata(state1)
        kleeneFA.aceptarEstado(state2)
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

    def mostrarNFA(self):
        self.nfa.display('nfa.gv', 'automata_finito_no_determinista')


def write_to_file(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(data)

if __name__ == '__main__':
    regex = input('Ingrese la regex: ')
    a = RegexToNFA(regex)
    a.mostrarNFA()
    
    nfa_data = ""
    nfa_data += f"ESTADOS: {{{', '.join(map(str, a.nfa.estados))}}}\n"
    nfa_data += f"SIMBOLOS: {{{', '.join(map(str, a.nfa.simbolo))}}}\n"
    nfa_data += f"ESTADO INICIAL: {{{a.nfa.estadoInicial}}}\n"
    nfa_data += f"ESTADOS DE ACEPTACION: {{{', '.join(map(str, a.nfa.estadosAceptados))}}}\n"
    transiciones = [f"({desde_estado}, {simbolo}, {hacia_estado})" for desde_estado, simboloTransicion in a.nfa.transiciones.items() for simbolo, hacia_estado in simboloTransicion.items()]
    nfa_data += f"TRANSICIONES: {{{', '.join(transiciones)}}}"
    write_to_file('nfa.txt', nfa_data)
