from collections import defaultdict
import functools
import itertools
import json
import math
import numpy
import re
import datetime

text = """
 ,S, ,C, ,C, , 
X, ,X, , , ,C, 
 ,X, , ,O,S, ,X
O,B, ,O, , ,S, 
B, ,O,R, ,R, , 
 ,B, , ,C, ,O, 
 ,O,X, ,C, ,R, 
R, ,B, , , , , 
X, ,B, ,S, , , 
 ,C, ,O,X, , , 
B, ,B, ,S, ,R, 
 ,B, ,C, ,B, ,B
X, ,X, ,R, ,C, 
O,O,R, ,X, ,B, 
S, ,S, ,B, ,O,S
S, , ,O, ,S, ,O
 ,C, ,B, , ,R, 
 ,X, ,B, , ,X, 
 ,B, , ,C, ,C, 
 ,B, ,S, ,B, ,R
 ,X, ,X, , , , 
 , , , , , ,C, 
 ,S, ,X, , , ,R
B, ,S, , ,O,B, 
O, ,R, , , ,S, 
 ,X, ,O,B, ,B, 
O, , ,C, , ,C, 
B, ,B, , ,B, , 
 , ,X, ,X, ,X, 
O,B, ,C, ,B, ,B
 , , ,B, ,S, , 
 ,C, ,X, ,O,C, 
B, ,B, , , , ,S
R, , , ,X, ,B, 
B, ,C, ,S, ,R, 
B, ,C, ,X, ,B, 
S, ,R, , ,B, ,X
 ,C, , , , , ,X
 ,O,B, ,S, ,B, 
 ,B, ,B, , , , 
B, ,B, ,X, ,S, 
 , ,O, ,R, ,B, 
B, , ,R, , , , 
 ,X, , ,C, , ,X
B, , ,B, ,B, ,O
S, , ,R, , , , 
O,X, , ,R, ,R, 
X, , ,B, ,O,X, 
X, ,C, ,S, ,B, 
 , ,X, ,C, , ,S
S, , , ,C, , , 
S, , ,B, ,X, , 
X, ,B, ,C, , ,X
 ,C, ,B, , ,O,O
S, ,C, ,B, ,O, 
O,B, , ,O,R, ,B
B, , , ,S, ,O,X
X, ,C, ,C, , , 
B, , ,S, ,B, , 
 ,R, , ,S, ,O,B
X, , ,C, ,R, ,B
B, ,B, , , ,X, 
C, ,O, ,B, , ,B
S, , , ,B, ,C, 
 ,B, ,B, , ,B, 
R, , ,X, , ,S, 
S, , ,C, ,B, , 
 ,C, ,O, ,S, ,O
 ,B, , ,B, ,S, 
O,R, , ,B, ,O, 
 , ,O,O,B, ,O,C
S, , ,C, ,R, ,S
 ,S, ,B, ,X, , 
S, , ,X, ,O, ,B
R, , , ,C, ,B, 
S, , ,S, , ,X, 
 ,R, ,X, ,R, , 
X, ,B, ,R, , ,C
 ,R, , , , , , 
C, ,S, , ,R, , 
 ,C, ,S, , ,B, 
B, , , ,R, ,R, 
 , , , , , , ,X
B, , ,X, , , ,X
 ,X, ,B, ,C, ,O
R, , , ,B, , ,X
R, ,B, ,R, ,B, 
R, ,B, ,B, ,B, 
 ,B, ,X, ,X, , 
 , , , ,R, , , 
 ,X, , ,S, , ,B
X, ,B, , ,X, , 
C, ,B, , ,B, , 
 , ,B, ,C, ,O,C
C, , , , ,X, ,C
 , , ,O,X, ,S, 
 ,X, ,C, ,C, , 
X, , ,C, ,O, ,R
O, ,X, ,X, ,O,R
O,C, ,B, , ,X, 
C, ,C, , ,X, ,X
 ,B, , ,O,X, , 
 ,S, , ,S, , ,X
 ,S, ,R, , ,X, 
X, , , , ,X, ,B
 ,C, , ,C, , ,B
 ,S, ,S, ,C, , 
 ,O,C, , ,R, ,X
 ,X, ,R, , ,B, 
 ,B, ,B, ,S, ,R
 , ,S, , ,B, , 
X, ,O,R, , , ,R
O,X, , ,X, ,O,C
B, ,O,X, ,R, ,S
R, ,B, ,O,B, , 
 ,C, ,X, ,X, ,X
 , ,R, , ,R, ,R
 , , , , ,O, ,X
 ,B, , , , ,R, 
 , ,S, , ,C, ,X
O, ,X, ,R, ,C, 
C, , ,X, ,C, , 
 ,X, ,B, ,S, ,X
X, , ,O,X, ,S, 
B, , ,B, ,R, , 
B, ,S, ,X, , , 
O,O, ,B, , ,R, 
C, ,S, ,B, ,X, 
 ,B, ,C, ,B, ,O
B, ,S, ,C, , ,B
R, , ,X, , , , 
C, , ,B, , ,C, 
 ,X, ,S, ,X, ,X
X, , ,C, , , ,S
 ,R, , ,X, ,X, 
 , , ,X, ,C, , 
 ,O,O,R, ,C, , 
C, ,O,B, ,R, ,O
 ,R, ,B, , , ,X
 ,O, , ,X, ,C, 
 , , ,S, , , ,S
B, ,X, , ,X, , 
X, ,S, ,X, , ,S
 ,X, , ,X, ,C, 
X, , , , , ,O,X
C, ,C, ,O,S, , 
X, ,O,O, ,C, ,B
 ,R, ,B, ,X, ,X
 ,O,X, ,C, , , 
C, , , , ,R, , 
 ,C, ,S, , ,B, 
X, ,C, , ,C, ,C
X, , ,B, ,S, , 
 , ,B, , , ,X, 
 ,R, ,B, , ,C, 
 ,O,R, ,B, ,B, 
O, ,B, , ,X, ,X
S, , ,X, ,B, ,B
X, , ,B, , , , 
C, , , ,S, , , 
X, , , ,R, ,B, 
B, ,C, ,B, ,S, 
O,R, ,X, ,R, , 
C, ,R, ,O, ,R, 
 ,B, ,C, , ,B, 
 ,R, , ,B, , , 
 ,B, , ,S, , , 
C, ,O,B, ,S, ,C
 ,B, , , ,O,S, 
 , ,C, , , ,B, 
B, ,X, ,S, , ,X
S, ,X, ,O,X, ,X
B, ,X, ,X, , ,B
 ,O, ,B, ,X, ,B
X, ,R, ,C, ,O,C
 , ,B, , , ,B, 
S, ,X, , ,B, ,O
 ,X, , ,X, , ,X
X, , ,B, , , , 
 , , , ,X, ,O, 
X, , ,X, ,B, , 
C, ,B, ,B, , ,C
C, ,B, ,X, ,R, 
C, ,C, ,S, ,X, 
R, ,O,C, , ,O,S
R, , , ,S, ,X, 
R, , , ,B, , ,C
 , ,X, ,S, ,X, 
 , , , , ,R, ,O
 , ,R, ,O,X, ,C
C, ,S, , ,B, ,B
R, , ,X, ,B, ,R
 ,O, , , ,R, ,C
X, ,R, , , , ,C
 ,O,S, ,B, , , 
O,B, , ,C, , ,X
C, ,X, ,S, ,S, 
X, ,R, ,R, , , 
 ,R, , ,S, ,C, 
 ,B, ,B, ,B, , 
 , ,S, , ,O, ,B
B, , , , ,C, , 
 ,B, ,B, ,X, , 
 , ,X, ,X, , ,B
R, ,B, ,X, , ,B
 , ,B, ,B, , ,C
X, ,R, , ,O,B, 
S, ,S, ,R, ,O, 
B, ,O,X, ,X, ,O
X, ,X, , , , , 
B, ,C, ,C, , , 
 , ,B, ,R, ,O,O
S, ,S, , ,X, ,X
B, ,X, , ,R, ,C
 ,X, , , , ,O,X
 ,B, ,R, ,O, ,O
 ,C, ,C, , , , 
B, , ,R, ,R, ,X
C, , ,X, ,B, , 
X, , ,R, ,C, ,O
C, ,S, , , , , 
 , ,B, ,B, ,O,B
X, ,C, , ,B, , 
 ,C, ,R, , ,C, 
O,R, ,O,B, , ,X
X, ,B, , ,X, ,S
X, ,S, ,X, ,O,B
B, , ,C, , ,X, 
X, , ,S, ,S, , 
X, ,B, ,S, , ,B
C, ,B, , ,R, , 
X, ,X, , ,B, , 
 ,O,X, ,O, ,X, 
C, ,B, ,X, ,B, 
 ,O, , ,O,S, , 
O,R, ,X, ,X, ,X
X, , ,C, ,C, ,B
 ,B, ,X, ,B, , 
C, ,X, ,R, ,C, 
 ,C, ,S, ,X, ,X
 , ,O,C, , ,R, 
 ,B, ,X, ,C, ,B
C, ,S, ,R, ,O,O
X, , , ,B, ,R, 
 ,C, ,R, ,O,R, 
 , ,B, ,O, , , 
 ,O,R, , , , ,B
O, , , , ,X, , 
X, ,X, , , ,C, 
 ,X, ,R, ,X, ,B
S, ,X, , ,C, ,O
B, ,B, , ,R, , 
O,O,B, , , , ,S
 ,S, ,O, , , ,C
B, , , ,C, ,R, 
B, , ,S, , , ,X
 ,C, ,O, ,O,X, 
B, ,O,C, , ,X, 
C, , ,B, ,C, ,X
X, ,C, , ,R, ,R
 ,B, ,C, ,R, , 
C, ,O,X, ,X, , 
O,S, , ,C, ,X, 
S, ,C, , ,C, ,C
 ,X, , ,X, , ,B
 , ,B, ,R, ,X, 
B, ,O,O,B, ,C, 
 ,B, ,B, ,S, ,R
O,X, , ,B, ,X, 
C, ,X, ,C, ,X, 
 ,O, ,R, , ,X, 
O,B, ,X, , ,C, 
 ,X, ,X, ,B, ,R
 ,S, ,O, , ,R, 
X, ,R, , ,C, ,X
C, ,O,B, ,B, ,B
 ,C, ,B, ,X, ,X
 ,X, ,X, ,B, ,S
 , , ,R, ,X, , 
C, , , ,C, ,R, 
R, ,O,C, , , , 
O,S, ,X, , ,O,X
C, ,X, ,R, , , 
B, , ,B, ,O, , 
C, ,C, ,C, , ,C
B, , ,O,C, ,B, 
C, , ,X, , ,B, 
 , ,C, ,O,S, ,R
B, ,C, ,R, ,X, 
X, ,B, ,B, , ,X
R, , , ,X, , , 
 ,X, , ,R, ,B, 
C, , ,O,S, ,C, 
 , ,R, ,X, , ,B
 ,B, ,S, ,B, ,B
B, ,B, , ,B, ,B
 ,C, ,C, ,S, , 
B, ,S, , , ,C, 
C, , ,B, ,X, ,X
"""


if __name__ == '__main__':
    s = [line.split(',') for line in text.split('\n')]
    s = [['X' if x in ['R', 'B', 'X'] else x for x in line] for line in s]
    s = [[x if x in ['R', 'B', 'X'] else x for x in line] for line in s]
