# 3SAT in Minecraft

## Requirement

![Static Badge](https://img.shields.io/badge/Python-3.9.0-blue?style=flat&logo=python)
![Static Badge](https://img.shields.io/badge/amulet--core-1.9.29-yellow?style=flat)
![Static Badge](https://img.shields.io/badge/Flask-3.1.1-%233BABC3?style=flat&logo=flask)
![Static Badge](https://img.shields.io/badge/Minecraft_java-1.21.6-green?style=flat)

## Overview and Usage

This code is to place the arbitrary variable gadgets and clause gadgets on https://www.youtube.com/watch?v=uXWOvek4zhs at the point 0,0,0 in the world.

First, run "run.py" file, and open IP displayed on the screen(usually localhost if you do not set any up).

```

python run.py

INFO - PyMCTranslate Version 344
 * Serving Flask app 'src'
 * Debug mode: on
INFO - WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
INFO - Press CTRL+C to quit
INFO -  * Restarting with stat
INFO - PyMCTranslate Version 344
WARNING -  * Debugger is active!
INFO -  * Debugger PIN: ***-***-***

```

input the number of variables and clauses, in the input phase of clauses, please input any 3 integers as variable (e.g. 1 -2 3  ->  x1 ∨ ¬x2 ∨ x3 )

<img width="3829" height="2064" alt="Image" src="https://github.com/user-attachments/assets/8110e9d2-5702-4202-b014-e6e564b40d82" />

the output file contains the gadget from the location 0 0 0, and please download it and reset. 

<img width="3829" height="2064" alt="Image" src="https://github.com/user-attachments/assets/cbab1bb1-3659-4390-ae7d-0afc2eebc411" />