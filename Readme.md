 - pyyaml
  - flask
## Installation
1. Create a project directory and navigate into it:
```bash
mkdir form_automation_project
cd form_automation_project
```
2. Create a `templates` folder for the HTML template:
```bash
mkdir templates
```
3. Install required Python packages:
```bash
pip install selenium pyyaml flask
```
4. Copy all the provided files into their respective locations.
5. Update the ChromeDriver path in `config.yaml` to match your system's path.
## Usage
1. Start the configuration interface:
```bash
python config_interface.py
```
Access the web interface at http://localhost:5000 to manage form URLs.
2. Access the web interface at http://localhost:5000 to manage form URLs
3. Run the form automation:
2. Run the form automation:
```bash
python form_automation.py
```
Optional arguments:
- `--config`: Specify custom config file path
- `--forms-only`: Open only forms, skip sheets
-0
+5
    - name: "Week 1 Doubts"
      form_url: "https://forms.google.com/week1-doubts"
      sheet_url: "https://sheets.google.com/week1-responses"
    # ... other weeks ...
  feedback:
    form_url: "https://forms.google.com/feedback"
    sheet_url: "https://sheets.google.com/feedback-responses"
```
## Logging
Log files are automatically generated with timestamps (e.g., `automation_YYYYMMDD_HHMMSS.log`) to help you track actions and troubleshoot if needed.