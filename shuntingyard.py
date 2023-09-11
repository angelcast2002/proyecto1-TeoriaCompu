def shunting_yard(expresion_infija):
  
  precedencia = {'+':1, '*':2}
  salida = []
  pila_operadores = []

  for token in expresion_infija:

    if token.isalnum(): # operandos
      salida.append(token)
    
    elif token == '(':
      pila_operadores.append(token)

    elif token == ')':
      while pila_operadores[-1] != '(':
        salida.append(pila_operadores.pop())
      pila_operadores.pop() # quitar '('
    
    elif token in precedencia:
      while pila_operadores and precedencia[pila_operadores[-1]] >= precedencia[token]:
        salida.append(pila_operadores.pop())
      pila_operadores.append(token)

  # agregar operadores restantes
  while pila_operadores: 
    salida.append(pila_operadores.pop())

  return ''.join(salida)

expresion = input("Expresión infija: ")
print("Expresión postfija:", shunting_yard(expresion))