def risky(): 
    raise RuntimeError("boom")
try:
    risky()
except:
    pass
