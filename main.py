from typing import Union, Iterable
from __future__ import annotations

class Utils:
    nums: str = "0123456789"
    letters: str = "abcdefghijklmnopqrstuvwxyz"
    numsLetters: str = nums+letters
    class HardNum:
        def __init__(self, arg: Union[str, int, list[Union[str,int]], Utils.HardNum], currentSystem:int = 10) -> None:
            self.num: list[int] = []
            self.ishard: bool = False
            self.currentSystem: int = currentSystem

            if isinstance(arg, Utils.HardNum):
                self.num = arg.num
                return

            if isinstance(arg, int):
                self.num = [int(i) for i in str(arg)]
                return
            
            if isinstance(arg, str):
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

            raise ValueError(f"Unavailable num type: {type(arg)}")

        def __call__(self, *args, **kwds):
            return self.num
        
        def __len__(self):
            return len(self.num)
        
        def __str__(self):
            num = ""
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
        
        def __getRealMinSystem(self) -> int:
            return max(self.num)+1
        
        def __int__(self) -> int:
            if self.currentSystem == 10 and self.__getRealMinSystem() <= 10:
                return int(self.__str__())
            raise ValueError("Unable convert number to int: use getTen or systemToTen instead")
            
        def getCurrentSystem(self, *args, **kargs) -> int:
            return self.currentSystem
        
        def getTen(self, currentSystem: Union[int, None] = None) -> Utils.HardNum:
            if not currentSystem:
                currentSystem = self.currentSystem
            if currentSystem == 10 and self.__getRealMinSystem() <= 10:
                return self
            if currentSystem == 10 and self.__getRealMinSystem() > 10:
                raise ValueError("Unable convert number to base10: real number base is unknown")
            return Utils.systemToTen(self, currentSystem)
        
        def getSystemFromCurrentSystem(self, endSystem: int):
            if self.currentSystem == 10 and self.__getRealMinSystem() <= 10:
                return Utils.tenToSystem(self, endSystem)
            if self.currentSystem == 10 and self.__getRealMinSystem() > 10:
                raise ValueError(f"Unable convert number to base{endSystem}: real number base is unknown")
            return Utils.systemToSystem(self, self.currentSystem, endSystem)
        
        def getSystemFromSystem(self, startSystem: int, endSystem: int, updateCurrentSystem: bool = False):
            if updateCurrentSystem:
                self.currentSystem = startSystem
            return Utils.systemToSystem(self, startSystem, endSystem)

    @staticmethod
    def tenToSystem(num: Union[str, int, list[Union[str,int]], Utils.HardNum], system: int) -> HardNum:
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
        num = Utils.systemToTen(num, startSystem)
        num = Utils.tenToSystem(num, endSystem)
        return num
    
    @staticmethod
    def bitwise(num1: Union[str, int, list[Union[str,int]], HardNum], num2: Union[str, int, list[Union[str,int]], HardNum]) -> HardNum:
        num1, num2 = int(Utils.HardNum(num1)), int(Utils.HardNum(num2))
        return Utils.HardNum(num1 & num2)