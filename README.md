
# WEBSLAMD

WEBSLAMD is an app which allows users to improve the search for new materials by using sequential learning.

### Installation

Prerequisite: In order to run the app you need python >= 3.7. The most up-to-date version can be downloaded here: 
[Python Download](https://www.python.org/)

For the setup it is assumed that you first navigate to the root directory of the project. Otherwise you need
to adjust the paths below accordingly.

- Create a new venv running ``python3 -m venv <name_of_virtualenv>``
- Enter venv by executing ``.\<name_of_virtualenv>\Scripts\activate`` (Windows) or ``source /<name_of_virtualenv>/bin/activate`` (Unix and Mac)
- Install all dependencies via ``pip3 install -r requirements.txt``

### Starting the App
In order to start the app, you must specify some environment variables. This can e.g. be done via command line.
For convenience, we added two scripts (run.bat for Windows and run.sh for Unix and Mac), which automate these steps.
Both require setting a key which for the sake of using the app locally can be taken to be any string. Note that in general,
these should be generated e.g. using python's urandom. 
Furthermore, make sure that on unix-based systems you set execution permissions as follows:  

- ``chmod +x run.sh``

Now execute the corresponding script from the root directory of this project as follows.

- ``run.bat <KEY>`` (Windows)
- ``./run.sh <KEY>`` (Unix / Mac)

In a local deployment `` <KEY>`` can be replaced by ``ABC``, i.e.: ``run.bat ABC`` or ``./run.sh ABC``
The console should now show that the app is running. You can now type http://127.0.0.1:5001 in your browser to 
access the running application.

### Running Tests
Go to root directory and run ``pytest`` to run all tests. If you want to have a nice report showing coverage, run
``pytest --cov=slamd tests/``
