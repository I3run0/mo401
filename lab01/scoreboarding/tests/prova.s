fld f1 0(x1)
fld f2, 0(x3)
fadd f3, f2, x0
fadd f1, f1, f3
fdiv f1, f1, f3
fmul f2, f2, f1
fsub f2, f2, f3
fsd f1, 0(x1)
fsd f2, 0(x3)