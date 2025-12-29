**ADVERTENCIA** _Estas funciones solo son ideas_

---

# Funciones estandar de I/O

## Familia read(inputs)

---
### readString():

- **Descripcion**: Lee la entrada del usuario en CLI
- **Argumentos**: prompt:string, limit:int
- **Retorno**: input:string

#### Descripcion de argumentos:

- **prompt**: string que aparecera en la consola para el usuario
- **limit**: cantidad de caracteres permitidos, ejemplo 1, solo un caracter, si hay mas del limit se hace un bucle hasta que este en el limit

---
### readInt():

- **Descripcion**: Lee en la entrada del usuario en CLI con excepciones si no es un digito integer
- **Argumentos**: prompt:string, min:int, max:int
- **Retorno**: input:int

#### Descripcion de argumentos

- **prompt**: string que aparecera en la consola para el usuario
- **min**: el valor minimo permitido en la entrada, si el digito es de un valor menor a min se repite con feedback hasta que se digite un digito correcto
- **max**: el valor maximo permitido en la entrada, si el digito es de un valor mayor a max se repite con feedback hasta que se digite un digito correcto

---
### readFloat():

- **Descripcion**: Lee en la entrada de usuario en CLI con excepciones si no es un digito floating-point
- **Argumentos**: prompt:string, min:float, max:float
- **Retorno**: input:float

#### Descripcion de argumentos

- **prompt**: string que aparecera en la consola para el usuario
- **min**: el valor minimo permitido en la entrada, si el digito es de un valor menor a min se repite con feedback hasta que se digite un digito correcto
- **max**: el valor maximo permitido en la entrada, si el digito es de un valor mayor a max se repite con feedback hasta que se digite un digito correcto

---
### readPassword():

- **Descripcion**: Lee en la entrada de usuario en CLI
- **Argumentos**: prompt:string, mask:string = ''
- **Retorno**: input:string

#### Descripcion de argumentos

- **prompt**: string que aparecera en la consola para el usuario
- **mask**: la mascara que se mostrara en la consola, por defecto es '' osea que no se mostrara lo que se escribe en la consola

---
### readBool():

- **Descripcion**: Lee en la entrada de usuario en CLI
- **Argumentos**: prompt:string, true:string|array = 'Y', false:string|array = 'N'
- **Retorno**: input:bool

#### Descripcion de argumentos

- **prompt**: string que aparecera en la consola para el usuario
- **true**: caracter valido para que se retorne True
- **false**: caracter valido para que se retorne False

---
## Output

### write():

- **Descripcion**: imprime strings en consola
- **Argumentos**: prompt:string, end:string = '\n', sep:string = ' ' 
- **Retorno**: void

#### Descripcion de argumentos:

- **prompt**: texto que se imprimira
- **end**: string con el que termina el print, por defecto newline 
- **sep**: string que separa los argumentos de prompt, por defecto un espacio

---
