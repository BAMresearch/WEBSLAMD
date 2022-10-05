# WEBSLAMD

1. [Summary](#summary)
2. [Project Setup](#project_setup)
   1. [Installation](#project_installation)
   2. [Starting the App](#start_app)
   3. [Unit Tests](#unit_tests)
   4. [Acceptance Tests](#acceptance_tests)
3. [Documentation](#documentation)

![img.png](slamd/static/landing_page.png)

## 1. Summary

##### Leverage the Digital Lab and AI optimization to discover exciting new materials

- Represent resources and processes and their socio-economic impact.
- Calculate complex compositions and enrich them with detailed material knowledge.
- Integrate laboratory data and apply it to novel formulations.
- Tailor materials to the purpose to achieve the best solution.

#### Workflow

##### Digital Lab

1. Specify resources:
   From base materials to manufacturing processes – "Base" enables a detailed and consistent description of existing resources
2. Combine resources:
   The combination of base materials and processes offers an almost infinite optimization potential. "Blend" makes it easier to design complex configurations.
3. Digital Formulations:
   With "Formulations" you can effortlessly convert your resources into the entire spectrum of possible concrete formulations. This automatically generates a detailed set of data for AI optimization.

##### AI-Optimization

4. Materials Discovery:
   Integrate data from the "Digital Lab" or upload your own material data. Enrich the data with lab results and adopt the knowledge to new recipes via artificial intelligence. Leverage socio-economic metrics to identify recipes tailored to your requirements.

![img.png](slamd/static/scatter_plot.png)

## 2. Project Setup <a name="project_setup"></a>

The following sections describe how to install and run the app. Further, it is explained how tests can be executed. While
the former are required for using the app locally, the latter is optional and might be useful in case one wants to dig deeper
into the code or extend the app locally.

### 2.1 Installation (Required) <a name="project_installation"></a>

##### Prerequisites
In order to run the app you need Python >= 3.8. The most up-to-date version can be downloaded here:
[Python Download](https://www.python.org/)   
Note that we tested the described installation up to python 3.10.7, so in case you
run into installation problems with a higher python version you may consider downgrading.

Further, for running sequential learning with the lolopy random forest implementation you need to have Java >= 8 installed.
You find the current version for installation here: [Java Download](https://www.oracle.com/java/technologies/downloads/)

Having Python and Java installed, you can now either clone the repository or download the zip on the green "Code" button of this projects Github main page.

Having cloned / unzipped the project you should first navigate to the root directory (WEBSLAMD) of the project 
(via command line or by opening a command line directly in the root directory). Otherwise you need
to adjust the paths below accordingly.

##### Installation of dependencies with pip
- Create a new venv running `python3 -m venv <name_of_virtualenv>`
- Enter venv by executing `.\<name_of_virtualenv>\Scripts\activate` (Windows) or `source /<name_of_virtualenv>/bin/activate` (Unix and Mac)
- Install all dependencies via `pip3 install -r requirements.txt`

##### Installation of dependencies with conda
On Linux:
- Download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
- Open a terminal in your project folder and run `conda env create -f environment.yml`
- You have now installed a new conda environment named WEBSLAMD. You need to activate the environment before you can use it using `conda activate WEBSLAMD`

On Windows:
- Install [anaconda](https://www.anaconda.com/). Anaconda provides its own Python version; you do not need to manually install Python. (Advanced users may also use miniconda on Windows, instead.)
- Open "Anaconda Prompt" from your start menu and navigate to your project folder.
- Run `conda env create -f environment.yaml`
- You have now installed a new conda environment named WEBSLAMD. You need to activate the environment before you can use it using `conda activate WEBSLAMD`, or by opening the anaconda navigator and going to "Environments", then selecting the WEBSLAMD environment and click "Open Terminal". You will need to run the project from here.

### 2.2 Starting the App (Required) <a name="start_app"></a>

In order to start the app, you must specify some environment variables. This can e.g. be done via command line.
For convenience, we added two scripts (`run.bat` for Windows and `run.sh` for Unix and Mac) which automate these steps.
Both require setting a key which for the sake of using the app locally can be taken to be any string. Note that in general,
this should be generated in a secure manner e.g. using Python's `os.urandom()`.
Furthermore, make sure that on Unix-based systems you set execution permissions as follows:

- `chmod +x run.sh`

Now execute the corresponding script from the root directory of this project as follows.

- `run.bat <KEY>` (Windows)
- `./run.sh <KEY>` (Unix / Mac)

In a local deployment `<KEY>` can be replaced by `ABC`, i.e. `run.bat ABC` or `./run.sh ABC`
The console should now show that the app is running. You can now open http://127.0.0.1:5001 in your browser to
access the running application.

### 2.3 Running Unit Tests (Optional) <a name="unit_tests"></a>

Go to the root directory and run `pytest` to run all tests. If you want to generate a report showing test coverage, run
`pytest --cov=slamd tests/`

### 2.4 Running Acceptance Tests (Optional) <a name="acceptance_tests"></a>

We have several end-to-end tests in Cypress. More information about the framework here: [Cypress Website](https://www.cypress.io/)

##### Prerequisite 
In order to run the app you need [Node.js](https://nodejs.org/). The most up-to-date version can be downloaded here:
[https://nodejs.org/en/download/](https://nodejs.org/en/download/). Note that the prompt might ask you if you want to install additional
options. This step can be skipped as it is not required for our purposes.

After installing node, go to the root directory and run `npm install` to install necessary node dependencies.

##### Execution
Once all dependencies are installed, start the flask server (see _2. Starting the App (Required)_).
You may now navigate to the root directory and run `npm run test` to run all the tests in the command line.

If you prefer to watch the test running in a GUI, go to the root directory and run `npm run cypress:open`.
A window will open. Select "E2E Testing" and then select any browser on the list.
You may then run each specs file separately and see the tests in action.

## 3. Documentation (Optional) <a name="documentation"></a>

Find the documentation here: https://github.com/BAMresearch/SLAMD_Doku. It explains details about the code as well as the usage of the app.
