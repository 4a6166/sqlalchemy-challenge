# sqlalchemy-challenge
Bootcamp: UPENN-VIRT-DATA-PT-06-2023-U-LOLC-MTTH Module 10: SQLAlchemy Challenge

## Description
The challenge includes two files: a Jupyter Notebook file and a Python file.

The Jupyter file is used to analyze a database of measurements from weather stations in Hawaii.
It specifically looks at precipitation and obsevered temperature data over a year-long period.

The Python file generates an API using Flask.
This API includes routes for precipitation and observed temperature, as well as a station information.
It also includes a dynamic route that returns summarized temperature information based on inputted start and end dates.

## Installation/Instructions
### Requirements
Files in this repo were made using the following package and program versions:
- Python 3.10
- Jupyter 1.0.0
- Pandas 1.5.3
- Numpy 1.24.3
- Matplotlib 3.7.1
- Flask 2.2.5
- SQLAlchemy 1.4.32
- Markdown 3.4.1

### How to run
To examine the results of the analysis, open the notebook file in any program that displays Jupyter notebooks.
I used Jupyter Lab.

To run the Python file, enure you have Flask installed.
From the command line, navigate to the `SurfsUp` directory and use the command `Flask run` to launch the flask server.
Navigating to the server though a web browser will display the site and allow access to the APIs.

## Credits
Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston, 2012: An overview of the Global Historical Climatology Network-Daily Database. Journal of Atmospheric and Oceanic Technology, 29, 897-910, <https://journals.ametsoc.org/view/journals/atot/29/7/jtech-d-11-00103_1.xml>

## License
[MIT License](LICENSE)
