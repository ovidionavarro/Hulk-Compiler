from src.cmp.semantic import Type,Context,SemanticError,Method
class ObjectType(Type):
    def __init__(self,name:str='Object'):
        super().__init__(name)

    # def __eq__(self, other: object):
    #     return other.name==self.name or isinstance(other,NumType) or isinstance(other,StringType) or isinstance(other,BoolType) or isinstance(other,ObjectType)
class AnyType(Type):
    def __init__(self, name: str='Any'):
        super().__init__(name)
class NoneType(Type):
    def __init__(self,name:str='None'):
        super().__init__(name)


class NumType(ObjectType):
    def __init__(self):
        super().__init__('Number')
    # def __eq__(self, other: object):
    #     return other.name == self.name or isinstance(other, NumType) or isinstance(other, ObjectType)
        

class StringType(ObjectType):
    def __init__(self):
        super().__init__('String')

    # def __eq__(self, other: object):
    #     return other.name == self.name or isinstance(other, StringType) or isinstance(other, ObjectType)
        
class BoolType(ObjectType):
    def __init__(self):
        super().__init__('Boolean')

    # def __eq__(self, other):
    #     return other.name == self.name or isinstance(other, BoolType) or isinstance(other, ObjectType)

class ErrorType(Type):    
    def __init__(self):
        super().__init__('<error>')

    # def conforms_to(self, other):
    #     return True

    # def bypass(self):
    #     return True

    # def __eq__(self, other):
    #     return isinstance(other, Type)


