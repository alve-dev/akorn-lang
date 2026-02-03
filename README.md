# Akorn Programming Language (Akorn)

## Overview

**Akorn** is a programming language designed and implemented by a single developer with a strong appreciation for both **C** and **Python**. The primary objective of Akorn is to combine the best aspects of low-level and high-level programming: the performance and control of C with the expressiveness and productivity of Python.

In the long term, Akorn is intended to specialize in **Machine Learning** and **Robotics**, providing safe high-level abstractions by default while still allowing explicit low-level control when required.

---

## Language Design Goal

- Combine **low-level performance** with **high-level expressiveness**
- Static typing by default, with controlled flexibility
- Clear, readable syntax inspired by C and Python
- Explicit design decisions to avoid unnecessary verbosity
- First-class support for systems programming, ML, and robotics

---

## Core Language Characteristics

### Typing System

- **Static typing by default**
- Hybrid typing model using explicit keywords
- All type behavior is explicit and predictable
- `dynamic` is a keyword, not a type, and must be used intentionally

---

### Paradigm

- **Prototype (current):** Imperative
- **Planned official version (1.0):** Multi-paradigm

Akorn is designed for both **systems-level performance** and **data science agility**. It uses a **trait-based composition model**, eliminating classical inheritance overhead while preserving expressiveness and composability.

---

### Memory Management

- **High-level code:** Automatic memory management (Garbage Collection)
- **Low-level code:** Manual memory management (intended for robotics and systems use)
- Explicit boundaries between safe and unsafe contexts

---

### Object Model

- No classes
- Uses **structs + traits**
- Object access syntax similar to Python (`object.method()`)
- Minimal verbosity
- Structured and readable syntax inspired by C

---
## Variable Types

- `var`
  It is a mutable variable, meaning it can change in the code

- `let`
  It is an immutable variable, meaning it can only have one value given at the beginning, that is, a constant

## Data Types

### High-Level Core Types

- `int`  
  Signed 64-bit integer (default integer type)

- `bigint`  
  Arbitrary-precision signed integer

- `float`  
  Signed 64-bit floating-point number

- `bigfloat`  
  Arbitrary-precision floating-point number

- `decimal`  
  Arbitrary-precision decimal type (financial/scientific use)

- `string`  
  UTF-8 string type

- `bool`  
  Boolean (`true` / `false`)

- `array<T, S>`  
  Contiguous memory array with explicit element 
  T: Type 

- `dict<K, V, S>`  
  Dictionary similar to Python  
  - Keys must be static and homogeneous  
  - Values may be heterogeneous

- `tensor`  
  Planned type for Machine Learning (not finalized)

---

### Low-Level Core Types

- `int`  
  Same as high-level (`int64`)

- `int32`, `int16`, `int8`  
  Signed integers of specific sizes

- `uint32`, `uint16`, `uint8`  
  Unsigned integers

- `uint1`  
  1-bit integer (used to simulate booleans efficiently)

- `pointer`  
  Raw pointer type (`int*`, `char*`, `float*`-like)

- `char`  
  Single character

- `string`  
  Provided to avoid direct `pointer<char>` usage

- `array`  
  Fully homogeneous, non-contiguous memory array

---

## Basic Syntax

### Variable Declarations

```akorn
var int number = 10;
var float number_float = 10.5;

let bigint big_number = 10**500;
let bigfloat big_number_float = 10.5**500;

// Prefer basic int and float when possible

let string language_name = "Akorn";


let array<string> languages = ["Akorn", "C", "Python", "C++", "Rust"];

//This would be equivalent to a Python tuple, that is, an immutable contiguous memory array (hence let) of strings called languages

let dict<string, string> developers = {
    "Guido van Rossum": "Python",
    "Bjarne Stroustrup": "C++",
    "Graydon Hoare": "Rust",
    "Me": "Akorn",
};

// Just like above, since it has `let` it cannot change, it's an immutable dict, which has keys of strings and values ​​of strings, and is called developers

var bool in_development = True;
```
---

## Dynamic Variables

```akorn
// 'dynamic' is a keyword, not a type

var dynamic variable = "Hello, World"; //Note: `var` is mutable, `dynamic` can be of any type; if it were `let`, `dynamic` wouldn't make sense unless it's in prototyping.
variable = 2025;
variable = True;
```

Dynamic typing is allowed but discouraged unless necessary. It is useful for rapid prototyping but should be used responsibly.

```akorn
var array<dynamic> list = [1, 2, 3, "hello", "Alex", [1.5, 6.3]]; //This is equivalent to Python's `list`, an array with contiguous memory, mutable, and with dynamic values ​​inside, meaning more than one type.

var dict<string, dynamic> person = {
    "name":"Jonh Doe",
    "dni":"123456789",
    "children": 2,
    "married": True,
}; //Similarly, a mutable dictionary with a string key, dynamic values ​​(more than one type), and it's 'var' meaning it can change, or in other words, mutable like people; that's why it's a person dictionary.
```
> Dictionary keys must be static and homogeneous (e.g., all strings or all integers). Values may be 
> dynamic.

---

## Program Structure

### Hello World(Block Syntax)

```akorn
func main(void) -> int
{
    write("Hello World");
    return 0;
}
```
---

### Conditionals(Age Checker)

```akorn
func main(void) -> int
{
    let int age = readInt("Enter your age: ");
    
    if age < 0
    {
        write("Still in your mother's womb");
    }
    elif age >= 200
    {
        write("Inmortal vampire");
    }
    elif age >= 18
    {
        write("Adult");    
    }
    else
    {
        write("Minor");
    }

    return 0;
}
```
---

### Loops(Money, More Money)
```akorn
func main(void) -> Int
{
    var int money = 1;
    var string answer;

    loop //"loop" is a completely infinite loop, equivalent to "while true" or "while (true)".
    {
        write("You have", money, "dollars. Do you want to double it?");
        answer = readString("[Y/N]: ", limit=1).to_lower();

        if answer == 'y'
        {
            money *= 2;        
        }
        elif answer == 'n'
        {
            break;
        }
        else
        {
            suspiciousUser(); // just a joke =)
        }
    }
    
    return 0;
}
```
---

### Funtions(Factorial)
```akorn
func fact(int n) -> int
{
    var int product = 1;
    
    for i in 1..n
    {
        product *= i;
    }

    return product;
    // Recursive version exists, but iterative avoids stack overhead
}
```
---

## Identation-Based Syntax(Python-style)
Semicolons (`;`) are **optional but recommended.**
Akon supports both block-based `{}` syntax and identation-based syntax

### Hello World(Identation)
```akon
func main(void) -> int:
    write("Hello World")
    return 0
```
### Rules
- A `:` afther `if`, `func`, `for`, `while`, `loop`, etc. Enables identation-based blocks
- Identation without `:`**-> error**
- Using `:` together with `{}`**-> error**
- No `:` **->** `{}` is required
---

## Standard Library(Planned)
`stdio`
- `write()`
    Standard output with automatic newline
- `readString()`
    Read a string from input
- `readInt()`
    Read an integer
- `readFloat`
    Read a floating-point number
- `readPassword()`
    Secure string input (hidden typing)
  `readBool()`
    Reads a string and returns a bool depending on the condition given by the programmer
---

`stdlib`
- `len()`
    Length of arrays, strings, etc.
- `panic()`
    Terminate program with a critical error
- `exit()`
    Exit program normally
---

## Project Status
Akon is currently in an **early prototype stage**
The standard library is minimal, and the interpreter is still under development

This project is primaryly a **learning and experimentation effort**, with a long-term vision of becoming a
serious tool for robotics and machine learning
