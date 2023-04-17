# CS515 Project 2: Calculator Language
Yetong Chen ychen12@stevens.edu
Honglin Qin hqin4@stevens.edu

A standard expression calculator used on the command-line.

## Github repo
https://github.com/ForrestQin/Calculator_Language

## Time
We spent about 20 hours on the project in total.

## Test 
Run `python3 test.py` to test the code.

We tested our code using the `unittest` and `io` modules in Python. The test input is in the `test_input.txt` file, and the expected output is in the `test_output.txt` file.

## Bugs or issues
Most of the bugs we encounter are related to precedence and reporting errors. We faced difficulties in resolving the `test #14 on error.03` bug until the end.

## Resolved issue
We adjusted the order of the calculations during the parsing process. We found the error by running the program step by step.

For `parse error`, we report an error as soon as we find it during the parsing process. For `divide by zero`, we store the error first and return it with the other results if it is a print statement. If it is an assignment or bare expression, we return `divide by zero`.

## 4 extensions
### Op-equals
We implement `op=` for every binary operation op. That is, implement `+=`, `-=`, `*=`, `/=`, `%=` and `^=`. The meaning of `x op= e` is the same as `x = x op (e)`. So, when the input is:
```
x = 1
y = 2
z = 3
a = 4
b = 5
c = 6
x += 1
y -= 1
z *= 2
a /= 2
b %= 3
c ^= 2
print x, y, z, a, b, c
```
the output should be:
```
2.0 1.0 6.0 2.0 2.0 36.0
```

### Relational operations
We implement relational operations `==`, `<=`, `>=`, `!=`, `<`, `>`, using 1 to mean true and 0 to mean false. 

Relational operators are left associative and lower precedence than arithmteic operators. 

So:
```
print 1+1 == 2, 1 <= 1, 0 >= 1, -10 != -10, 5>3, -1 < 0
```
should yeild:
```
1 1 0 0 1 1
```

### Boolean operations
We implement the boolean operations for and/conjunction (`&&`), or/disjunction (`||`), and negation (`!`). Treat any non-zero number as true, but only ever return 1 or 0. 

The op-equals extension include these boolean operations. 

Boolean operators are lower precedence than both arithmetic and relational expressions. `||` and `&&` are left associative; `!` is non-associative. 

So:
```
print 1 && 2, 2 && 1, -5 && 1, 0 && -100
print 1+1!=2 || 0>1, !2
```
should yield:
```
1 1 1 0
0 0
```

### Comments
Multi-line comments begin with `/*` and end with `*/`, with arbitrary line breaks in between. 

The `#` character introduces a single-line comment: from `#` until the end of the line is treated as a comment.

So:
```
x = 1
/* 
x = 2
y = 3
*/
y = 4
# print 0
print x, y
```
yields:
```
1.0 4.0
```