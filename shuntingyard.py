def shuntingYard(re_str):
    precedence_map = {
        '(': 1,
        '+': 2,
        '.': 3,
        '*': 4,
    }
    
    output = []
    stack = []
    
    for char in re_str:
        if char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Pop '('
        elif char in precedence_map:
            while stack and precedence_map.get(stack[-1], 0) >= precedence_map[char]:
                output.append(stack.pop())
            stack.append(char)
        else:
            output.append(char)
    
    while stack:
        output.append(stack.pop())
    
    return ''.join(output)


def setConcatenaciones(regex):
    i = 0
    while i < len(regex):
        if i == 0:
            pass
        else:
            esAlfaNum = (regex[i].isalnum() or regex[i] == ':') and (regex[i - 1].isalnum() or regex[i - 1] == ':')
            esCerradura = (regex[i].isalnum() or regex[i] == '(' or regex[i] == ':') and regex[i - 1] == '*'
            esParentesisCierre = (regex[i].isalnum() or regex[i] == ':') and regex[i - 1] == ')'
            entreParentesis = regex[i] == '(' and regex[i - 1] == ')'
            esParentesisApertura2 = regex[i] == '(' and regex[i - 1] != regex[- 1] and regex[i - 1].isalnum()
            if regex[i - 2] != regex[- 1]:
                esParentesisApertura = (regex[i].isalnum() or regex[i] == ':') and regex[i - 1] == '(' and (regex[i - 2].isalnum() or regex[i - 2] == ':')
            else:
                esParentesisApertura = False
            
            if (esAlfaNum or esCerradura or esParentesisCierre or esParentesisApertura or entreParentesis or esParentesisApertura2):
                regex = regex[:i] + '.' + regex[i:]
                i = 0
        i += 1

    return regex

# Cadena Vacia = ':'
# Ejemplo de uso 
expresion_infija = input("Expresión en notación infija: ")
NewExpresion = setConcatenaciones(expresion_infija)
print(NewExpresion)
expresion_postfija = shuntingYard(NewExpresion)
print("Expresión en notación postfija:", expresion_postfija)
