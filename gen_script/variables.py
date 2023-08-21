#!/usr/bin/python3

"""
variables
---------

Contains class files for reading and processing macro variables.
"""

class Variable :
    """
Represents the base class for variables.
"""

    def __init__(self, name) :
        self.__name = name

    @property
    def name(self) :
        return self.__name

    @name.setter
    def name(self, value) :
        self.__name = value

    def __str__(self) :
        return self.name

    def __getitem__(self, index) :
        raise NotImplemented

    def __len__(self) :
        raise NotImplemented

class RangeVariable(Variable) :
    """
RangeVariable

Represents a variable that can take values within a range.
"""

    def __init__(self, name, start, end, points) :
        super().__init__(name)
        self.__start = start
        self.__end = end
        self.__points = points

    @property
    def start(self) :
        return self.__start

    @start.setter
    def start(self, value) :
        self.__start = value

    @property
    def end(self) :
        return self.__end

    @end.setter
    def end(self, value) :
        self.__end = value

    @property
    def points(self) :
        return self.__points

    @points.setter
    def points(self, value) :
        self.__points = value

    def __getitem__(self, value) :
        if self.points == 1 :
            return self.start
        return (self.end - self.start) / (self.points - 1) * value + self.start

    def __len__(self) :
        return self.points

class ListVariable(Variable) :
    """
ListVariable

Represents a variable that can take values from a list.
"""

    def __init__(self, name, items) :
        super().__init__(name)
        self.__items = items

    def __iter__(self) :
        return iter(self.__items)

    @property
    def items(self) :
        return self.__items

    @items.setter
    def items(self, value) :
        self.__items = value

    def __getitem__(self, index) :
        return self.items[i]

    def __len__(self) :
        return len(self.items)
    
    
