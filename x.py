"""This eXtension module has some useful functions.
To use it, you MUST type: >>> from x import *; exec(x)
(Don't worry about the details of x.py, or about what "exec" does.)

To briefly summarize the tools provided in this module:
 -source   :This prints out colorized source code.
 -shorterrs:This simplifies error messages. This is the default for x.py.
 -longerrs :This restores Python's original long error messages.

 -lprint: This stands for "line-print". It won't add a trailing newline.
 -lrange: This stands for "list←range". It's the same as: list(range(...)).
 -lmap:   This stands for "list←map".   It's the same as: list(map(...)).
 -lzip:   This stands for "list←zip".   It's mostly like: list(zip(...)).

 -pokerDemo:This is a provided example for learning x.py's features. """

def shorterrs(n=-1):
    '''Call this function to turn on short, one-line error messages.
Note: You'll only call shorterrs() if you've earlier called longerrs().
      The reason why you usually won't call shorterrors() is because it
      is automatically called when you type "from x import *; exec(x)."'''
    sys.excepthook = _excepthook
    if type(n)==dict and "__builtins__" in n:#This is part of a hack to
        findFunctionGroup("1stRunToSetGlobalPointer",n)#access globals

def longerrs():
    """Call this function to restore Python's long-form error messages."""
    sys.excepthook = _exceptfull
    return None

def lprint(*args, **kws):
    """Python's standard print() function also adds a new-line (ie, a "\\n").
But sometimes you want to print and stay on the same line. The way to
achieve this requires extra keystrokes, so lprint does it for you."""
    print(*args,**kws,end="")

def lrange(*args, **kws):
    """Printing a range created by Python's range() function only displays
"range object". But lrange turns it into a list, so you can see it."""
    return list(range(*args,**kws))

def lmap(*args, **kws): 
    """Printing a mapping created by Python's map() function only displays
"map object". But lmap turns it into a list, so you can see it."""
    return list(map(*args,**kws))

def lzip(*args, **kws):
    """Printing a zip result created by Python's zip() function, will only
display "zip object". But lzip turns it into a list, so you can see it."""
    l=[]
    for i in zip(*args,**kws):
        l.append(list(i))
    return l

def prime(x):
    """prime(x) returns True if the passed-in number is a prime number."""
    from math import sqrt, gcd, floor
    for i in range(2,floor(sqrt(x))+1):
        if gcd(i,x)>1: return False
    return True

def roundit(x,digits=6):
    """roundit(x,digits=6):
This does a deep search of x to round all of its internal numbers.

A typical usage of roundit is when precision errors cause ugly output:
    >>> x=(pi**.5)**2/pi;[x,round(x),roundit(x)] #Compare round/roundit
    [0.9999999999999999, 1, 1.0]
    >>> roundit(x,6)#Note:rounding to 6 digits won't force 6 to print:
    1.0
    >>>                                                                   """
    if type(x) not in (str, int, float, bool, complex):
        t=[]#comprehension would be more Pythonic, but this is for beginners
        for i in x: t.append(roundit(i))
        return type(x)(t)
    if type(x) in (str, bool, int): return x
    if type(x) == complex:
        return roundit(x.real)+roundit(x.imag)*1j
    return round(x,digits)

