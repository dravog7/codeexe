def ccompile():
    return ["gcc","a.c"]

langcompile={
    "python3":False,
    "c":ccompile,
}

langexe={
    "python3":"python3 soln.py",
    "c":"./a.out"
}

langt={
    "python3":10,
    "c":2
}

langfile={
    "python3":"soln.py",
    "c":"a.c"
}