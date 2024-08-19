def Zellen():
    ca1 = "*"
    for i in range(0,35):
        ca1 = " " + ca1 + " "

    return ca1

def elementary1():
    rule = {"   ": " ",
            "  *": "*",
            " * ": "*",
            " **": "*",
            "*  ": " ",
            "* *": "*",
            "** ": "*",
            "***": " ",
            }
    return rule

def elementary2():
    rule = {"   ": " ",
            "  *": "*",
            " * ": "*",
            " **": "*",
            "*  ": "*",
            "* *": "*",
            "** ": "*",
            "***": " ",
            }
    return rule

def elementary3():
    rule = {"   ": " ",
            "  *": " ",
            " * ": "*",
            " **": "*",
            "*  ": "*",
            "* *": "*",
            "** ": "*",
            "***": " ",
            }
    return rule

def elementary4():
    rule = {"   ": " ",
            "  *": " ",
            " * ": "*",
            " **": " ",
            "*  ": "*",
            "* *": "*",
            "** ": " ",
            "***": " ",
            }
    return rule


def  ca_step(ca1, rule):
    t = ca1
    print(t)

    for k in range(0,31):
        temp = " "
        for j in range(1,70):
            temp = temp + rule[t[j-1] + t[j] + t[j+1]]

        t = temp + " "  #Die erste und die letzte Zelle bleiben Tot, weil sie on the edge leben.
        print(t)

    ca2 = t

    return ca1, ca2, rule


def main():
    ca1 = Zellen()
    rule = elementary1()

    ca2 = ca_step(ca1, rule)
    print(ca2)

    rule = elementary2()
    ca2 = ca_step(ca1, rule)
    print(ca2)
    print("Zelde = Illuminati confirmed")

    rule = elementary3()
    ca2 = ca_step(ca1, rule)
    print(ca2)

    rule = elementary4()
    ca2 = ca_step(ca1, rule)
    print(ca2)


main()