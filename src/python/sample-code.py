if __name__ == "__main__":
    class B:
        def __init__(self):
            print("B")

        def funcB1(self):
            print("funcB1")

        def funcB2(self):
            self.__funcB22()

        def __funcB22(self):
            print("funcB22")


    class A:
        def __init__(self):
            print("A")

        def funcA(self):
            b = B()
            b.funcB1()
            b.funcB2()

a = A()
a.funcA()