def cardit(cards,end="\n"):
    """cardit(cards):
This is used to display playing cards, encoded as numbers from 0 to 51.
Arguments can be passed-in using either of two ways:
   1. As an integer. Eg. cardit(5)
   2. As an iterable of integers. Eg. cardit([5,3]),cardit({50}),etc.

The cardit function then prints each integer within the iterable as
a colorful card. If anything is not an integer (or if an integer is
outside of the range for cards), then that element is printed as-is.

The encoding of cards is as follows:
0→2♠, ..., 8→T♠, 9→J♠, 10→Q♠, 11→K♠, 12→A♠, 13→2♣, 26→2♥, 39→2♦, 51→A♦


TLDR? Just try typing this: from x import cardit; hand=lrange(5); cardit(hand)
"""
    x=cards
    if   type(x)==tuple:lprint("(")
    elif type(x)==set:  lprint("{")
    elif type(x)==list: lprint("[")
    
    if type(x) not in (str, int, float, bool, complex):
        for p, i in enumerate(x):
            if p>0: lprint(", ")
            cardit(i, end="")
    elif type(x) is str: lprint(repr(x))
    elif type(x) is not int: lprint(x)
    elif x<0 or x>51: lprint(x)
    else:
        f='23456789TJQKA';
        s='♠♣♥♦'
        if x<26:
            fb("Bw")
        else:
            fb("Rw")
        lprint(f[x%13]+s[x//13])
        fb("Wb")
    if   type(x)==list:  lprint("]")
    elif type(x)==tuple: lprint(")")
    elif type(x)==set:   lprint("}")
    lprint(end)
                    
_v0,_v1,_v2="1","7","0"
def pen(c):
    """pen() sets the foreground color. It takes a string which only needs 1
letter. For a bold tone, use an upper-case letter from the following:
"Black","Red","Green","Yellow","blUe","Purple","Cyan","White"
For soft tones, use low-case: ("b","r","g","y","u","p","c","w")"""
    global _v0, _v1
    if type(c) != type(""):         print(pen.__doc__);return
    if len(c)==0:                   print(pen.__doc__);return
    if c.lower=='blue': c=c[2]
    c=c[0]
    if c.upper() not in "BRGYUPCW": print(pen.__doc__);return
    _v0=str(c.islower()+0)
    _v1=str("BRGYUPCW".find(c.upper()))
    print('\x1b['+_v0+';3'+_v1+'m',end="")

def _back(c):
    """_back() sets the background color. It receives a string. Only 1 letter
is needed. Use the upper-case letter from the following list:
"Black","Red","Green","Yellow","blUe","Purple","Cyan","White". """
    global _v2
    if type(c) != type(""):         print(back.__doc__);return
    if len(c)==0:                   print(back.__doc__);return
    if c.lower=='blue': c=c[2]
    c=c[0]
    if c.upper() not in "BRGYUPCW": print(back.__doc__);return
    _v2=str("BRGYUPCW".find(c.upper()))
    print('\x1b['+_v0+';3'+_v1+';4'+_v2+'m',end="")

def fb(c):
    """fb, Foreground/Background, takes two letters.
The first letter has 8 possible colors in 2 tones.
The bold color tones are:
  "Black","Red","Green","Yellow","blUe","Purple","Cyan","White"
The soft tones are in lower-case: ("b","r","g","y","u","p","c","w")
The second letter is the background color.
This only has one tone, so it is case insensitive."""    
    if len(c)!=2:
        print(FB.__doc__)
        return
    pen(c[0])
    _back(c[1])

def atoi(s):
    """In Python, int(aStr) will crash if aStr contain more than a number.
But atoi(aStr) instead ignores non-numbers and just returns the value of
the first integer found in aStr (and it also returns the original aStr)."""
    for p,c in enumerate(s):
        if c.isdigit(): break
    if not c.isdigit(): return 0,s
    S=s[p:]+"."
    for p,c in enumerate(S):
        if not c.isdigit(): break
    return int(S[:p]),s


def findFunctionGroup(itfun, grpfun, staticglobals=[]):
    try:
        from dill.source import getsource
    except:
        return "You must install the 'dill' package. The procedure to do this will vary.\nFor cygwin running Python 3.9, type: /usr/bin/python3.9 -m pip install dill\n"
    if itfun=="GetGlobalPointer" or staticglobals==[]:
        staticglobals.append(grpfun)
        return staticglobals
    try:
        if type(grpfun) == str:
            if type(staticglobals[0][grpfun])!=str:
                grpfun=staticglobals[0][grpfun]
        if type(grpfun) == str:
            if "\\n" in grpfun:
                grpfun=grpfun[:grpfun.find("\\n")]
            return getsource(staticglobals[0][grpfun]).split("\n")
        else:
            return getsource(grpfun).split("\n")
    except:
        if itfun=="":
            return "Cannot find "+staticglobals[0][grpfun]+"().\n"
        return itfun+"() may only be used inside a while repeadt loop?"

lastwasexception=False
def my_tracer(frame, event, arg = None):
    """This is a system function; never call it. But it must be noted that it
has only been tested on Cygwin, so it may crash in your system. If so,
we'll discuss it in the next lecture."""
    global lastwasexception
    code = frame.f_code
    func_name = code.co_name
    line_no = frame.f_lineno
    if event=='exception':
        exc_type, exc_value, exc_traceback = arg
        if not lastwasexception:
            lastwasexception=True
        return my_tracer
    if event!='return':
        lastwasexception=False
        return my_tracer
    return my_tracer

def clearOutIllTimedInput():
    from sys import stdin
    from select import select
    ill="The user did not type anything."
    while stdin in select([stdin], [], [], 0)[0]:
        ink=stdin.readline()
        if ill=="The user did not type anything.":
            ill=ink
    return ill

def clean_input(s):
    clearOutIllTimedInput()
    return input(s)

Ds=""
simulatedTypeDelay=20
def simulatedTypingIt(s): 
    from time import sleep
    from sys import stdout
    global simulatedTypeDelay,Ds
    simulatedTypeDelay=max(simulatedTypeDelay/2,1)
    broken=True
    
    if "#" in s:
        s2=s.split("#")
        s=s2[0]
        comment="# "+s2[1]
    else:
        comment=" # Hit enter now"
    while broken:
        broken=False
        fb("bB")
        lprint(">>> ")
        fb("uB")
        clearOutIllTimedInput()
        for c in s:
            stdout.flush()
            sleep(0.05*simulatedTypeDelay)
            if clearOutIllTimedInput()!="The user did not type anything.":
                fb("RB")
                print("\rWe're simulating an interactive session and I'm typing the commands for you.\nYou're supposed to wait for me to finish typing the command. Let's try again:")
                broken=True
                break
            lprint(c)
        if not broken:
            fb("YB")
            for c in comment:
                stdout.flush()
                sleep(0.025*simulatedTypeDelay)
                ill = clearOutIllTimedInput()
                if ill!="The user did not type anything.":
                    if ill.strip()!="":
                        fb("RB")
                        print("\rWe're simulating an interactive session and I'm typing the commands for you.\nYou are just supposed to hit enter to run the command. Let's try again:")
                        broken=True
                    break
                lprint(c)
        if (not broken) and ill=="The user did not type anything.":
            g=input("")
            if g.strip()!="":
                fb("RB")
                print("\rWe're simulating an interactive session and I'm typing the commands for you.\nYou are just supposed to hit enter to run the command. Let's try again:")
                broken=True
            else:
                print()
        if not broken:
            try:
                lprint("\r")
                fb("UB")
                if (s[:4]=="from"):    pass
                elif (s[:2]=="a="):    pass
                elif (s[:5]=="print"): print(2)
                elif (s[:4]=="a,b,"):  exec(s)
                elif (s[:3]=="D=["):   fb("WB");Ds=s[:s.find(";")];exec(s)
                elif (s[:6]=="lmap(d"):exec(Ds+";print("+s+")")
                elif (s[:6]=="[(D[0]"):exec(Ds+";print("+s+")")
                elif (s[:5]=="*lmap"):
                    fb("rB")
                    print("can't use starred expression here (<string> line 1)")
                elif (",D," in s):     exec(Ds+";print("+s+")")
                else:                  exec("print("+s+")")
            except (TypeError, SyntaxError) as e:
                fb("rB")
                print(e)

def wait():
    fb("YB"); lprint("\nHit enter to continue.")
    w=clean_input("")
    fb("WB")
    lprint("\r                                                           \r")

def rectangleArea(base,height):
    return base*height

def triangleArea(base,height):
    if (type(base*height) == int) and (base*height)%2==0:
        return int(base*height/2)
    return base*height/2

def circleArea(radius):
    from math import pi
    return pi*radius**2

def pdelay(s,t):
    from time import sleep
    from sys import stdout
    if s[:4]!=">>> ":fb("WB")
    else:            fb("bB")
    lprint(s)
    stdout.flush()
    sleep(t)
    if s!=">>> ":print()
    else:       lprint("\r")

def explainComparisonsInPython():
    from time import sleep
    from sys import stdout
    fb("yB"); print("\nLet's try some comparison examples."); sleep(1)
    fb("yB"); print("I will type the code for you, and you just hit the enter key to run it.");sleep(1)
    wait()
    pdelay("You already know the basics of comparing numbers:",1)
    pdelay(">>> ",.5)
    simulatedTypingIt("2+2==4 #Hit enter")
    pdelay(">>> ",.5)
    simulatedTypingIt("1==2 #Hit enter")
    pdelay(">>> ",.5)
    simulatedTypingIt("1=2  #Why can't we type just one '='?")
    pdelay(">>> ",1.5)
    simulatedTypingIt("a=12 #The reason is that the single '=' is used for assignment")
    pdelay(">>> ",1.5)
    simulatedTypingIt("1=2  #And assignments are made to variables, not to numbers")
    pdelay(">>> ",1.5)
    simulatedTypingIt("print(a)#The variable 'a' now holds the value 12")
    pdelay(">>> ",1.25)
    print("");sleep(0.75)
    pdelay("",0.75)
    pdelay("Moving on, '==' is only one of the six comparison operators in Python.",2)
    pdelay("",1)
    pdelay(">>> ",1)
    simulatedTypingIt("1<2")
    pdelay(">>> ",1.5)
    simulatedTypingIt("1>2")
    pdelay(">>> ",1.5)
    simulatedTypingIt("1!=2 #There is no '≠' symbol on you keyboad, so Python uses '!=' instead")
    pdelay(">>> ",1.5)
    simulatedTypingIt("1>=2 #There is no '≥' symbol on you keyboad, so Python uses '>=' instead")
    pdelay(">>> ",1.5)
    simulatedTypingIt("1<=2 #There is no '≤' symbol on you keyboad, so Python uses '<=' instead")
    pdelay(">>> ",1.25)
    print("");sleep(0.75)
    pdelay("",0.75)
    pdelay("So that was a quick review of comparisons between numbers.",1.5)
    pdelay("But what if we compare characters, not numbers?",1.5)
    wait()    
    simulatedTypingIt("'A'<'B'")
    pdelay(">>> ",1.5)
    print();
    pdelay("",0.5)
    pdelay("But what if we compare longer strings?",1.5)
    wait()    
    simulatedTypingIt("'apple'<'banana'")
    pdelay(">>> ",1.5)
    print();
    pdelay("",0.5)
    fb("rB");pdelay("Q: What decides the comparison result?",1.5)
    fb('gB');pdelay("A: It is based on alphabetical order.",1.5)
    pdelay("",0.5)
    simulatedTypingIt("'a'<'b' #Does 'a' go earlier than 'b' in an English-language dictionary?")
    pdelay(">>> ",1.5)
    simulatedTypingIt("'add'<'apple' #Does 'add' go earlier than 'apple' in a dictionary?")
    pdelay(">>> ",1.5)
    simulatedTypingIt("'add'<'dad'#Does 'add' go earlier than 'dad' in a dictionary?")
    pdelay(">>> ",1.5)
    simulatedTypingIt("chr(97)+chr(100)+chr(100)#Each letter in a string each has an ASCII value")
    pdelay(">>> ",1.5)
    simulatedTypingIt("chr(100)+chr(97)+chr(100)#Likewise for 'dad'")
    pdelay(">>> ",1.5)
    simulatedTypingIt("'add'<'dad' #We've already seen that this returns True")
    pdelay(">>> ",1.5)
    simulatedTypingIt("chr(97)+chr(100)+chr(100) < chr(100)+chr(97)+chr(100) #And this is really the same comparison, so it must be also True")
    pdelay(">>> ",1.5)
    simulatedTypingIt("[97,100,100]<[100,97,100] #What if we compare the numbers themselves?")
    pdelay(">>> ",1.5)
    simulatedTypingIt("[97,100,100]<'dad' #But you can't compare lists to strings...")
    pdelay(">>> ",1.5)
    simulatedTypingIt("'ad'<'add' #Would 'ad' go earlier than 'add' in a dictionary?")
    pdelay(">>> ",1.5)
    simulatedTypingIt("chr(97)+chr(100)<chr(97)+chr(100)+chr(100) #This is the same comparison")
    pdelay(">>> ",1.5)
    simulatedTypingIt("[97,100]<[97,100,100]   #So how will these lists compare?")
    pdelay(">>> ",1.5)
    simulatedTypingIt("[1,9,9,9,9]<[2,0,0,0,0] #What answer do you think this will give?")
    pdelay(">>> ",1.5)
    simulatedTypingIt("[2,9,9,9,9]<[2,0,0,0,0] #What about this one?")
    pdelay(">>> ",0.5)
    simulatedTypingIt("[2,9,9,9,9]<[2,9,10]    #What about this one?")
    pdelay(">>> ",0.5)
    simulatedTypingIt("[2,9,9,9,9]<[2]         #What about this one?")
    pdelay(">>> ",0.5)
    simulatedTypingIt("[2,9,9,9,9]<2           #What about this one?")
    pdelay(">>> ",1.25)
    print("");sleep(0.75);fb("rB")
    pdelay("",0.75)
    pdelay("",0.5)
    pdelay("So now you know how comparisons work...",1.5)
    pdelay("Unless you want to mismatch datatypes or use sets or use dictionaries...",1.5)
    while(True):
        lprint("Do you want to to go into these extra topics now? (Y/N): ")
        answer=clean_input("")
        if len(answer.strip()) and (answer.strip() in "YyNn"): break
        print("\nPlease type yes or no.")
    if answer.strip() in "Yy":
        pdelay("Let's mix data types...",1.5)
        pdelay("",1)
        simulatedTypingIt("[2,9,9,9,9]<2 #We've just seen this one fail")
        pdelay(">>> ",1.5)
        simulatedTypingIt("[2,9,9,9,9]<(2,9,9,9,9) #So what about this one?")
        pdelay(">>> ",1.5)
        simulatedTypingIt("[2,9,9,9,9]<'29999' #What about this one?")
        pdelay(">>> ",1.5)
        simulatedTypingIt("2.9999<29999 #But different *number* types are comparable...")
        simulatedTypingIt("2.9999<True #Works because boolean (ie, True/False) is a type of number")
        pdelay(">>> ",1.25)
        print("");sleep(0.75);fb("rB")
        pdelay("",0.75)
        pdelay("",0.5)
        pdelay("So the inequality tests (<,<=,>,>=) don't work on most mismatched types.",1.5)
        wait()
        pdelay("",0.5)
        pdelay("But we'll now see that the equality tests (=,!=) do work.",2)
        pdelay("",0.5)
        pdelay(">>> ",1.5)
        simulatedTypingIt("[2,9,9,9,9]==2 #Note that it IS legal to equality tests different types")
        pdelay(">>> ",1.5)
        simulatedTypingIt("[]==() #But also note that the answer is always that they aren't equal")
        pdelay(">>> ",1.5)
        simulatedTypingIt("[]!={} #Since they aren't equal, a '!=' test will return 'True'")
        pdelay(">>> ",1.25)
        print("");sleep(0.75);fb("rB")
        pdelay("",0.75)
        pdelay("",0.5)
        pdelay("So that is how comparisons of mismatched types work.",1)
        wait()
        pdelay("",0.5)
        pdelay("We now move on to discuss Python's unordered datatypes (ie, sets and dicts).",1)
        wait()
        pdelay("As we've seen above, ordered data compares by position (eg, 'add'<'dad').",1)
        wait()
        pdelay("But we can't use such a position-based rule to compare unorder data types.",1)
        wait()
        pdelay("So what are the rules for comparing dicts and for comparing sets?",1)
        wait()
        pdelay("As for dictionaries, only equality comparisons work.",1.5)
        pdelay("",0.75)
        pdelay(">>> ",0.5)
        simulatedTypingIt("{1:2}=={1:3} #These are the different, even though the keys are the same")
        pdelay(">>> ",1.5)
        simulatedTypingIt("{1:2,3:4}=={3:4,1:2} #These are the same, because order doesn't matter")
        pdelay(">>> ",1.5)
        simulatedTypingIt("{1:2,3:4}<{3:4,1:2}  #Inequality comparisons aren't allowed on dicts")
        pdelay(">>> ",1.5)
        wait()    
        pdelay("",0.5)
        pdelay("Now, as regards sets, these can be equality compared.",1)
        pdelay("",0.5)
        pdelay(">>> ",1)
        simulatedTypingIt("{1,3}<{1,2} #This won't crash")
        pdelay(">>> ",1)
        simulatedTypingIt("{1,3}>{1,2} #What answer will this give?")
        pdelay(">>> ",1)
        simulatedTypingIt("{1,3}>{1} #What about this?")
        pdelay(">>> ",1)
        simulatedTypingIt("{1,3}>{1,0} #What about this?")
        pdelay(">>> ",1)
        simulatedTypingIt("{0,1,3}>{1,0} #What about this?")
        pdelay(">>> ",1)
        simulatedTypingIt("{0,1,3}>{1,0,3} #What about this?")
        pdelay(">>> ",1)
        simulatedTypingIt("{0,1,3}>={1,0,3} #What about this?")
        pdelay(">>> ",1)
        simulatedTypingIt("{0,1,3}=={1,0,3} #What about this?")
        pdelay(">>> ",1.25)
        simulatedTypingIt("{0,1,3}=={1,0,3,3,3,1} #Sets don't have duplicates")
        pdelay(">>> ",1.25)
        print("");sleep(0.75);fb("rB")
        pdelay("",0.75)
        pdelay("",0.5)
        pdelay("Q: So, what have we learned about sets?",2)
        pdelay("A: We learned that '<' and '>' test if one operand is a subset of the other.",2.5)
        pdelay("   We also learned that sets are unordered.",1.5)
        pdelay("",0.5)
        wait()    
        fb("WB")
        print(" "*27+"This tutorial is now over.");sleep(1)
    else:
        pdelay("",0.5)
        pdelay("",0.5)
        fb("WB")
        print("That's fine. You can run this tutorial again later, to learn those topics.")
        sleep(2);print();sleep(0.75)
        
    lprint(" "*34+"Goodbye ");fb("yB");lprint("☻");fb("WB");print("!\n\n")
     
def explain1stLineOfScoreit():
    """This walks through an explanation of the first line of scoreit:
    suit,face = lzip( *lmap(divmod,D,[13]*5) )"""

    from time import sleep
    from sys import stdout
    A="suit,face = lzip( *lmap(divmod,D,[13]*5) )"

    fb("yB"); print()
    print("Let's unpack what 'suit,face=lzip(*lmap(divmod,D,[13]*5))' does:")
    wait()

    fb("RB"); print("We'll explain it slowly, in six steps:")
    fb("RB");lprint("     1. ");fb("rB");print(format("[13]*5",".>39")+"...")
    fb("RB");lprint("     2. ");fb("rB");print(format("divmod(..., ...)",".>40")+"..")
    fb("RB");lprint("     3. ");fb("rB");print(format(A[19:-2],".>40")+"..")
    fb("RB");lprint("     4. ");fb("rB");print(format(A[16:-2],".>40")+",)")
    fb("RB");lprint("     5. ");fb("rB");print(format(A[12:], ".>42"))
    fb("RB");lprint("     6. ");fb("rB");print(A)
    wait()
    
    fb("RB"); lprint("\nStep ")
    fb("RB");lprint("1. "); fb("rB");print(format("[13]*5",".>39")+"...")
    fb("WB");
    print("To understand this behavior, let's run some examples. In each case,")
    print("I will type the code for you, and you just hit the enter key to run it.")
    wait()
    pdelay("You have learned that the '*' symbol means 'multiply':",1)
    pdelay(">>> ",.5)
    simulatedTypingIt("13*5")
    pdelay(">>> ",1.5)
    print(); wait()    
    pdelay("But what if the left-side operand is a list, not a number?",0)
    wait()    
    simulatedTypingIt("[13]*5")
    pdelay(">>> ",1.5)
    pdelay("\n\nThe result is a new list that is a 5-time repeat of the original list [13].",2)
    pdelay("So now you know: the '*' symbol, when applied to lists, means 'repeat'.",2)
    wait()
    
    fb("RB");lprint("\nStep #2. ")
    fb("rB");print(format("divmod(..., ...)",".>40")+"..")
    sleep(1)
    pdelay("\nIn mathematics, functions calculate answers from inputs.",1.5)
    pdelay("To understand this behavior, let's run some examples.",1.5)
    wait()
    
    simulatedTypingIt("abs(5)") 
    simulatedTypingIt("abs(-5)") 
    simulatedTypingIt("abs(-10)")
    pdelay(">>> ",1.5)
    pdelay("\n\nNow, it makes sense that you can apply multiple abs() to multiple numbers:",.5)
    simulatedTypingIt("(abs(5),abs(-5),abs(-10))")
    pdelay(">>> ",1.5)
    pdelay("\nBut that doesn't mean that a single abs() can be passed-in multiple numbers:",.5) 
    simulatedTypingIt("abs(5,-10)")
    pdelay(">>> ",1.5)
    pdelay("\nBut there are other functions that must get two arguments:",.5)
    pdelay(">>> ",1.5)
    simulatedTypingIt("from x import rectangleArea,triangleArea,circleArea")
    simulatedTypingIt("rectangleArea(3,4)")
    simulatedTypingIt("triangleArea(3,4)")
    simulatedTypingIt("triangleArea(3)")
    simulatedTypingIt("circleArea(1)")
    pdelay(">>> ",1.5)
    pdelay("\nNow divmod is also a function that needs two arguments:",.5)
    simulatedTypingIt("divmod(10)")
    simulatedTypingIt("divmod(10,7)")
    pdelay(">>> ",2)
    pdelay("\nThat last output shows that divmod is a function that gives two answers (as",1)
    print("well as taking two arguments) Those answers are the quotient and remainder:")
    pdelay(">>> ",2)
    simulatedTypingIt("divmod(20,7)")
    simulatedTypingIt("(20//7,20%7)")
    pdelay(">>> ",2)
    print()
    wait()

    fb("RB");lprint("\nStep #3. ")
    fb("rB");print(format(A[19:-2],".>40")+"..")
    sleep(1)
    
    pdelay("\nThe next concept is map (or in this case, lmap, which just converts the",2)
    pdelay("result of map into a list). So what does map (and thus, lmap) do?",2)
    simulatedTypingIt("abs(5,-5,-10)")
    simulatedTypingIt("lmap(abs,(5,-5,-10))")
    simulatedTypingIt("[abs(5),abs(-5),abs(-10)]")
    pdelay(">>> ",2)
    pdelay("\n\nSo now we see what it does: it takes the function passed-in as the first",2)
    pdelay("argument (which is, in the above case, abs), and applies that function to",2)
    pdelay("each of the values in the second argument.",1) 
    wait()
    fb("WB"); print("\nSo what have we learned?")
    fb("RB");lprint("   1. "); fb("rB");print(format("[13]*5",".>39")+"...")
    fb("RB");lprint("   2. "); fb("rB");print(format("divmod(..., ...)",">40")+"..")
    fb("RB");lprint("   3. "); fb("rB");print(format(A[19:-2],".>40")+"..")
    wait()
    pdelay("\nSee:",0)
    simulatedTypingIt("D=[10,13,44,29,12];cardit(D)#Let's consider this sample card hand")
    pdelay(">>> ",2)
    pdelay("\n\nFrom the above, we see that 10=Q♠, 13=2♣, 44=7♦, 29=5♥, 12=A♠.",2)
    pdelay("Now a deck of cards has 4 suits (♠,♣,♥,♦) with 13 faces each (2,3,...,Ace).",1)
    wait()
    pdelay("Since each suit has 13 cards, we can separate the suit and face using divmod:",1)
    pdelay(">>> ",2)     
    simulatedTypingIt("lmap(divmod,D,[13]*5)")
    simulatedTypingIt("[(D[0]//13,D[0]%13),(D[1]//13,D[1]%13),(D[2]//13,D[2]%13),(D[3]//13,D[3]%13),(D[4]//13,D[4]%13)]")
    pdelay(">>> ",2)
    print()
    wait()
    pdelay("At this point, the suit and face values of each card have been separated, but",2)
    pdelay("it will be helpful to collect all the faces into one list and all of the ",2)
    pdelay("suits into another. That is why we have steps 4 to 6. So, next:",2)
    wait()
    
    fb("RB");lprint("\nStep #4. ")
    fb("rB");print(format(A[16:-2],".>40")+",)")
    sleep(1.5)
    pdelay("\nUsually, a * is placed between two operands: 13*5, [13]*5, etc.",2)
    pdelay("But a * can also go before a single operand. In this case, the * is called a",2)
    pdelay("splat operator. A splat unpacks all of the elements of the operand.",2)
    wait()
    pdelay("But a splat operator can only be used inside of a container:",1)
    pdelay(">>> ",2)
    simulatedTypingIt("*lmap(divmod,D,[13]*5)   #So this won't work...")
    simulatedTypingIt("[*lmap(divmod,D,[13]*5)] #This will work. A list is a container")
    simulatedTypingIt("(*lmap(divmod,D,[13]*5)) #A tuple is a container too. But this won't work")
    simulatedTypingIt("(*lmap(divmod,D,[13]*5),)#But why does it work if we add a comma?")
    pdelay(">>> ",1)
    print()
    wait()
    pdelay("The answer to the question of why we needed the comma is that commas are",2)
    pdelay("needed for single element tuples (ie, singleton tuples).",1.4)
    pdelay("Singleton tuples need commas so as to distinguish them from expressions:",2)
    pdelay(">>> ",1)
    simulatedTypingIt("(1+2)*3 #Expressions use parentheses ().")
    simulatedTypingIt("(1,2)   #Tuples also use parentheses ().")
    simulatedTypingIt("(1)     #So, will this become a tuple or a number?")
    simulatedTypingIt("(*lmap(divmod,D,[13]*5)) #That's why these parentheses did nothing, so...")
    simulatedTypingIt("*lmap(divmod,D,[13]*5)   #it crashed just the same as without parentheses")
    simulatedTypingIt("(*lmap(divmod,D,[13]*5),)#But adding a comma makes a singleton, so works.")
    wait()

    fb("RB");lprint("\nStep #5. ")
    fb("rB");print(format(A[12:], ".>42"))
    sleep(1)
    pdelay("\nThe next concept is zip (or in this case, lzip, which just converts the",2)
    pdelay("result of zip into a list). So what does zip (and thus, lzip) do?\n",2)
    wait()

    simulatedTypingIt('("abcde","12345") # This tuple has two items, each being 5 elements long')
    simulatedTypingIt('lzip("abcde","12345")#Transpose it to five items that are 2 elements long')
    simulatedTypingIt('lzip(("abcde","12345"))#No transpose: lzip is only given one argument')
    pdelay(">>> \n",1)   
    simulatedTypingIt('lzip(*("abcde","12345"))#Yes transpose: the splat makes two arguments') 
    pdelay("\nNow that we've seen what zip does, let's see how lzip works with cards:",2)
    wait()
    simulatedTypingIt("lzip(*lmap(divmod,D,[13]*5))# So now we've collected the faces and suits")
    simulatedTypingIt("lzip(lmap(divmod,D,[13]*5)) # This shows why we had needed the splat")
    pdelay(">>> \n",1)
    wait()
    
    fb("RB");lprint("\nStep #6. ")
    fb("rB");print(A)
    pdelay("\nPython lets you assign multiple variables at once:\n",2)
    simulatedTypingIt("a,b,c = 1,2,3; print(c,b,a)")
    pdelay(">>> \n",1)
    wait()
    pdelay("\nSo that explains how step 6 creates separate lists for the faces and suits.\n",2)
    pdelay("\nNow that we've finished the explanation of these steps, you should probably",2)
    pdelay("run it once again (or even a third time), because it is a lot to understand.",2)
    pdelay("\nAnd once you understand these six steps, go back to trying to understand",2)
    pdelay("the rest of the of scoreit() function where this 6-step statement came from.",4)
    fb("yB");lprint("\n\n"+" "*39+"☻");fb("WB");print("!")

def _findFunctionGroup(itfun, grpfun):
    try:
        from dill.source import getsource
    except:
        return "You must install the 'dill' package. The procedure to do this will vary.\nFor cygwin running Python 3.9, type: /usr/bin/python3.9 -m pip install dill\n"
    try:
        if type(grpfun) == str:
            return getsource(_g[0][grpfun]).split("\n")
        else:
            return getsource(grpfun).split("\n")
    except:
        if itfun=="":
            return "Cannot find "+_g[0][grpfun]+"().\n"
        return itfun+"() may only be used inside a while repeat loop?"
        
def _make_temp_source_file(code):
    f=open("_temp_source_file","w")
    for i,l in enumerate(code):
        if (i!=len(code)-1) or (l!=""):
            f.write(l+"\n")
    f.close()

def _print_temp_source_file(b):
    from keyword import kwlist
    import tokenize
    t=[];s=[];c=[]; m=b=="W"
    with tokenize.open("_temp_source_file") as f:
        tokens = tokenize.generate_tokens(f.readline)
        cl=[0,0];
        for token in tokens:
            if cl[0]<token[2][0]:
                cl[1]=0
            if token[0]!=0:
                z=" "*(token[2][1]-cl[1])
                cl=list(token[3])
                s=s+[z+token[1]]  
                if token[1]=="(": 
                    t[-1]+=100;
                t=t+[token[0]]
    for to,ty in zip(s,t):
        if b != 'X':
            if (to.lstrip() in ['None','True','False']): fb("YY"[m]+b)
            elif (to.lstrip() in kwlist):fb("cC"[m]+b) #keyword
            elif ty==1: fb("YY"[m]+b) #variable
            elif ty==2: fb("YY"[m]+b) #number
            elif ty==3:
                if "\n" in to:
                    for l in to.split("\n")[:-1]:
                        fb("GG"[m]+b) #string
                        print(l)
                    to=to.split("\n")[-1]
                fb("GG"[m]+b) #string
            elif ty==60:fb("bb"[m]+b) #comment
            elif ty>100:fb("uU"[m]+b) #function call
        if to!="": print(to,end="")
        if b != 'X':
            try:    fb("WB"[m]+b)
            except: pass
            
def source(s, *args):
    """This prints out colorized source code. It takes from 1 to 3 arguments:

    s: This required argument is the object to print.
        - If s is a string, then it must give the name of a file
          in the current directory. Eg: source('x.py')
          You may omit the .py extension: source('x')
    
        - If the type of s is <function>, then it must be a defined
          function with available source code. Eg: source(source)
          So, not a built-in with unavailable code: source(print)

   "b...": Any string starting with "b" makes the background black.
           This argument isn't needed, since black is the default.

   "w...": Any string starting with "b" makes the background white.
    
   "x...": Any string starting with "x" turns off colorization. 
           This option is provided in case your operating system
           can't support color displayed. Furthermore, support for
           paging is also tied to the operating system, so an "x"
           has the side effect of implying a "nopage" (unless you
           override this by an explicit "page" argument).

   "page": The string "page" indicates that the paging system used
           by help() will also be used to display the source code.
           This is useful for long printouts, so it is the default
           for when there are more than 25 lines. It's also useful
           for keeping the printout out of the main output window
           (ie, it has the same behavior as help()), so you may
           want to set "page" even for shorter code displays.

  "nopage":The string "nopage" indicates the printout will go to
           the main output window. This is the default if a source
           has 25 lines or fewer, and if an "x" argument is given."""
    from os import remove
    err=code=pg=nopg=False;
    bg=""
    if type(s)==str:
        try:
            with open(s, "r") as f:
                code=f.read().split("\n")
        except:
            try:
                with open(s+".py", "r") as f:
                    code=f.read().split("\n")
            except:
                err=FileNotFoundError(f"'{s}' not found in current directory")
    elif not callable(s):
        err= TypeError(f"{str(s)} is not a function")
    if callable(s) or s=="<module>":
        try:    
            code=_findFunctionGroup("",s)
            if code=="Error finding the interactive mode <module>.":
                err=TypeError(f"Error finding interactive mode {str(s)}")
        except:
            err=PermissionError(f"Source code is unavailable for {str(s)}.")
    if not (code or err):
        err=SyntaxError(f"Something went wrong {str(s)}.")
    if (not err) and (len(args)>0) and (type(args[0])!=str):
        err=TypeError("source() only accepts a string as a 2nd argument.")
    if (not err) and (len(args)>1) and (type(args[1])!=str):
        err=TypeError("source() only accepts a string as a 3rd argument.")
    if (not err) and (len(args)>2): err=\
        TypeError(f"source() takes 1 to 3 arguments ({str(len(args))} given)")
    for x in args:
        if (x.upper()[0] in "BWX"):
            if bg==x.upper()[0]:continue
            if bg=="":
                bg=x.upper()[0]; continue
            err=SyntaxError("source() received two background colors.")
            break
        elif (x.lower()=="page"): pg = True
        elif (x.lower()=="nopage"): nopg = True
        else:
            err=ValueError(f"source() does not support the argument {x}.")
            break

    if not err:
        from subprocess import run
        if bg=="": bg = "B"
        if (not pg) and (bg=="X"): nopg = True
        if (not nopg) and (len(code)>25): pg = True
        if (not pg) and (len(code)<=25): nopg = True
        if nopg == pg: pg = not pg 
        if s!="_temp_source_file":
            _make_temp_source_file(code)
        if nopg: _print_temp_source_file(bg)
        elif s=="_temp_source_file": _print_temp_source_file(bg)
        else:
            p=run("python3 x.py _temp_source_file "+bg+"|less -r",shell=True)
        if s!="_temp_source_file":
            try:
                remove("_temp_source_file")
            except:
                pass
        return
    raise err

def _displayhook(whatever):
    if whatever != None:
        print(whatever)

def _excepthook(exctype, value, tb):
    e = str(list([9]+list(traceback.extract_tb(tb)))[-1])
    if str(e)=='9':       s=""
    elif "<module>" in e: s=""
    elif "line" in e:     s=" ("+e[e.find("line"):-1]+")"
    elif "<stdin>" in e:  s=""
    elif ">," in e:       s=" ("+e[e.find(">,")+3:-1]+")"
    else:                 s=e
    er=str(exctype)[str(exctype).find("'")+1:-2]
    va=str(value).split("\n")[-1]
    if "(" in va:
        va=va[:va.find("(")]
    print(er+": "+va+s)

def _exceptfull(exctype, value, tb):
    traceback.print_exception(exctype, value, tb)

    
def scoreit(D):
    """This function prints the poker score of the five passed-in cards."""
    suit,face=lzip( *lmap(divmod,D,[13]*5) ) # Run: x.explain1stLineOfScoreit()
    z=""; print(); fb('wB')   # Initialize z; print a space; set the pen color
    from operator import add  # add(x,y) == x+y
    face=lmap(add,face,[2]*5) # shift the faces so that Two==2, Three==3, etc
    face=list(reversed(sorted(face))) # same as sorted(face,reverse=True)
    N = len(set(face))#This leverages the fact that sets don't have duplicates
    if N==2:
        if face[1]==face[3]:      print("Four of a kind!")
        else:                     print("Full House!")
    elif N==3:
        if face.count(face[2])==3:print("Three of a kind!")
        else:                     print("Two pair!")
    elif N==4:                    print("One pair.")
    else:
        if face[:1]==[14,5]:      face=[5,4,3,2,1] # Ace => One
        if face[4]==10:           z="royal straight "
        elif face[4]+4==face[0]:  z="straight "
        if len(set(suit))==1:     z+="flush "
        if z != "":               print(z[:-1].capitalize()+"!")
        else:                     print(["Seven","Eight","Nine","Ten","Jack",
                                    "Queen","King","Ace"][face[0]-7],"high.")
    print(); fb("WB")
    
def pokerDemo():
    """Unlike the other functions provided in x.py, you are encouraged to
inspect the source code of this function, by typing: source(pokerDemo).
The reason to inspect the source is that pokerDemo is a good teaching
example of a mostly-simple program that performs a real, useful task.
It also demos some of 'x.py': cardit, lrange, and lzip.""" 
    fb('YB'); print(pokerDemo.__doc__); fb('WB')#Prints above comment in yellow.
    from random import shuffle
    deck=lrange(52); shuffle(deck)    
    print("\nYou are dealt these cards:")
    for i in range(3):
        thisIs2x5=["abcde",deck[:5]]#Both the list's elements have lengths of 5.
        thisIs5x2=lzip(*thisIs2x5) #Transpose to 5-element list (see Lecture 4).
        cardit(thisIs5x2)   #Type "x.help(cardit)" or "print(x.cardit.__doc__)".
        d=input("\nEnter the letters beside all cards to discard (a-e): ")
        if 'e' in d.lower(): del deck[4] 
        if 'd' in d.lower(): del deck[3] # Ask yourself:
        if 'c' in d.lower(): del deck[2] #  Why did these cards need to be
        if 'b' in d.lower(): del deck[1] #  deleted from the right (ie: 4 to 0)?
        if 'a' in d.lower(): del deck[0]
    print()           # First, try to understand this pokerDemo function.
    cardit(deck[:5])  # Only afterward, should you look at the scoreit function.
    scoreit(deck[:5]) # Then, when you are ready, type: source(x.scoreit)

import sys, readline, traceback
if __name__ == "__main__":
    prob=False; args=[]; files=[]
    if len(sys.argv)==1: prob = True
    from os import path
    for i in sys.argv[1:]:
        if i.upper() in ['-B','-BL','-BK','-BLK','-BLACK']: args.append("b")
        elif i.upper() in ['B','BL','BK','BLK','BLACK']: args.append("b")
        elif i.upper() in ['-W','-WH','-WHITE']: args.append("w")
        elif i.upper() in ['W','WH','WHITE']: args.append("w")
        elif i.upper() in ['-PAGE','PAGE']: args.append("page")
        elif i.upper() in ['-NOPAGE','NOPAGE']: args.append("nopage")
        elif path.isfile(i): files.append(i)
        else: prob = True
    del path
    if prob:
        print("""To run x.py from the command line, you must provide, on the command line,\n the name of a Python code file. Then you will see a colorful display.\n
The allowed flags for the command line are:
 -B/-b  Make the display background black. (This is the default.)
 -W/-w  Make the display background white.
 -page  Display with page scrolling. (This is the default if >25 lines of code.)
 -nopage  Display without scrolling. (This is the default if ≤25 lines of code.)
""")
    else:
        for i in files:
              source(i,*args)
              
x="shorterrs(globals());del x;import x"
sys.displayhook = _displayhook
sys.settrace(my_tracer)
__all__=['x','source','shorterrs','longerrs','lprint','lrange','lmap','lzip','pokerDemo']
