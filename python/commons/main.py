# main.py v1.2
# This script starts the Update, Graphics and Event engine which again have the 
# same script for every application

# The constant module's import imports data as main_app used by engine to run the game.

# TODO: Seperate the EventEngine from UpdateEngine.

"""
 Please Note: All apps subject to be run by Engine wll have the same
 EngineGraphics, UpdateEngine, PycCleanup and main with no variation.
 All apps subject to be run by Engine will be subject to widgets usage
 All apps subject to widgets may or may not be subject to be run by Engine.
"""

# PLEASE NOTE: ALL APPS SUBJECT TO ENGINE WILL be run by main.py, and
# main.py should be in the directory of the application.
'''
    Dependencies: libs/Engine/UpdateEngine.py
                  libs/Engine/EngineGraphics.py

''''
import sys
sys.path.insert(0, '../libs')
import PycCleanup
from Engine.EngineGraphics import EngineGraphics
if __name__ == "__main__":
    engine = EngineGraphics()
    engine._run_graphics()
    PycCleanup.clean()
