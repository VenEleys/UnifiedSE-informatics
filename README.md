# What is it?
This is utility allows to solve most tasks of Unified State Exam (ЕГЭ) in Russia 2026
All useful methods are gathered in 1 file to make it easy to import and use

# Further will be provided documentation about using such methods in tasks (1-27)
missing tasks are WIP

# Task 2: LogicBinarMatrix
Example:
F = ¬ (x → w) ∨ (y ≡ z) ∨ y
"Truth table":
var1 var2 var3 var4 F
 -    1    -    0   0
 -    0    1    -   0
 -    -    0    -   0
```python
Utils.LogicBinarMatrix(formula="not(not(x<=w) or (y==z) or y)", letters="xywz", mask=["...","10.",".10","0.."]).solve().print_result()
# z x w y
# 1 1 1 0 
# 1 0 1 0 
# 1 0 0 0
```
this instance of LogicBinarMatrix requires:
- formula(str): function based on variables, if "truth table" (aka Таблица истинности) requires F(function result) = 0, add not() to full formula
- letter(str): names of used variables
- mask(list[str]): data based on "truth table", mask must be filled by columns of "truth table"
