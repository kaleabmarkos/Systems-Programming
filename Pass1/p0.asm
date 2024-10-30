PROGRAM:   START   0
FIRST:   LDB   #BUF2
        BASE   BUF   2
        STL   RETADDR
        CLEAR   X
TOP:   RMO   X,A
        MUL   BUF1,X
        STA   BUF2,X
        TIX   MAX
TOP:    EQU   SUBF+SUBR
        J      RETADDR
BUF1   RESW   512
BUF2:   RESB   1536
MAX:   WORD   512
CHAR:   BYTE   =0CDCBA
HEX:   BYTE   =0X12BA
RETADDR:   RESW    1
        END   FIRST