fld f1, 0(x1)
fld f2, 0(x3)
fld f3, 0(x4)
fld f4, 0(x5)
fadd f3, f2, f1
fsd f3, 0(x4)
fdiv f4, f2, f1
fsd f4, 0(x5)
fadd f1, f2, f4
fsd f1, 0(x1)
fmul f2, f2, f3
fsd f2, 0(x3)
fsub f2, f2, f3
fsd f2, 0(x3)
fdiv f1, f1, f4
fsd f1, 0(x1)
