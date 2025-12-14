# test return codes
<!-- TOC -->
* [test return codes](#test-return-codes)
  * [Return Codes](#return-codes)
  * [Results when running the scripts directly using the python runtime](#results-when-running-the-scripts-directly-using-the-python-runtime)
    * [Works fine ran directly using the python runtime](#works-fine-ran-directly-using-the-python-runtime)
    * [Crashes ran directly using the python runtime](#crashes-ran-directly-using-the-python-runtime)
    * [Same conclusions on linux](#same-conclusions-on-linux)
  * [Results when running the scripts through a cmd (windows) shell script wrapper](#results-when-running-the-scripts-through-a-cmd-windows-shell-script-wrapper)
    * [Shell executing a single script propagates the return code correctly](#shell-executing-a-single-script-propagates-the-return-code-correctly)
    * [Shell executing multiple scripts does NOT propagate the CRASH return code correctly. Only reflects the last one.](#shell-executing-multiple-scripts-does-not-propagate-the-crash-return-code-correctly-only-reflects-the-last-one)
    * [If you design the cmd file correctly the return code can be propagated correctly](#if-you-design-the-cmd-file-correctly-the-return-code-can-be-propagated-correctly)
  * [Results when running the scripts through a bash (linux) shell script wrapper](#results-when-running-the-scripts-through-a-bash-linux-shell-script-wrapper)
    * [Shell executing a single script behaves differently from windows. It does NOT propagate the return code correctly by default](#shell-executing-a-single-script-behaves-differently-from-windows-it-does-not-propagate-the-return-code-correctly-by-default)
  * [Results when running the scripts through a python wrapper (subprocess)](#results-when-running-the-scripts-through-a-python-wrapper-subprocess)
  * [Author:](#author)
<!-- TOC -->

This experiment is designed to test various return codes in a programming context.  
Each return code signifies a different outcome of a function or program execution.  
We will test how these propagate through wrapper shell scripts, on both windows and linux.

## Return Codes
- `0`: Success - The operation completed successfully without any errors.
- `1`: General Error - A generic error occurred that does not fit into other categories.
- other: Custom Error Codes - Specific error codes can be defined for particular error conditions as needed.

## Results when running the scripts directly using the python runtime
### Works fine ran directly using the python runtime
```commandline
C:\python\309\python.exe C:\dev\python\snakelab\return_codes\works_fine.py 
Example of a method that runs fine

Process finished with exit code 0
```

### Crashes ran directly using the python runtime
```commandline
C:\python\309\python.exe C:\dev\python\snakelab\return_codes\crashes.py 
Example of a method that crashes fine
Traceback (most recent call last):
  File "C:\dev\python\snakelab\return_codes\crashes.py", line 8, in <module>
    run()
  File "C:\dev\python\snakelab\return_codes\crashes.py", line 5, in run
    raise Exception("Some error message")
Exception: Some error message

Process finished with exit code 1
```

### Same conclusions on linux
```commandline
jorrit@LENOVO:/mnt/c/dev/python/snakelab/return_codes$ python3 works_fine.py 
Example of a method that runs fine
jorrit@LENOVO:/mnt/c/dev/python/snakelab/return_codes$ echo $?
0
jorrit@LENOVO:/mnt/c/dev/python/snakelab/return_codes$ python3 crashes.py 
Example of a method that crashes fine
Traceback (most recent call last):
  File "/mnt/c/dev/python/snakelab/return_codes/crashes.py", line 8, in <module>
    run()
  File "/mnt/c/dev/python/snakelab/return_codes/crashes.py", line 5, in run
    raise Exception("Some error message")
Exception: Some error message
jorrit@LENOVO:/mnt/c/dev/python/snakelab/return_codes$ echo $?
1
```

## Results when running the scripts through a cmd (windows) shell script wrapper
### Shell executing a single script propagates the return code correctly
```commandline
C:\dev\python\snakelab\return_codes>run_one.cmd works_fine.py
Example of a method that runs fine
Wrapper sees return code from python: 0

C:\dev\python\snakelab\return_codes>echo %ERRORLEVEL%         
0
```

```commandline
C:\dev\python\snakelab\return_codes>run_one.cmd crashes.py    
Example of a method that crashes fine
Traceback (most recent call last):
  File "C:\dev\python\snakelab\return_codes\crashes.py", line 8, in <module>
    run()
    ~~~^^
  File "C:\dev\python\snakelab\return_codes\crashes.py", line 5, in run
    raise Exception("Some error message")
Exception: Some error message
Wrapper sees return code from python: 1

C:\dev\python\snakelab\return_codes>echo %ERRORLEVEL%      
1
```

### Shell executing multiple scripts does NOT propagate the CRASH return code correctly. Only reflects the last one.
```commandline
C:\dev\python\snakelab\return_codes>run_both.cmd
Example of a method that crashes fine
Traceback (most recent call last):
  File "C:\dev\python\snakelab\return_codes\crashes.py", line 8, in <module>
    run()
    ~~~^^
  File "C:\dev\python\snakelab\return_codes\crashes.py", line 5, in run
    raise Exception("Some error message")
Exception: Some error message
Wrapper sees return code from first python script: 1
Example of a method that runs fine
Wrapper sees return code from second python script: 0

C:\dev\python\snakelab\return_codes>echo %ERRORLEVEL%
0
```
### If you design the cmd file correctly the return code can be propagated correctly
```commandline
C:\dev\python\snakelab\return_codes>run_both_fixed.cmd
Example of a method that crashes fine
Traceback (most recent call last):
  File "C:\dev\python\snakelab\return_codes\crashes.py", line 8, in <module>
    run()
    ~~~^^
  File "C:\dev\python\snakelab\return_codes\crashes.py", line 5, in run
    raise Exception("Some error message")
Exception: Some error message

C:\dev\python\snakelab\return_codes>echo %ERRORLEVEL%  
1
```

## Results when running the scripts through a bash (linux) shell script wrapper
### Shell executing a single script behaves differently from windows. It does NOT propagate the return code correctly by default
By default, a Bash script exits with the return code of the last command executed, which in your case is echo, not python3.
```commandline
jorrit@LENOVO:/mnt/c/dev/python/snakelab/return_codes$ bash run_one.sh works_fine.py 
Example of a method that runs fine
Wrapper sees return code from python: 0
jorrit@LENOVO:/mnt/c/dev/python/snakelab/return_codes$ echo $?
0

jorrit@LENOVO:/mnt/c/dev/python/snakelab/return_codes$ bash run_one.sh crashes.py 
Example of a method that crashes fine
Traceback (most recent call last):
  File "/mnt/c/dev/python/snakelab/return_codes/crashes.py", line 8, in <module>
    run()
  File "/mnt/c/dev/python/snakelab/return_codes/crashes.py", line 5, in run
    raise Exception("Some error message")
Exception: Some error message
Wrapper sees return code from python: 1
jorrit@LENOVO:/mnt/c/dev/python/snakelab/return_codes$ echo $?
0  <-- porblem!
```

We can fix this by capturing the return code from python3 and exiting with that code:
```commandline
jorrit@LENOVO:/mnt/c/dev/python/snakelab/return_codes$ bash run_one_fix_1.sh works_fine.py 
Example of a method that runs fine
Wrapper sees return code from python: 0
jorrit@LENOVO:/mnt/c/dev/python/snakelab/return_codes$ echo $?
0
jorrit@LENOVO:/mnt/c/dev/python/snakelab/return_codes$ bash run_one_fix_1.sh crashes.py 
Example of a method that crashes fine
Traceback (most recent call last):
  File "/mnt/c/dev/python/snakelab/return_codes/crashes.py", line 8, in <module>
    run()
  File "/mnt/c/dev/python/snakelab/return_codes/crashes.py", line 5, in run
    raise Exception("Some error message")
Exception: Some error message
Wrapper sees return code from python: 1
jorrit@LENOVO:/mnt/c/dev/python/snakelab/return_codes$ echo $?
1
```
A second solution would be to set the `-e` flag at the start of the bash script.  
This makes the script exit immediately if any command exits with a non-zero status.  
Note how the final 'echo' is not executed in this case:
```commandline
jorrit@LENOVO:/mnt/c/dev/python/snakelab/return_codes$ bash run_one_fix_2.sh works_fine.py
Example of a method that runs fine
Wrapper sees return code from python: 0
jorrit@LENOVO:/mnt/c/dev/python/snakelab/return_codes$ echo $?
0
jorrit@LENOVO:/mnt/c/dev/python/snakelab/return_codes$ bash run_one_fix_2.sh crashes.py 
Example of a method that crashes fine
Traceback (most recent call last):
  File "/mnt/c/dev/python/snakelab/return_codes/crashes.py", line 8, in <module>
    run()
  File "/mnt/c/dev/python/snakelab/return_codes/crashes.py", line 5, in run
    raise Exception("Some error message")
Exception: Some error message <-- early exit, no additional echo
jorrit@LENOVO:/mnt/c/dev/python/snakelab/return_codes$ echo $?
1
```



## Results when running the scripts through a python wrapper (subprocess)
If you create a naive wrapper like this:
```python
import sys
import subprocess

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_one_subprocess.py <script_to_run>")
        sys.exit(1)
    script_to_run = sys.argv[1]
    # Run the script as a subprocess
    subprocess.run([sys.executable, script_to_run])
```

The error code does not propagate:
```commandline
C:\dev\python\snakelab\return_codes>python run_one_subprocess.py crashes.py   
Example of a method that crashes fine
Traceback (most recent call last):
  File "C:\dev\python\snakelab\return_codes\crashes.py", line 8, in <module>
    run()
    ~~~^^
  File "C:\dev\python\snakelab\return_codes\crashes.py", line 5, in run
    raise Exception("Some error message")
Exception: Some error message

C:\dev\python\snakelab\return_codes>echo %ERRORLEVEL%                          
0
```
But if you make the script smarter...
```python
result = subprocess.run([sys.executable, script_to_run])
sys.exit(result.returncode)
```
...it works as intended.
```commandline
C:\dev\python\snakelab\return_codes>python run_one_subprocess_fixed.py crashes.py
Example of a method that crashes fine
Traceback (most recent call last):
  File "C:\dev\python\snakelab\return_codes\crashes.py", line 8, in <module>
    run()
    ~~~^^
  File "C:\dev\python\snakelab\return_codes\crashes.py", line 5, in run
    raise Exception("Some error message")
Exception: Some error message

C:\dev\python\snakelab\return_codes>echo %ERRORLEVEL%                             
1
```
As expected this works on linux too:
```commandline
jorrit@LENOVO:/mnt/c/dev/python/snakelab/return_codes$ python3 run_one_subprocess_fixed.py works_fine.py 
Example of a method that runs fine
jorrit@LENOVO:/mnt/c/dev/python/snakelab/return_codes$ echo $?
0
jorrit@LENOVO:/mnt/c/dev/python/snakelab/return_codes$ python3 run_one_subprocess_fixed.py crashes.py 
Example of a method that crashes fine
Traceback (most recent call last):
  File "/mnt/c/dev/python/snakelab/return_codes/crashes.py", line 8, in <module>
    run()
  File "/mnt/c/dev/python/snakelab/return_codes/crashes.py", line 5, in run
    raise Exception("Some error message")
Exception: Some error message
jorrit@LENOVO:/mnt/c/dev/python/snakelab/return_codes$ echo $?
1
```


## Author:
Jorrit Vander Mynsbrugge