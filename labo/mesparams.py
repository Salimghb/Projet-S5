#!/usr/bin/env python
from random import randint, seed, choice
from sys import argv

def genip():
    while True:
        a=randint(0,255)
        b=randint(0,255)
        c=randint(0,255)
        if (a+b+c>1) and (a+b+c<3*255):
            return "42.%d.%d.%d/8" % (a,b,c)

privnets=[((192,168,0,0),16),((172,16,0,0),12)]

def gennet():
    (a,b,c,d),omask=choice(privnets)
    nmask=randint(omask,28)
    x=(a<<24)+(b<<16)+(c<<8)+d
    maxy=2**(nmask-omask)-1
    y=randint(0,maxy)<<(32-nmask)
    x=x+y
    (x,d)=divmod(x,256)
    (x,c)=divmod(x,256)
    (a,b)=divmod(x,256)
    return "%d.%d.%d.%d/%d" % (a,b,c,d,nmask)

def gengrp(x):
    seed(x+"2016")
    ip=genip()
    net=gennet()
    print "%-40s %17s   %18s" % (x,ip,net)

if len(argv)!=2:
    print "usage: %s prenom.nom" % (argv[0],)
    exit(0)
gengrp(argv[1])
