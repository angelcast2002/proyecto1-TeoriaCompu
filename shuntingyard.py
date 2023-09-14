def shunting_yard(expresion):
    precedencia = {'+': 2, '*': 1}
    salida = []
    pila_operadores = []
    utlimoToken = []
    
    for token in expresion:
        if token.isalnum() or token == 'ε':
            if utlimoToken and utlimoToken[-1].isalnum():
                salida.append(token)
                salida.append('.')
            else:
                salida.append(token)
        elif token in precedencia:
            while pila_operadores and pila_operadores[-1] in precedencia and precedencia[token] <= precedencia[pila_operadores[-1]]:
                salida.append(pila_operadores.pop())
            pila_operadores.append(token)
        elif token == '(':
            pila_operadores.append(token)
        elif token == ')':
            while pila_operadores and pila_operadores[-1] != '(':
                salida.append(pila_operadores.pop())
            if pila_operadores and pila_operadores[-1] == '(' and not len(pila_operadores) > 1 :
                salida.append(".")
                pila_operadores.pop()
            elif pila_operadores:
                pila_operadores.pop()
        utlimoToken.append(token)
    
    while pila_operadores:
        salida.append(pila_operadores.pop())
    
    return ''.join(salida)

# Ejemplo de uso
expresion_infija = input("Expresión en notación infija: ")
expresion_postfija = shunting_yard(expresion_infija)
print("Expresión en notación postfija:", expresion_postfija)
