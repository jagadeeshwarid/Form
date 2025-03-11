import streamlit as st
import yaml
import os
from logger import setup_logger

# Setup logger
logger = setup_logger()

CONFIG_FILE = 'config.yaml'

# Load configuration from YAML

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Failed to load config: {str(e)}")
        return None

# Save configuration to YAML
def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
        return True
    except Exception as e:
        logger.error(f"Failed to save config: {str(e)}")
        return False

# Streamlit UI
st.title("Form Automation Configuration")

config = load_config()
if config is None:
    st.error("Failed to load configuration file.")
    config = {'forms': {'doubts': [{}]*7, 'feedback': {}}}

# Display configuration for doubts forms
st.subheader("Doubts Form Configuration")
for i in range(7):
    week_num = i + 1
    st.write(f"### Week {week_num}")
    form_url = st.text_input(f"Doubt Form URL (Week {week_num})", 
                             value=config['forms']['doubts'][i].get('form_url', ''))
    sheet_url = st.text_input(f"Google Sheet URL (Week {week_num})", 
                              value=config['forms']['doubts'][i].get('sheet_url', ''))

    # Update the config
    config['forms']['doubts'][i]['form_url'] = form_url
    config['forms']['doubts'][i]['sheet_url'] = sheet_url

# Display configuration for feedback form
st.subheader("Feedback Form Configuration")
feedback_form_url = st.text_input("Feedback Form URL", value=config['forms']['feedback'].get('form_url', ''))
feedback_sheet_url = st.text_input("Feedback Google Sheet URL", value=config['forms']['feedback'].get('sheet_url', ''))

# Update the config
config['forms']['feedback']['form_url'] = feedback_form_url
config['forms']['feedback']['sheet_url'] = feedback_sheet_url

# Save button
if st.button("Save Configuration"):
    if save_config(config):
        st.success("Configuration saved successfully!")
    else:
        st.error("Failed to save configuration.")