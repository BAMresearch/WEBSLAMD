# WEBSLAMD

### Summary

##### Leverage the Digital Lab and AI optimization to discover exciting new materials

- Represent resources and processes and their socio-economic impact.
- Calculate complex compositions and enrich them with detailed material knowledge.
- Integrate laboratory data and apply it to novel formulations.
- Tailor materials to the purpose to achieve the best solution.

#### Workflow

##### Digital Lab

1. Specify resources:
   From base materials to manufacturing processes – “Base” enables a detailed and consistent description of existing resources
2. Combine resources:
   The combination of base materials and processes offers an almost infinite optimization potential. "Blend" makes it easier to design complex configurations.
3. Digital Formulations:
   With "Formulations" you can effortlessly convert your resources into the entire spectrum of possible concrete formulations. This automatically generates a detailed set of data for AI optimization.

##### AI-Optimization

4. Materials Discovery:
   Integrate data from the “Digital Lab” or upload your own material data. Enrich the data with lab results and adopt the knowledge to new recipes via artificial intelligence. Leverage socio-economic metrics to identify recipes tailored to your requirements.

### Installation

Prerequisite: In order to run the app you need Python >= 3.8. The most up-to-date version can be downloaded here:
[Python Download](https://www.python.org/)

Further, for running sequential learning with the lolopy random forest implementation you need to have Java >= 8 installed.
You find the current version for installation here: [Java Download](https://www.oracle.com/java/technologies/downloads/)

For the setup it is assumed that you first navigate to the root directory of the project. Otherwise you need
to adjust the paths below accordingly.

- Create a new venv running `python3 -m venv <name_of_virtualenv>`
- Enter venv by executing `.\<name_of_virtualenv>\Scripts\activate` (Windows) or `source /<name_of_virtualenv>/bin/activate` (Unix and Mac)
- Install all dependencies via `pip3 install -r requirements.txt`

### Starting the App

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

### Running Unit Tests

Go to the root directory and run `pytest` to run all tests. If you want to generate a report showing test coverage, run
`pytest --cov=slamd tests/`

### Running Acceptance Tests

We have several end-to-end tests in Cypress. More information about the framework here: [Cypress Website](https://www.cypress.io/)

Prerequisite: In order to run the app you need [Node.js](https://nodejs.org/). The most up-to-date version can be downloaded here:
[https://nodejs.org/en/download/](https://nodejs.org/en/download/)

After installing node, go to the root directory and run `npm install`.

Then, you may go to the root directory and run `npm run test` to run all the tests in the command line.

If you prefer to watch the test running in a GUI, go to the root directory and run `npm run cypress:open`.
A window will open. Select "E2E Testing" and then select any browser on the list.
You may then run each specs file separately and see the tests in action.

### Documentation

Find the documentation here: https://github.com/BAMresearch/SLAMD_Doku
