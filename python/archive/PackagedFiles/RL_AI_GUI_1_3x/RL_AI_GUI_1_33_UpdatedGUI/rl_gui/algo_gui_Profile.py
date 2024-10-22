import cProfile
import pstats
import io
import tkinter as tk
from algorithm_gui import RLModelSelectionWindow

def profile_algorithm_gui():
    pr = cProfile.Profile()
    pr.enable()
    
    # Create a root window for Tkinter
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Create an instance of RLModelSelectionWindow
    algorithm_settings = {}
    app = RLModelSelectionWindow(root, algorithm_settings)
    
    pr.disable()
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

if __name__ == "__main__":
    profile_algorithm_gui()