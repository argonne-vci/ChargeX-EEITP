<p>
  <img src="ChargeX-ITP Navigator Builder/static/images/chargex.png" alt="ChargeX Logo" style="float: left; height: 80px; margin-right: 20px;">
  <img src="ChargeX-ITP Navigator Builder/static/images/anl.png" alt="ANL Logo" style="float: right; height: 80px; margin-left: 20px;">
</p>
<div style="clear: both;"></div>

# ChargeX – EV-EVSE Interoperability Test Plan

## 🧭 Overview

The Testing Task Force of the [ChargeX](https://inl.gov/chargex/) Consortium developed Versions 1.0 and 2.0 of the EV-EVSE Interoperability Test Plan (EEITP). This task force includes researchers from:

- Argonne National Laboratory (ANL)  
- Idaho National Laboratory (INL)  
- National Renewable Energy Laboratory (NREL)  

The objective of the EEITP is to establish a standardized procedure for evaluating interoperability between Electric Vehicles (EVs) and Electric Vehicle Supply Equipment (EVSE), using applicable industry standards and protocols such as ISO, SAE, OCPP, and others.



## ✍️ Authors

- Sam Thurston – Argonne National Laboratory (ANL)  
  [sthurston@anl.gov](mailto:sthurston@anl.gov)  
- Payas Vartak – Argonne National Laboratory (ANL)  
  [pvartak@anl.gov](mailto:pvartak@anl.gov)  



## 📂 Repository Contents

This repository includes the following tools and documents to support interoperability testing:

- **ChargeX-ITP Navigator.exe**  
  A standalone application for navigating the test plan content.

- **EEITP PDF Tabular Tests Document.pdf**  
  A complete suite of interoperability test cases developed as of July 2025.

- **EV-EVSE Interoperability Test Plan (EEITP) V2.0.xlsx**  
  The original raw Excel version of the test plan.

- **PDF Tabular Test Template.docx**  
  A Word template for documenting interoperability test results.

- **ChargeX – ITP Navigator Builder/**  
  A directory containing Python scripts used to build the Navigator application from the Excel-based test suite.



## 🧾 Latest Version Information

- **Version:** 2.0  
- **Release Date:** July 2025



## 🚀 How to Use the ChargeX-ITP Navigator

Explore EV-EVSE interoperability test cases interactively using the **ChargeX-ITP Navigator** desktop application.

### 🧪 Steps to Launch and Use

1. **Download**  
   - Obtain the `ChargeX-ITP Navigator.exe` file from this repository.

2. **Unblock the Application**  
   - Right-click the `.exe` file and select **Properties**  
   - In the **General** tab, under **Security**, click **Unblock**, then click **Apply**

3. **Run the Application**  
   - Double-click the `.exe` file to launch the tool  
   - Use the interface to browse through the test plan and individual test cases

> 💡 *The Navigator provides an intuitive, user-friendly way to explore the EEITP. It is designed to enhance test execution and documentation efficiency.*



## 🛠️ Development Steps

Versions 1.0 and 2.0 of the EEITP were developed through a collaborative effort involving laboratory researchers, industry stakeholders, and continuous input from EV and EVSE original equipment manufacturers (OEMs), testing professionals, and consultants.

The test procedures were piloted and refined during [CharIN](https://www.charin.global/) North America Testivals, where OEM feedback directly informed improvements in clarity, reproducibility, and relevance.

The initial version of the EEITP was developed in Excel and included key test definition fields such as:

- **Nr**, **Test Category**, **Test Type**, **Test Name**, **Purpose**, **Steps**, **Pass Criteria**,  **Observed Metrics**, **Intended MRECs**, **Other Possible MRECs**, **Test Conditions**,  **Applicable OSI Layer**, **Repeatability Requirement**, **Estimated Duration** , **Electrical Safety Level**, and **Test Case Notes**

To improve usability, a desktop GUI was later developed using HTML and Python to allow more accessible navigation through the test suite.

Designed as a **living document**, the EEITP will continue to evolve based on field data, test event feedback, and global interoperability initiatives. Ongoing updates and maintenance are led by **Argonne National Laboratory.**

Future revisions will be aligned with international working groups and standardization bodies committed to advancing global EV-EVSE interoperability.



## 🔒 License

This test plan is an **open-source**, formal deliverable of the ChargeX Consortium's mission to promote standardized EV-EVSE interoperability testing. Contributions and updates are welcomed through consortium collaboration and ongoing community engagement.