# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 Taobao .Inc
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://code.taobao.org/license.html.
#
# This software consists of voluntary contributions made by many
# individuals. For the exact contribution history, see the revision
# history and logs, available at http://code.taobao.org/.
#

USER_DISABLE = 0
USER_ENABLE = 1
USER_DELETED = 2

USER_FEMALE=0
USER_MALE=1
USER_UNKNOWN=-1

PROJECT_DISABLE=0
PROJECT_ENABLE=1
PROJECT_MARK_DELETED=2
PROJECT_TRUE_DELETED=3

MY_PROJECT_NONE = 0
MY_PROJECT_OWNER = 1
MY_PROJECT_MEMBER = 2 #member
MY_PROJECT_WATCH = 3 #watch

ISSUE_OPEN = 0
ISSUE_CLOSED = 1
ISSUE_DELETED = 2

COMMENT_ENABLE = 1
COMMENT_DELETED = 0

FILE_ENABLE = 1
FILE_DELETED = 0

WIKI_ENABLE = 1
WIKI_DELETED = 0

PM_SEND_INV = 0
PM_ACCEPT_INV = 1
PM_REJECT_INV = 2


#代码仓库类型
REPOSITORY_TYPE_PUBLIC=1
REPOSITORY_TYPE_PRIVATE=2

MSG_INBOX = 1
MSG_OUTBOX = 2
MSG_TRASH = 3

MSG_SENDER_OUTBOX = 1
MSG_SENDER_TRASHBOX = 2

MSG_READER_INBOX = 3
MSG_READER_TRASHBOX = 4
MSG_DELETED = 5

DEFAULT_PIC='/img/headers/default.png'



LICENSES= (
('Apache License 2.0','Apache License 2.0'),
('Artistic License/GPL','Artistic License/GPL'),
('Eclipse Public License 1.0','Eclipse Public License 1.0'),
('GNU General Public License v2','GNU General Public License v2'),
('GNU General Public License v3','GNU General Public License v3'),
('GNU Lesser General Public License','GNU Lesser General Public License'),
('MIT License','MIT License'),
('Mozilla Public License 1.1','Mozilla Public License 1.1'),
('New BSD License','New BSD License'),
)

OPEN_PLATFORM_WEIBO='weibo'
OPEN_PLATFORM_TAOBAO='taobao'
WEIBO_APP_KEY='2808354212'
WEIBO_APP_SECRET='1e67e9dcfb8954e56a233dc75596f85a'

TAOBAO_APP_KEY='12382164'
TAOBAO_APP_SECRET='898beee5769deff2178bec1b15a2a6bf'

OPEN_DEFAULT_PWD='123456'

LANGS=("2.PAK",
"A++",
"ABC",
"ABLE",
"ABSET",
"ABSYS",
"Accent",
"ActionScript",
"Ada",
"ADL",
"Alan",
"Aleph",
"ALGOL",
"AmigaE",
"Android",
"APL",
"AppleScript",
"AspectJ",
"Assembly",
"Atlas Autocode",
"Acceptance, Test Or Launch Language",
"AutoLISP",
"AWK",
"BASIC",
"Batch",
"BCPL",
"Befunge",
"BETA",
"Bigwig",
"Bistro",
"BLISS",
"Blue",
"BOO",
"Bourne shell",
"Bourne-Again shell",
"Brainfuck",
"C",
"Cg",
"C++",
"C#",
"Caml",
"Ceicil",
"CHILL",
"Cilk",
"Clarion",
"Clean",
"Clipper",
"CLU",
"Cold Fusion",
"COBOL",
"CobolScript",
"Cocoa",
"COMAL",
"Concurrent Clean",
"CORAL66",
"Common Lisp",
"CPL",
"Curl",
"Delphi",
"Dibol",
"Dylan",
"E",
"Eiffel",
"ElastiC",
"Elf",
"Erlang",
"Euphoria",
"F#",
"Forth",
"FORTRAN",
"FP",
"Frontier",
"FoxPro",
"Falcon",
"GENIE",
"Go",
"Godiva",
"Goedel",
"Groovy",
"Handel-C",
"Haskell",
"HTML",
"HTMLScript",
"Hugo",
"HyperCard",
"ICI",
"Icon",
"Inform",
"INTERCAL",
"IronPython",
"J",
"JADE",
"Java",
"JavaScript",
"JOVIAL",
"Joy",
"J#",
"Kid",
"KRYPTON",
"Jython",
"Kvikkalkul",
"LabVIEW",
"Lagoona",
"Leda",
"Limbo",
"LISP",
"Logo",
"MSW Logo",
"Star Logo",
"Lua",
"LYaPAS",
"m4",
"MAD",
"Mathematica",
"MATLAB",
"Miranda",
"Miva",
"Mercury",
"Mesa",
"ML",
"Microcode",
"MMIX",
"Modula",
"Modula-2",
"MOO",
"Moto",
"MUMPS",
"Mary",
".NET",
"Nial",
"Nuva",
"NodeJS",
"Oberon",
"Objective-C",
"Object-C",
"Objective Caml",
"Object Pascal",
"Obliq",
"Occam",
"Oz",
"Pascal",
"Perl",
"PHP",
"Pike",
"PILOT",
"PL-SQL",
"PL/I",
"Poplog",
"POP-11",
"PostScript",
"Prolog",
"Proteus",
"Python",
"REBoL",
"Powerbuilder",
"Quake C",
"Rascal",
"Ratfor",
"REBOL",
"REXX",
"Report (RPG)",
"Rigal",
"Ruby",
"S-Lang",
"SAS",
"Sather",
"Scala",
"Scheme",
"Sed",
"Seed7",
"Self",
"SETL",
"SGML",
"Simula",
"Sisal",
"Smalltalk",
"SML",
"Snobol",
"SPARK",
"SPICE",
"SPITBOL",
"SQL",
"Squeak",
"SystemC",
"SystemVerilog",
"Shell",
"Swift",
"TADS",
"Tcl Tk",
"teco",
"Tempo",
"Tom",
"tpu",
"Trac",
"Turing",
"Unicon",
"UnLambda",
"Uml",
"Vala",
"Var'aq",
"VBA",
"VBScript",
"Verilog",
"VHDL",
"Verilog HDL",
"Visual Basic",
"Visual C++",
"Visual C#",
"Visual DialogScript",
"Visual FoxPro",
"Water",
"Whitespace",
"Windows PowerShell",
"Wirth",
"XHTML",
"XML",
"XPath",
"XSL",
"XSLT",
"XOTcl",
"YAFL",
"Yorick",
"Z")

PAGE_SIZE = 20
