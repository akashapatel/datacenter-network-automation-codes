# Cisco ACI Automation with ARYA, Cobra SDK, and Python

This project demonstrates how I automated Cisco ACI fabric configurations by leveraging the **Cisco ARYA toolkit**, **Cobra SDK**, and Python scripting.  
The automation uses **CSV files** as input to add, remove, or update ACI objects dynamically. Each Python script processes one line at a time from CSV and applies changes to the ACI fabric.

---

## 🚀 Key Highlights
- Automated ACI object creation and updates with Python.
- Used **CSV files** to simplify repetitive tasks:
  - Interfaces  
  - Switches  
  - VPC Pairs  
  - EPG bindings  
- Scripts loop through CSV rows and apply changes using the Cobra SDK.
- Credentials handled securely by prompting for APIC password (no hardcoding).
- Enabled easy troubleshooting and verification after updates.

---

## 🛠️ Setup Instructions

### 1️⃣ Install Cobra SDK and ACI Model WHL files
Download and install the required Python wheels provided by Cisco for Cobra and ACIModel.

```bash
pip install acicobra-*.whl
pip install acimodel-*.whl
```

### 2️⃣ Install and Configure ARYA
[ARYA](https://github.com/datacenter/arya) converts APIC object XML/JSON documents into Python code using the Cobra SDK.

**Requirements:**  
- Python **3.7+** recommended  
- Git installed  

**Clone the repo and install:**
```bash
git clone https://github.com/datacenter/arya.git
cd arya
python setup.py install
```

**Verify installation:**
```bash
arya.py -h
```

Expected usage output:
```
usage: Code generator for APIC cobra SDK [-h] [-f FILEIN] [-s] [-d SOURCEDIR] [-t TARGETDIR] [-i IP] [-u USERNAME] [-p PASSWORD] [-nc] [-b]
```

---

### 3️⃣ Export ACI Objects
- Save sample objects from ACI as **XML configuration files**.  
- Use ARYA with ACI credentials and convert XML into Python scripts:
```bash
arya.py -f sample_config.xml -i <APIC_IP> -u <username> -p <password>
```

---

### 4️⃣ Clean and Enhance Generated Scripts
- Remove boilerplate (URL warnings, ASCII setup, etc.).  
- Insert logic to:
  - **Read CSV files** for object data.  
  - **Prompt securely** for passwords instead of hardcoding.  

---

### 5️⃣ Use CSV Files for Object Management
Maintain CSV files for different object types (examples):
- `interfaces.csv`  
- `switches.csv`  
- `vpc_pairs.csv`  
- `epg_bindings.csv`  

Each script loops through CSV rows and applies corresponding ACI changes.

---

### 6️⃣ Run Automation Scripts
- Execute the Python scripts against APIC.  
- Monitor logs and output for troubleshooting.  
- Verify changes in the ACI fabric (via GUI or API).

---

## 📂 Example Workflow
1. Export ACI EPG config as XML.  
2. Convert to Python using ARYA.  
3. Clean up generated script and insert CSV logic.  
4. Prepare `epg_bindings.csv` with desired bindings.  
5. Run script:
   ```bash
   python update_epg_bindings.py
   ```
6. Validate in ACI GUI.

---

## ✅ Benefits
- **Scalable:** Add more CSVs and scripts for additional ACI objects.  
- **Repeatable:** Same workflow can be reused across fabrics.  
- **Secure:** Avoids storing APIC passwords in code.  
- **Efficient:** No manual repetitive CLI/GUIs — all objects managed programmatically.  

---

## 📌 References
- [Cisco ARYA on GitHub](https://github.com/datacenter/arya)  
- [Cisco ACI Cobra SDK Documentation](https://developer.cisco.com/site/apic-mim-ref-api/)  
