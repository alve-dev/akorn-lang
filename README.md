# Akon Programming Language (Akon)

## Overview

**Akon** is a programming language designed and implemented by a single developer with a strong appreciation for both **C** and **Python**. The primary objective of Akon is to combine the best aspects of low-level and high-level programming: the performance and control of C with the expressiveness and productivity of Python.

In the long term, Akon is intended to specialize in **Machine Learning** and **Robotics**, providing safe high-level abstractions by default while still allowing explicit low-level control when required.

---

## Language Design Goals

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

Akon is designed for both **systems-level performance** and **data science agility**. It uses a **trait-based composition model**, eliminating classical inheritance overhead while preserving expressiveness and composability.

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
- Minimal verbosity (unlike Java)
- Structured and readable syntax inspired by C

---

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

- `array<T>`  
  Contiguous memory array with explicit element type

- `dict<K, V>`  
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

```akon
int number = 10;
float number_float = 10.5;

bigint big_number = 10**500;
bigfloat big_number_float = 10.5**500;

// Prefer basic int and float when possible

string language_name = "Akon";

array<string> languages = ["Akon", "C", "Python", "C++", "Rust"];

dict<string, string> developers = {
    "Guido van Rossum": "Python",
    "Bjarne Stroustrup": "C++",
    "Graydon Hoare": "Rust",
    "Me": "Akon",
};

bool in_development = true;
```
---

## Dynamic Variables

```akon
// 'dynamic' is a keyword, not a type

dynamic variable = "Hello, World";
variable = 2025;
variable = true;
```

Dynamic typing is allowed but discouraged unless necessary. It is useful for rapid prototyping but should be used responsibly.

```akon
array<dynamic> list = [1, 2, 3, "hello", "Alex", [1.5, 6.3]];

dict<string, dynamic> person = {
    "name":"Jonh Doe",
    "dni":"123456789",
    "children": 2,
    "married": true,
};
```
> Dictionary keys must be static and homogeneous (e.g., all strings or all integers). Values may be 
> dynamic.

---

## Program Structure

### Hello World(Block Syntax)

```akon
func main(void) -> int
{
    print("Hello World");
    return 0;
}
```
---

### Conditionals(Age Checker)

```akon
func main(void) -> int
{
    int gae = read_Int("Enter your age: ");
    
    if (age < 0)
    {
        print("Still in your mother's womb");
    }
    elif (age >= 200)
    {
        print("Inmortal vampire");
    }
    elif (age >= 18)
    {
        print("Adult");    
    }
    else
    {
        print("Minor");
    }

    return 0;
}
```
---

### Loops(Money, More Money)
```akon
func main(void) -> int
{
    int money = 1;

    while (true)
    {
        print("You have", money, "dollars. Do you want to double it?");
        string answer = readString("[Y/N]: ", limit=1).to_lower();

        if (answer == 'y')
        {
            money *= 2;        
        }
        elif (answer == 'n')
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
```akon
func fact(int n) -> int
{
    int product = 1;
    
    for (i in range(1, n + 1))
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
    print("Hello World")
    return 0
```
### Rules
- A `:` afther `if`, `func`, `for`, `while`, etc. Enables identation-based blocks
- Identation without `:`**-> error**
- Using `:` together with `{}`**-> error**
- No `:` **->** `{}` is required
---

## Standard Library(Planned)
`stdio`
- `print()`
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
- `range()`
    Fundamental for `for` loops; unable independenly

---

## Project Status
Akon is currently in an **early prototype stage**
The standard library is minimal, and the interpreter is still under development

This project is primaryly a **learning and experimentation effort**, with a long-term vision of becoming a
serious tool for robotics and machine learning
