class Algebra:

    def __init__(self):
        pass

    @classmethod
    def sum(cls, a, b):
        return a + b
    
    @classmethod
    def sub(cls, a, b):
        if a < b:
            return None
        return a - b
    
    @classmethod
    def mul(cls, a, b):
        return a*b

    
    
