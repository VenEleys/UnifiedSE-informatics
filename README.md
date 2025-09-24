# Usage
paste this code to your project

use Utils methods to convert numbers with any base >= 2

# System to ten
if you have number with base > 36 or non-letter number, use f"_var_" instead
```python
var = 10
print(Utils.systemToTen(f"12_{var}_3",16)) # 4771
print(Utils.systemToTen("12_10_3",16)) # 4771
print(int("12a3",16)) # 4771
print(Utils.systemToTen("12_10_3",16) == (int("12a3",16))) # True
print(hex(4771)[2:]) # 12a3
print(Utils.tenToSystem("4771", 16)) # 12a3
```
