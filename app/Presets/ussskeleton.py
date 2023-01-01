PART1 = """//USSSCHG  JOB (JOBNAME),'CREATE USS SCREEN ',CLASS=A,                  00010000
//*            TYPRUN=SCAN,                                             00020000
//             MSGLEVEL=(1,1),MSGCLASS=K,NOTIFY=&SYSUID                 00030000
//*
//BUILD   EXEC ASMACL
//C.SYSLIB  DD DSN=SYS1.SISTMAC1,DISP=SHR
//          DD DSN=SYS1.MACLIB,DISP=SHR
//C.SYSIN   DD *
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
         MACRO
&NAME    SCREEN &MSG=™,&TEXT=™
         AIF   ('&MSG' EQ '™' OR '&TEXT' EQ '™').END
         LCLC  &BFNAME,&BFSTART,&BFEND
&BFNAME  SETC  'BUF'.'&MSG'
&BFBEGIN SETC  '&BFNAME'.'B'
&BFEND   SETC  '&BFNAME'.'E'
.BEGIN   DS    0F
&BFNAME  DC    AL2(&BFEND-&BFBEGIN)        MESSAGE LENGTH
&BFBEGIN EQU   *                       START OF MESSAGE
*  HERE START THE GENERATION OF THE LOGO
*  TO GO AFTER - SEARCH (EMERIC)
         DC    X'F57A'                 ERASE/WRITE, WCC"""

