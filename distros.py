from typing import List

def color_256(n: int) -> str:
    return f"\033[38;5;{n}m"

RST = color_256(0)
WHI = color_256(7)
RED = color_256(9)
GRE = color_256(10)
YEL = color_256(11)
BLU = color_256(12)
LBLU = color_256(14)
BLA = color_256(16)
CYA = color_256(36)
DPIN = color_256(125)

colors = {
    "reset": RST,
    "white": WHI,
    "red": RED,
    "green": GRE,
    "yellow": YEL,
    "blue": BLU,
    "lightblue": LBLU,
    "black": BLA,
    "cyan": CYA,
    "deeppink": DPIN
}

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

tux_lines: List[str] = [
WHI + "                                        " + RST,   
WHI + "                                        " + RST,
WHI + "                     .:                 " + RST,
WHI + "                                        " + RST,
WHI + f"               .+#.-#+*                 " + RST,
WHI + f"               .+{YEL}=*+*-{WHI}*                 " + RST,
WHI + f"               {YEL}.+****+= {WHI}.               " + RST,
WHI + f"               .#{YEL}+++#{WHI}%%+                " + RST,
WHI + "               %@%%%@@@%-               " + RST,
WHI + "              =%@%%%@%*+*:.             " + RST,
WHI + "             *@@@@@@@@@@@%..            " + RST,
WHI + "            =@@@@%@@@@@@@%=             " + RST,
WHI + "           .*%@%@#@@@@@@@@* .           " + RST,
WHI + f"        {YEL}+*#*={WHI}%%@@%@@@@%@{YEL}%#*   :+        " + RST,
WHI + f"     {YEL}+***####+{WHI} *@@@@@@@{YEL}%***-:+*#*       " + RST,
WHI + f"     {YEL}+*#######*{WHI} +@@%@@@{YEL}%++*#######*     " + RST,
WHI + f"     {YEL}**########*#{WHI}%%%#*: {YEL}:*#######**     " + RST,
YEL + f"     :==++*****+-       :+***+=         " + RST,
YEL + f"            :--:         :-:.           " + RST,
WHI + "                                        " + RST,
]

def print_side_by_side(left: List[str], right: List[str], width: int = 40, gap: int = 4) -> None:
    spacer = ' ' * gap
    for l, r in zip(left, right):
        # pad to width (colour codes do NOT count for len)
        print(l.ljust(width + l.count('\033')) + spacer + r.ljust(width + r.count('\033')))

distros = {
    "linux": tux_lines,
    "arch": arch_lines,
    "cachyos": cachy_lines,
    "debian": debian_lines
}

# ---- show them ----
#print_side_by_side(arch_lines, cachy_lines, gap=6)
