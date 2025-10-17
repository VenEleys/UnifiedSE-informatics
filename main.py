from __future__ import annotations
from typing import Union, Iterable
from enum import Enum
from itertools import permutations

class Utils:
    nums: str = "0123456789"
    letters: str = "abcdefghijklmnopqrstuvwxyz"
    numsLetters: str = nums+letters
    class OPERATORS(Enum):
        """
        Includes standart math operators in String
        """
        ADDITION = "+"
        SUBSTRACTION = "-"
        MULTIPLY = "*"
        DIVISION = "/"
        FLOORDIVISION = "//"
        MOD = "%"
        POWER = "**"
        EQUAL = "=="
        INEQUAL = "!="
        LESS = "<"
        LESS_EQUAL = "<="
        GREATER = ">"
        GREATER_EQUAL = ">="

    class HardNum:
        """
        Special data Type
        \nIncludes List, Str, Int at once
        Can easily be converted to number with other base

        """
        def __init__(self, arg: Union[str, int, list[Union[str,int]], Utils.HardNum, float], currentSystem:int = 10) -> None:
            self.num: list[int] = []
            self.ishard: bool = False
            self.currentSystem: int = currentSystem
            self.isNegative: bool = False
            self.fract: str = ""

            if isinstance(arg, Utils.HardNum):
                self.num = arg.num
                return

            if isinstance(arg, int):
                if abs(arg) == -arg:
                    arg = abs(arg)
                    self.isNegative = True
                
                self.num = [int(i) for i in str(arg)]
                return
            
            if isinstance(arg, str):
                if arg[0] == "-":
                    self.isNegative = True
                    arg = arg[1:]

                i:int = 0
                while i < len(arg):
                    if arg[i] in Utils.numsLetters:
                        self.num.append(Utils.numsLetters.index(arg[i]))
                        i += 1
                        continue
                    if arg[i] == "_":
                        i += 1
                        str_num: str = ""
                        while arg[i] != "_":
                            str_num+= arg[i]
                            i += 1
                        num: int = int(str_num)
                        if num > 36:
                            self.ishard = True
                        self.num.append(num)
                        i += 1
                        continue
                    raise ValueError(f"Unavailable sign for number: {arg[i]}")
                return
            
            if isinstance(arg, list) or isinstance(arg, tuple):
                num_list: Union[list, tuple] = arg
                for i in num_list:
                    if isinstance(i, int):
                        self.num.append(i)
                        if i > 36:
                            self.ishard = True
                        continue
                    if isinstance(i, str):
                        for j in i:
                            self.num.append(Utils.numsLetters.index(j))
                        continue
                return
            
            if isinstance(arg, float):
                int_: int = int(arg)
                float_: float = arg - int_
                self.fract = str(float_)
                new_ = Utils.HardNum(int_)
                self.num = new_.num
                self.isNegative = new_.isNegative
                return

            raise ValueError(f"Unavailable num type: {type(arg)}")

        def __call__(self, *args, **kwds):
            return self.num
        
        def __len__(self):
            return len(self.num)
        
        def __str__(self):
            num = ""
            if self.isNegative:
                num += "-"
            for i in self.num:
                if i > 36:
                    i = f"({i})"
                else:
                    i = Utils.numsLetters[i]
                num += str(i)
            return num
        def __iter__(self) -> Iterable[int]:
            return iter(self.num)
        
        def __getitem__(self, key: int) -> int:
            return self.num[key]
        
        def __int__(self) -> int:
            if self.currentSystem == 10 and self.__getRealMinSystem() <= 10:
                return int(self.__str__())
            raise ValueError("Unable convert number to int: use getTen or systemToTen instead")
        #TODO: __float__
        
        def __add__(self, num) -> Utils.HardNum:
            return self.__doMathOperation(num, Utils.OPERATORS.ADDITION)
        
        def __sub__(self, num) -> Utils.HardNum:
            return self.__doMathOperation(num, Utils.OPERATORS.SUBSTRACTION)
        
        def __mul__(self, num) -> Utils.HardNum:
            return self.__doMathOperation(num, Utils.OPERATORS.MULTIPLY)
        
        def __truediv__(self, num) -> Utils.HardNum:
            return self.__doMathOperation(num, Utils.OPERATORS.DIVISION)
        
        def __floordiv__(self, num) -> Utils.HardNum:
            return self.__doMathOperation(num, Utils.OPERATORS.FLOORDIVISION)
        
        def __mod__(self, num) -> Utils.HardNum:
            return self.__doMathOperation(num, Utils.OPERATORS.MOD)
        
        def __pow__(self, num) -> Utils.HardNum:
            return self.__doMathOperation(num, Utils.OPERATORS.POWER)
        
        def __neg__(self) -> Utils.HardNum:
            self.isNegative = not self.isNegative
            return self
        
        def __abs__(self) -> Utils.HardNum:
            self.isNegative = False
            return self
        

        def __eq__(self, num) -> bool:
            return self.__doComparisonOperation(num, Utils.OPERATORS.EQUAL)
        
        def __ne__(self, num) -> bool:
            return self.__doComparisonOperation(num, Utils.OPERATORS.INEQUAL)
        
        def __lt__(self, num) -> bool:
            return self.__doComparisonOperation(num, Utils.OPERATORS.LESS)
        
        def __le__(self, num) -> bool:
            return self.__doComparisonOperation(num, Utils.OPERATORS.LESS_EQUAL)
        
        def __gt__(self, num) -> bool:
            return self.__doComparisonOperation(num, Utils.OPERATORS.GREATER)
        
        def __ge__(self, num) -> bool:
            return self.__doComparisonOperation(num, Utils.OPERATORS.GREATER_EQUAL)
        
        
        def __getRealMinSystem(self) -> int:
            return max(self.num)+1
        
        def __doMathOperation(self, num: Union[int, str, Utils.HardNum], operation: Utils.OPERATORS) -> Utils.HardNum:
            ans: int = eval(f"int(self) {operation.value} int(num)")
            if self.currentSystem == 10 and self.__getRealMinSystem() <= 10:
                return Utils.HardNum(ans)
            return Utils.tenToSystem(ans, self.currentSystem)

        def __doComparisonOperation(self, num: Union[int, str, Utils.HardNum], operation: Utils.OPERATORS) -> bool:
            ans: bool = eval(f"int(self) {operation.value} int(num)")
            return ans

            
        def getCurrentSystem(self, *args, **kargs) -> int:
            """
            Returns number`s base
            \n(might be incorrect if base wasn`t set on HardNum implementation)
            """
            return self.currentSystem
        
        def getTen(self, currentSystem: Union[int, None] = None) -> Utils.HardNum:
            """
            Returns number with base10
            """
            if not currentSystem:
                currentSystem = self.currentSystem
            if currentSystem == 10 and self.__getRealMinSystem() <= 10:
                return self
            if currentSystem == 10 and self.__getRealMinSystem() > 10:
                raise ValueError("Unable convert number to base10: real number base is unknown")
            return Utils.systemToTen(self, currentSystem)
        
        def getSystemFromCurrentSystem(self, endSystem: int) -> Utils.HardNum:
            """
            :return: - Number with {endSystem} base from current base (Use getCurrentSystem to check current base)
            :rtype: Utils.HardNum
            :param endSystem: - final base of number
            :type endSystem: int
            """
            if self.currentSystem == 10 and self.__getRealMinSystem() <= 10:
                return Utils.tenToSystem(self, endSystem)
            if self.currentSystem == 10 and self.__getRealMinSystem() > 10:
                raise ValueError(f"Unable convert number to base{endSystem}: real number base is unknown")
            return Utils.systemToSystem(self, self.currentSystem, endSystem)
        
        def getSystemFromSystem(self, startSystem: int, endSystem: int, updateCurrentSystem: bool = False) -> Utils.HardNum:
            """
            :return: - Number with {endSystem} base from {startSystem} base
            :rtype: Utils.HardNum
            :param startSystem: - current base of number
            :param endSystem: - final base of number
            :type startSystem: int
            :type endSystem: int
            """
            if updateCurrentSystem:
                self.currentSystem = startSystem
            return Utils.systemToSystem(self, startSystem, endSystem)

    @staticmethod
    def tenToSystem(num: Union[str, int, list[Union[str,int]], Utils.HardNum], system: int) -> HardNum:
        """
        Converts number with base10 to number with any base
        """
        num = int(Utils.HardNum(num))
        
        if system > 36:
            ans_list: list = []
            while num > 0:
                a = num%system
                num //= system

                ans_list = [a] + ans_list
            return Utils.HardNum(ans_list, system)

        ans_str: str = ""
        while num > 0:
            ans_str = Utils.numsLetters[num%system] + ans_str
            num //= system
        return Utils.HardNum(ans_str, system)
    
    @staticmethod
    def systemToTen(num: Union[str, int, list[Union[str,int]], Utils.HardNum], system: int) -> HardNum:
        """
        Converts number with any base to number with base10
        """
        num = Utils.HardNum(num, system)
        ans: int = 0
        l: int = len(num)
        for index, i in enumerate(num()):
            if i >= system:
                raise ValueError(f"invalid number with base {system}: containing a number ({i}) equal or larger base")
            ans += i*system**(l-1-index)
    
        return Utils.HardNum(ans)
    
    @staticmethod
    def systemToSystem(num: Union[str, int, list[Union[str,int]], HardNum], startSystem: int, endSystem: int):
        """
        Converts base of number from any to any
        """
        num = Utils.systemToTen(num, startSystem)
        num = Utils.tenToSystem(num, endSystem)
        return num
    
    @staticmethod
    def bitwise(num1: Union[str, int, list[Union[str,int]], HardNum], num2: Union[str, int, list[Union[str,int]], HardNum]) -> HardNum:
        """
        Returns bitwise of two numbers in base10
        """
        num1, num2 = int(Utils.HardNum(num1)), int(Utils.HardNum(num2))
        return Utils.HardNum(num1 & num2)
    
    class LogicBinarMatrix:
        def __init__(self, matrix: dict = {}, mask: list[str] = [], letters: str = "", formula: str = "") -> None:
            self.matrix: dict = matrix
            self.mask: list[str] = mask
            self.ans: dict = {}
            self.letters: str = letters
            if not letters:
                self.letters = "".join(matrix.keys())
            self.formula = formula

        # def __setattr__(self, name, value):
        #     super().__setattr__(name, value)
        #     if not self.ans:
        #         self.ans = {}
        
        def solve(self) -> Utils.LogicBinarMatrix:
            if not self.matrix and self.letters and self.formula:
                self.create_matrix()
            letter_perm = list(permutations(self.matrix.keys()))
            matrix_perms = list(permutations(range(len(list(self.matrix.values())[0]))))
            for i in letter_perm:
                for j in matrix_perms:
                    val = 0
                    cor = 0
                    for x in range(len(self.mask)):
                        for y in range(len(self.mask[0])):
                            if self.mask[x][y] in "01":
                                val += 1
                            if self.mask[x][y] == str(self.matrix[i[x]][j[y]]):
                                cor += 1
                    if cor == val:
                        for x in i:
                            self.ans[x] = [self.matrix[x][y] for y in j]
            return self

        def create_matrix(self, letters: str = "", formula: str = ""):
            if letters:
                self.letters = letters
            if formula:
                self.formula = formula

            if not self.letters:
                raise ValueError("Can`t create matrix: keys are missing")
            if not self.formula:
                raise ValueError("Can`t create matrix: formula is missing")
        
            
            width = len(self.letters)
            self.matrix = {}
            for let in self.letters:
                self.matrix[let] = []

            for i in range(width**2):
                binar = bin(i)[2:]
                line = [int(_) for _ in ("0"*(width-len(binar))+binar)]
                for j in range(width):
                    exec(f"{self.letters[j]} = {line[j]}")

                if eval(self.formula):
                    self.add_line(*line)

        def add_line(self, *args: int) -> None:
            if len(args) != len(self.letters):
                raise ValueError(f"Can`t add line: args amount({len(args)}) != keys amount({len(self.letters)})")
            for i in range(len(args)):
                if not isinstance(args[i], int):
                    raise ValueError(f"Value must be int, not {type(args[i])}")
                self.matrix[self.letters[i]].append(args[i])
            

        def print_result(self, printUnmasked: bool = True):
            if not self.ans:
                return
            keys = list(self.ans.keys())
            print(" ".join(keys))

            if printUnmasked:
                for i in range(len(next(iter(self.ans.values())))):
                    for key in keys:
                        print(self.ans[key][i], end = " ")
                    print()



Utils.LogicBinarMatrix(formula="not((x and not(y)) or (y==z) or not(w))", letters="xywz", mask=["00.",".11",".00","01."]).solve().print_result()