PART2 = """
* (EMERIC) ==>   CODE AFTER WALLPAPER GENERATED
*         DC    X'1104B0'               SBA, 1120     ROW 14 COL 01
*         DC    X'290242F5C0E0'         SFE, PROTECTED/NORMAL/PURPLE
*         DC C'                                        '
*         DC C'                                        '
         DC    X'110772'               SBA, 1668     ROW 20 COL 68
         DC    X'290242F5C0E0'         SFE, PROTECTED/NORMAL/PURPLE
         DC    C'by DEFAY E.'
*.* APPLICATION: NETVIEW
*         DC    X'11061C'               APPLICATION POSITION
*         DC    X'290242F2C0E0'         SFE, PROTECTED/NORMAL/RED
*         DC    C'CNM01'                APPLICATION NAME
*         DC    X'110625'               DESCRIPTION POSITION
*         DC    X'290242F1C0E0'         SFE, PROTECTED/NORMAL/BLUE
*         DC    C'- Netview System'     APPLICATION DESCRIPTION
.* APPLICATION: TSO
*         DC    X'110699'               APPLICATION POSITION
*         DC    X'290242F2C0E0'         SFE, PROTECTED/NORMAL/RED
*         DC    C'TSO'                  APPLICATION NAME
*         DC    X'1106A2'               DESCRIPTION POSITION
*         DC    X'290242F1C0E0'         SFE, PROTECTED/NORMAL/BLUE
*         DC    C'- Logon to TSO/ISPF'  APPLICATION DESCRIPTION
*.* APPLICATION: SA
*         DC    X'11066C'               APPLICATION POSITION
*         DC    X'290242F2C0E0'         SFE, PROTECTED/NORMAL/RED
*         DC    C'SA'                   APPLICATION NAME
*         DC    X'110675'               DESCRIPTION POSITION
*         DC    X'290242F1C0E0'         SFE, PROTECTED/NORMAL/BLUE
*         DC    C'- System Automation'  APPLICATION DESCRIPTION
.* OTHER INFORMATION
         DC    X'1106E2'               SBA, 1780     ROW 23 COL 01
         DC    X'290242F2C0E0'         SFE, PROTECTED/NORMAL/RED
         DC    C'Ask me Anything Master...'
         DC    X'1106FB'               SBA, 1802     ROW 23 COL 22
         DC    X'290242F6C0C8'         SFE, UNPROTECTED/NORMAL
         DC    X'13'                   INSERT CURSOR
         DC    X'11073A'               SBA, 1840     ROW 24 COL 01
         DC    X'290242F6C0E0'         SFE, PROTECTED/NORMAL/YELLOW
         DC    C&TEXT                  USS MESSAGES
&BFEND   EQU   *                       END OF MESSAGE
.END     MEND
*
*
*               ..............
USSTAB   USSTAB TABLE=STDTRANS,FORMAT=DYNAMIC
*        SPACE
L        USSCMD   CMD=L,REP=LOGON,FORMAT=BAL      
         USSPARM  PARM=P1,REP=APPLID,DEFAULT=TSO
         USSPARM  PARM=LOGMODE                    
         SPACE                                    
TSO      USSCMD CMD=TSO,REP=LOGON,FORMAT=BAL
         USSPARM PARM=APPLID,DEFAULT=TSO
         USSPARM PARM=P1,REP=DATA
*        SPACE
CNM01    USSCMD  CMD=CNM01,REP=LOGON,FORMAT=BAL
         USSPARM PARM=APPLID,DEFAULT=CNM01
CICS     USSCMD  CMD=CICS,REP=LOGON,FORMAT=BAL
         USSPARM PARM=APPLID,DEFAULT=CICS
IMS      USSCMD  CMD=IMS,REP=LOGON,FORMAT=BAL
         USSPARM PARM=APPLID,DEFAULT=IMS81CR1
SA       USSCMD  CMD=CNM01,REP=LOGON,FORMAT=BAL
         USSPARM PARM=APPLID,DEFAULT=CNM01
*        SPACE
         USSMSG MSG=00,BUFFER=(BUF00,SCAN)
         USSMSG MSG=01,BUFFER=(BUF01,SCAN)
         USSMSG MSG=02,BUFFER=(BUF02,SCAN)
         USSMSG MSG=03,BUFFER=(BUF03,SCAN)
*        USSMSG MSG=04,BUFFER=(BUF04,SCAN)
         USSMSG MSG=05,BUFFER=(BUF05,SCAN)
         USSMSG MSG=06,BUFFER=(BUF06,SCAN)
         USSMSG MSG=08,BUFFER=(BUF08,SCAN)
         USSMSG MSG=10,BUFFER=(BUF10,SCAN)
         USSMSG MSG=11,BUFFER=(BUF11,SCAN)
         USSMSG MSG=12,BUFFER=(BUF12,SCAN)
         USSMSG MSG=14,BUFFER=(BUF14,SCAN)
*        SPACE
STDTRANS DC    X'000102030440060708090A0B0C0D0E0F'
         DC    X'101112131415161718191A1B1C1D1E1F'
         DC    X'202122232425262728292A2B2C2D2E2F'
         DC    X'303132333435363738393A3B3C3D3E3F'
         DC    X'404142434445464748494A4B4C4D4E4F'
         DC    X'505152535455565758595A5B5C5D5E5F'
         DC    X'604062636465666768696A6B6C6D6E6F'
         DC    X'707172737475767778797A7B7C7D7E7F'
         DC    X'80C1C2C3C4C5C6C7C8C98A8B8C8D8E8F'
         DC    X'90D1D2D3D4D5D6D7D8D99A9B9C9D9E9F'
         DC    X'A0A1E2E3E4E5E6E7E8E9AAABACADAEAF'
         DC    X'B0B1B2B3B4B5B6B7B8B9BABBBCBDBEBF'
         DC    X'C0C1C2C3C4C5C6C7C8C9CACBCCCDCECF'
         DC    X'D0D1D2D3D4D5D6D7D8D9DADBDCDDDEDF'
         DC    X'E0E1E2E3E4E5E6E7E8E9EAEBECEDEEEF'
         DC    X'F0F1F2F3F4F5F6F7F8F9FAFBFCFDFEFF'
END      USSEND
*        SPACE
*********************************************************************** ********
*DEFAULT MESSAGE PROVIDED BY VTAM:
*  MSG 00: IST457I POSITIVE command COMMAND RESPONSE
*  MSG 01: IST450I INVALID command COMMAND SYNTAX
*  MSG 02: IST451I command COMMAND UNRECOGNIZED, PARAMETER=parameter
*  MSG 03: IST452I parameter PARAMETER EXTRANEOUS
*  MSG 04: IST453I parameter PARAMETER VALUE value NOT VALID
*  MSG 05: N/A
*  MSG 06: IST792I NO SUCH SESSION EXISTS
*  MSG 07: N/A
*  MSG 08: IST454I command COMMAND FAILED, INSUFFICIENT STORAGE
*  MSG 09: N/A
*  MSG 10: READY
*  MSG 11: IST455I parameters SESSIONS ENDED
*  MSG 12: IST456I keyword REQUIRED PARAMETER OMITTED
*  MSG 13: N/A
*  MSG 14: IST458I USS MESSAGE number NOT DEFINED
*********************************************************************** ********
*  CUSTOMIZED USS MESSAGES:
         SCREEN MSG=00,TEXT='Master, The command is in progress...'
         SCREEN MSG=01,TEXT='Invalid command or syntax'
         SCREEN MSG=02,TEXT='Ha Ha... You're wrong Master'
         SCREEN MSG=03,TEXT='Parameter is unrecognized!'
*        SCREEN MSG=04,TEXT='Parameter with value is invalid'
         SCREEN MSG=05,TEXT='Why do you wanna leave me Master ?'
         SCREEN MSG=06,TEXT='There is not such session.'
         SCREEN MSG=08,TEXT='Command failed as storage shortage.'
         SCREEN MSG=10,TEXT='Anything...'
         SCREEN MSG=11,TEXT='Your session has ended'
         SCREEN MSG=12,TEXT='Required parameter is missing'
         SCREEN MSG=14,TEXT='There is an undefined USS message'
         END
/*
//L.SYSLMOD DD DISP=SHR,DSN=ADCD.Z110.VTAMLIB
//L.SYSIN   DD *
  NAME USSN(R)
//*
"""