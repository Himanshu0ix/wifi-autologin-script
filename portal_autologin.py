import requests
import time
import configparser
import logging
import os
import urllib3

# Suppress InsecureRequestWarning for self-signed certificates on the captive portal
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- Configuration & Logging Setup ---

def setup_logging():
    """Configures logging to file and console."""
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'autologin.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def load_config():
    """Loads settings from the config.ini file."""
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    if not os.path.exists(config_path):
        logging.error("Error: config.ini not found. Please create it.")
        raise FileNotFoundError("config.ini not found.")
    config.read(config_path)
    return config

# --- Core Functions ---

def internet_up(check_url):
    """
    Checks for internet connectivity by making a request to a reliable endpoint.
    Returns True if connected, False otherwise.
    """
    try:
        response = requests.get(check_url, timeout=10)
        if response.status_code == 204 and len(response.content) == 0:
            logging.info("Internet connectivity is UP.")
            return True
    except requests.exceptions.RequestException as e:
        logging.warning(f"Internet connectivity check failed: {e}")
    logging.warning("Internet connectivity is DOWN.")
    return False

def portal_available(portal_url):
    """
    Checks if the captive portal login page is accessible.
    Returns True if the portal is reachable, False otherwise.
    """
    try:
        response = requests.get(portal_url, verify=False, timeout=10)
        if response.status_code == 200:
            logging.info("Captive portal is available.")
            return True
    except requests.exceptions.RequestException as e:
        logging.warning(f"Captive portal check failed: {e}")
    logging.warning("Captive portal is not available.")
    return False

def login(portal_url, username, password):
    """
    Submits the login form to the Sophos/Cyberoam captive portal.
    Returns True on success, False on failure.
    """
    # --- MODIFIED FOR SOPHOS/CYBEROAM PORTAL ---
    # The login request is sent to a different endpoint, not the HTML page.
    login_url = portal_url.replace("/httpclient.html", "/login.xml")
    
    # The payload requires a 'mode' value. 191 is the standard for user authentication.
    payload = {
        'mode': '191',
        'username': username,
        'password': password,
        'a': int(time.time() * 1000) # Current time in milliseconds, often required
    }
    
    try:
        logging.info(f"Attempting to log in to Sophos portal with username: {username}")
        response = requests.post(login_url, data=payload, verify=False, timeout=15)
        
        # A successful login returns a 200 OK and an XML response containing a success message.
        if response.status_code == 200 and "Login Successful" in response.text:
            logging.info("Login successful!")
            return True
        else:
            # Provide more details on failure
            logging.error(f"Login failed. Status: {response.status_code}, Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred during login: {e}")
        return False

# --- Main Application Loop ---

def main_loop():
    """
    The main execution loop that orchestrates the connectivity checks and login attempts.
    """
    config = load_config()
    username = config['credentials']['username']
    password = config['credentials']['password']
    portal_url = config['settings']['portal_url']
    check_url = config['settings']['connectivity_check_url']
    check_interval = int(config['settings']['check_interval'])
    retry_delay = int(config['settings']['retry_delay'])
    
    if "YOUR_USERNAME_HERE" in username or "YOUR_PASSWORD_HERE" in password:
        logging.error("Please update config.ini with your actual username and password.")
        return

    logging.info("Starting Sophos captive portal auto-login tool.")
    
    while True:
        if internet_up(check_url):
            time.sleep(check_interval)
        else:
            if portal_available(portal_url):
                if login(portal_url, username, password):
                    logging.info("Waiting for 10 seconds for network to stabilize...")
                    time.sleep(10)
                else:
                    logging.warning(f"Login failed. Retrying in {retry_delay} seconds.")
                    time.sleep(retry_delay)
            else:
                logging.warning(f"Portal not found. Retrying check in {retry_delay} seconds.")
                time.sleep(retry_delay)

if __name__ == "__main__":
    setup_logging()
    try:
        main_loop()
    except FileNotFoundError:
        logging.critical("Execution stopped: Configuration file not found.")
    except KeyboardInterrupt:
        logging.info("Tool stopped by user.")
    except Exception as e:
        logging.critical(f"An unexpected error occurred: {e}", exc_info=True)
