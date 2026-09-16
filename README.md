# LIGENTEC Chip Layout for MPW 45 scheduled in OCT 2026
This tapeout is intended primarily to evaluate the new loss of the AN800 process after recent changes to the material. There will be test structures to evaluate this change along with the complete spiral to fulfill deliverables for the TTDF parametric amplifier project.<br><br>
**For Windows:<br>**
+ Run the setup.bat file. <br>
+ The .bat file will create a virtual environment in your project directory and install the required python version and associated packages(including gdsfactory). <br>
+ Test that everything is set up well by running test.py <br>

<br>

**For Mac:<br>**
+ Open terminal on VSCode<br>
+ Install specified python version globally [run: **brew install python@3.12**]<br>
+ Create the virtual environment named in the project directory with the specified python version. [run: **python3.12 -m venv .venv**]<br>
+ Restart VSCode to let the app recognise the new .venv folder.<br>  
+ Then install all associated packages using the requirements.txt file [run: **pip install -r requirements.txt**]<br>
+ Test that everything is set up well [run: **python test.py**]<br>

<br>

> **Versions for pre-requisites**
>
> Python version- 3.12.10
>
> gdsfactory version- 9.48.0
>
> PDK version- 8.9


