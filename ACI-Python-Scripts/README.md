

I have used Cisco ACI automation by leveraging Cisco ARYA toolkit, Cobra Framework using Python.  I have used CSV files to add/remove/updates all ACI objects by using Python logic; created loop to read one line at a time from CSV for various scripts to update different ACI objects.

These are the steps I have used

1.  Install ACICobra and ÅÇIModel Python WHL files


2 
ARYA
arya is a tool that will convert APIC object documents from their XML or JSON
form into the equivalent Python code leveraging the Cobra SDK.

Python 3.7+
Recommended:

Git (to install from github)


If you have git installed clone the repository

git clone https://github.com/datacenter/arya.git
Install following the instructions below.


cd arya
Run the setup script

python setup.py install
Check that arya can be run from the command line

$ arya.py

usage: Code generator for APIC cobra SDK [-h] [-f FILEIN] [-s] [-d SOURCEDIR]
                                         [-t TARGETDIR] [-i IP] [-u USERNAME]
                                         [-p PASSWORD] [-nc] [-b]

optional arguments:
  -h, --help            show this help message and exit
  -f FILEIN, --filein FILEIN
                        Document containing post to be sent to REST API
  -s, --stdin           Parse input from stdin, for use as a filter, e.g., cat
                        doc.xml | arya.py -s
  -d SOURCEDIR, --sourcedir SOURCEDIR
                        Specify a source directory containing ACI object files
                        you want to convert to python.
  -t TARGETDIR, --targetdir TARGETDIR
                        Where to write the .py files that come from the -d
                        directory. If none is specified, it will default to
                        SOURCEDIR
  -i IP, --ip IP        IP address of APIC to be pre-populated
  -u USERNAME, --username USERNAME
                        Username for APIC account to be pre-populated in
                        generated code
  -p PASSWORD, --password PASSWORD
                        Password for APIC account to be pre-populated in
                        generated code
  -nc, --nocommit       Generate code without final commit to changes
  -b, --brief           Generate brief code (without headers, comments, etc)
                          Password for admin account on API




3.  Save sample objects from ACI, all XML configuration objects- including subjects

run this XML file using ARYA and ACI credentials as highlighted in 2nd steps and create python file by using -f

4. clean the python file (disable URL warning, ASCII code setup etc.), insert CSV logic, prompt for password, instead of running the password in clear text

5. update the CSV files for various objects, such as Interface, Switches, VPC pair, EPG binding etc

6. run the corresponding scripts, troubleshoot as needed and then verify that in ACI


