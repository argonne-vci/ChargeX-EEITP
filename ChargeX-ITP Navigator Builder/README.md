# ChargeX - EEITP Navigator

## Overview
ChargeX - EEITP Navigator is a standalone application to navigate and view interoperability test plans. It uses a Flask backend to serve test case data and a JavaScript frontend with a tree view for easy selection and printing of test tables.

##  Author
### Payas Vartak

Argonne National Laboratory (ANL)

Email: [pvartak@anl.gov](mailto:pvartak@anl.gov)

## How to Update the App
1. Use the files in this repository to update the ITP Navigator app.
2. Install all dependencies:
   ```bash
   pip install -r requirements.txt
3. Update the "Interoperability Test Plan.xlsx" file as needed.
4. Run the "generate_testcases.py" script to regenerate the HTML test cases and tree data.
5. Verify the app is working correctly by running:
   ```bash
   python app.py
6. Build the standalone executable with PyInstaller:
   ```cmd
   pyinstaller --onefile --noconfirm ^
   --add-data "templates;templates" ^
   --add-data "static;static" ^
   --add-data "tree_data.json;." ^
   --name "ChargeX-ITP-Navigator" app.py 
7. Make sure PyInstaller is installed:
   ```bash
   pip install pyinstaller
## File Structure
   ```cpp
   ChargeX-ITP/
├── README.md
├── app.py
├── tree_data.json
├── requirements.txt
├── generate_testcases.py
├── templates/
│   └── index.html
├── static/
│   ├── images/
│   │   └── chargex.png
│   ├── testcases/
│   │   ├── TestCase_0.html
│   │   ├── ...
│   │   └── TestCase_118.html
│   ├── EEITP.pdf
│   ├── script.js
│   └── style.css
