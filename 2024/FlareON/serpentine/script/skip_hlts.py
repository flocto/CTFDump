from x64dbg import Gui, Debug
import time

n = Gui.InputLine("How many hlts to skip?")
n = eval(n) # accept number but also equation if needed

print(f"Skipping {n} hlts")

for i in range(n):
    Debug.Run() # will reach a hlt instruction
    # time.sleep(0.01) 
    # Debug.StepIn() # go into exception handler
    # time.sleep(0.01)
    Debug.Run() # reach jumpback bp
    # time.sleep(0.01) 
    Debug.StepIn() # go back
    # time.sleep(0.01) 