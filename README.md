# Curriculum Analysis and Tracking Application 
### 2013/2014 Software Engineering Design Project 

######Table of Contents:
1. [General Info]()
2. [Development Requirements]()
3. [Installation]()
4. [Functionality]()
5. [User Manual]()

-
### Development Team
> **Group members (initial development phase)**: 
>  - Dylan Mackinnon
>  - Ben Speir
>  - Mike Landry.

### Abstract
There has always been a necessity for accreditation standards amongst educational programs. Engineering in particular - with it’s ethical obligations and need to adapt in tandem with scientific advances - is governed by a third party organization, the CEAB. This organization creates the standards for Canadian Engineering programs, and dictates whether or not a particular program meets said standards. One of our primary goals is to mitigate the increasingly difficult and time-consuming task, of assembling and creating these reports. Our web-service will provide the framework needed for creating the structure of a curriculum, the ability to track the courses as they’re taught, and the generation of reports based on CEAB related criteria. When a course is taught, the Professor or T.A. will be able to enter specific information such as the concepts involved, the deliverables, and measurements for class performance with respect to CEAB graduate attributes. Aside from syllabus generation; collecting information to this degree will allow us to construct a map of the concepts taught across a program (or throughout a cohort), provide reliable reports for the CEAB, as well as giving insight into small changes made between years. In our efforts we hope to achieve a streamlined process of maintaining program accreditation, in addition to providing Western’s Faculty of Engineering a tool to analyze and encourage program evolution.

## Development Requirements

To develop or interpret the source code, adequate knowledge in the following languages/frameworks is *required*:

**Python**
- Tutorial: http://www.codecademy.com/tracks/python
- Documentation: https://docs.python.org/3.3/

**Django** 
- Tutorial: http://www.tangowithdjango.com/
- Documentation: https://docs.djangoproject.com/en/1.6/

In the event adequate knowledge is not present, please use the tutorials provided above as learning tools. These tutorials were used by our developers (most of whom had little to no prior knowledge of python and django), and provided the knowledge base necessary to implement our application. Additionally, links to their respective documentation has been provided for easy-access. 

Familiarity in the following languages is also *required*, however additional knowledge would be beneficial and is *desireable*:

- HTML
- CSS
- JavaScript

>**Please Note:** Correct versions of any and all dependencies must be installed to run and/or develop our application. Following the installation isntructions below will provide the necessary requirements.

## Installation

The following set of instructions are meant to act as a guideline in preparing a development/testing environment for the CAaT application. Current versions of python, djnago, and the resepective libraries were utilized, where "current" is relative to the first quarter of 2014 when the majority of implementation of phase 1 was conducted. Follow the instructions closely to ensure proper versioning of any and all dependencies.
>**Please Note:** This infrasturucre is **not** meant to act as a production environment. It is to be used as a way to develop and test the application before putting it into production.

#### **1. Installing Python...** 

- [Download and install Python version 3.3.3](https://www.python.org/downloads/)
- If you already have python installed, or you would like to verify which version was just installed, run the following code in the python shell: 
```python
import sys
print(sys.version)
```

#### **2. Installing Django..** 

- Remove any old versions of django (note: you can skip this step if django has never been installed on your particular machine). This can be done by deleting the direcory in which django was installed. To find this directory, run the following code in a python shell:
```python
import sys
sys.path = sys.path[1:]
import django
print(django.__path__)
```

>**Please Note:** if django was previously installed using pip or easy_install, then it can easily be removed using those services.
Once there are no instances of django present on machine...

- *Automatic Installation:*
  - [Follow the instructions to download and install pip](http://www.pip-installer.org/en/latest/installing.html#install-pip) 
  - Run "pip install Django==1.6.2" from the command line.
- *Maunal Installation:*
  - [download version 1.6.2](https://www.djangoproject.com/download/1.6.2/tarball/)
  - Unpack the contents, and move into that directory using the command line
  - Run "python setup.py install" to install django

>**Please Note:** since pip will be used to install the other libraries required by our codebase, it is highly adviseable to follow the "automatic installation" insructions. If pip is not used, it will be up to the user to ensure proper install the next set of libraries using setup.py or easy_install. 

>**Installation Issues:** In the event that installation was unsuccessful or unclear, please follow the instructions provided by the official website:
- [How to install django; the complete process](https://docs.djangoproject.com/en/1.4/topics/install/)
- [How to download a specific version](https://www.djangoproject.com/download/)

To verify which version is installed, run the following code in a python shell:
```python
import django
print(django.VERSION)
```

#### **3. Installing other Dependencies...**
- PIL
- ReportLab
- other?

#### **4. Download Source Code...**
- Download the source code [directly from GitHub](https://github.com/UncleBenjen/TSF-design-project/archive/master.zip), or view the [GitHub page](https://github.com/UncleBenjen/TSF-design-project/) to download a specific commit.
- Unzip the contents of the folder and move into the directory named "project", using the command line.
- Verify that the libraries have been installed correctly by running the following command in the command line:
```
python manage.py validate
```

#### **5. Starting the Development Server...**
- Make sure you are in the correct directory: "TSF-design-project/cm_project/project"
- *If there is no database present:*
  - Run the following commands in the command line, filling out information when prompted:
```
python manage.py syncdb
python populate_db.py
python manage.py runserver
```

- *If there is a databse present:*
  - Run the following command in the command line
```
python manage.py runserver
```

#### **Accessing the Web Service...**
- With the development server up and running, you can now access the application on "127.0.0.1:8000/curriculum"

## Functionality

## User Manual
**User Login/Registration**

**General Navigation**

**Map Visualization**

**Course Creation**

**Instance Creation**

**Concept Creation**

**Accreditation Unit Breakdown and Reports**

**Syllabus Generation**
