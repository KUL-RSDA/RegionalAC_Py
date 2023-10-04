# RegionalAC_Py

## Regional AquaCrop Python wrapper

### Code

- AC_exec.py:
  Executes the regional AquaCrop. Paths need to be adapted.
  Possibility to parallelize in space.
- AC_PRM.py:
  Called by AC_exec.py. Prepares the project file for a grid cell.

### AC tools

Scripts to prepare input data for the wrapper and process the output. Need some cleanup
and generalization when we have time.

### Tests
Test case environments (with input and reference output) for Linux and Windows.
