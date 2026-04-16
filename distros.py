from typing import List

def color_256(n: int) -> str:
    return f"\033[38;5;{n}m"

RST = color_256(0)
BLU = color_256(12)
LBLU = color_256(14)
CYA = color_256(36)
DPIN = color_256(125)


arch_lines: List[str] = [
BLU + "                                        " + RST,   
BLU + "                                        " + RST,
BLU + "                    :-                  " + RST,
BLU + "                   .==:                 " + RST,
BLU + "                  .====:                " + RST,
BLU + "                  -=====:               " + RST,
BLU + "                 :=======:              " + RST,
BLU + "                ==.-======.             " + RST,
BLU + "               ============.            " + RST,
BLU + "              -=============.           " + RST,
BLU + "             ================:          " + RST,
BLU + "            =======-:.-=======:         " + RST,
BLU + "          .=======.     =======:        " + RST,
BLU + "         .=======-       =======-       " + RST,
BLU + "         ========-       ======-.       " + RST,
BLU + "       .=======--:       --=======:     " + RST,
BLU + "      :====.                  .-====    " + RST,
BLU + "     :=:                          .-=   " + RST,
BLU + "                                        " + RST,
BLU + "                                        " + RST,
]

cachy_lines: List[str] = [
CYA + "                                        " + RST,    
CYA + "                                        " + RST,
CYA + "                                        " + RST,
LBLU + f"        .{CYA}={LBLU}={CYA}=============+=.             " + RST,
LBLU + f"       :-{CYA}=={LBLU}-=={CYA}======++===.    .-:       " + RST,
LBLU + f"      ---{CYA}==={LBLU}---==+{CYA}======                " + RST,
LBLU + f"     ----{CYA}===={LBLU}-{CYA}========-                 " + RST,
LBLU + f"    ----={CYA}===:                           " + RST,
LBLU + f"  .--=={CYA}=++=.              .{LBLU}-=={CYA}:         " + RST,
CYA + f" .======++.               .:::.         " + RST,
LBLU + f" .-----={CYA}==                              " + RST,
LBLU + f"   =={CYA}======                      :{LBLU}---=-{CYA} " + RST,
CYA + f"    =+++++==.                    :----: " + RST,
CYA + f"     ===={LBLU}=--={CYA}-{LBLU}-::::::::::::::::         " + RST,
CYA + f"      ==={LBLU}=--{CYA}====={LBLU}==-----------          " + RST,
CYA + f"       :={LBLU}=-{CYA}========={LBLU}==-------           " + RST,
CYA + f"        .{LBLU}={CYA}=============={LBLU}==--            " + RST,
CYA + "                                        " + RST,
CYA + "                                        " + RST,
CYA + "                                        " + RST,
]

debian_lines: List[str] = [
DPIN + "                                       " + RST, 
DPIN + "                                       " + RST, 
DPIN + "              :+########*+-:           " + RST, 
DPIN + "           :*####=..   .:+###*-        " + RST, 
DPIN + "          *##*:            :###*.      " + RST, 
DPIN + "         **=                 +#**      " + RST, 
DPIN + "       :#*         .=+=-.     +#-      " + RST, 
DPIN + "       **.       .+           -#-      " + RST, 
DPIN + "       **        =        .   -#=      " + RST, 
DPIN + "       #=        *            =*       " + RST, 
DPIN + "       #=        -+    :     ++        " + RST, 
DPIN + "       +*        ..+-     :++.         " + RST, 
DPIN + "       -#-          ::---:             " + RST, 
DPIN + "        =#+                            " + RST, 
DPIN + "         =#+                           " + RST, 
DPIN + "          .*+                          " + RST, 
DPIN + "            -*+                        " + RST, 
DPIN + "              .=+-                     " + RST, 
DPIN + "                   .                   " + RST, 
DPIN + "                                       " + RST, 
]

def print_side_by_side(left: List[str], right: List[str], width: int = 40, gap: int = 4) -> None:
    spacer = ' ' * gap
    for l, r in zip(left, right):
        # pad to width (colour codes do NOT count for len)
        print(l.ljust(width + l.count('\033')) + spacer + r.ljust(width + r.count('\033')))

distros = {
    "arch": arch_lines,
    "cachyos": cachy_lines,
    "debian": debian_lines   
}

# ---- show them ----
#print_side_by_side(arch_lines, cachy_lines, gap=6)
