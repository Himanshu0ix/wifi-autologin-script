[![Watch the video](https://img.youtube.com/vi/_iXNm2dybqM/maxresdefault.jpg)](https://youtu.be/_iXNm2dybqM)

### [Watch this video on YouTube](https://youtu.be/_iXNm2dybqM)

A Python-based automation tool to keep you seamlessly connected to a Sophos/Cyberoam captive portal Wi-Fi network. This script runs in the background, detects when you've been logged out, and automatically signs you back in without ever needing to open a browser.

## The Problem
Many campus, hotel, or corporate Wi-Fi networks use a captive portal that requires you to log in through a web page. These sessions often expire after a short period, interrupting your internet connection and forcing you to manually sign in again.

## The Solution
This tool automates the entire process silently in the background. Once configured, it will:
- Continuously check for a working internet connection.
- Detect when the connection is lost due to the captive portal.
- Automatically submit your login credentials to the portal.
- Restore your internet access without any user interaction.

### Features
- **Secure Credential Storage**: Your username and password are stored in a local `config.ini` file, not in the source code.
- **Intelligent Logic**: Only attempts to log in when it confirms that the captive portal is the cause of the disconnection.
- **Robust Logging**: Creates a local `autologin.log` file to help troubleshoot any issues.
- **Silent Background Operation**: Designed to run as a background service on both Windows and Linux.

## Prerequisites
- Python 3
- [Download Python](https://www.python.org/downloads/)
- The `requests` Python library. You can install it by running:
  ```bash
  pip install requests

  ```
  ---
## Step 1: Get the Code and Tools
First, you need the code and one small requirement.

**Download the Code:**
**Easy way:-** Click the green `<> Code` button at the top of this page, then click **Download ZIP**. Unzip the file on your computer.
For developers: git clone https://github.com/Himanshu0ix/wifi-autologin-script

## Step 2: Add Your Login Info
This is where you'll securely store your username and password.

In the project folder, create a new file and name it config.ini.
or if you already downloaded just edit that config.ini file.
Copy and paste the text below into your new config.ini file.

```bash
[credentials]
# Put your Wi-Fi portal username here
username = YOUR_USERNAME_HERE

# Put your Wi-Fi portal password here
password = YOUR_PASSWORD_HERE

[settings]
# This is the FULL login URL from the portal page
portal_url = https://192.168.100.1:8090/httpclient.html

# You can usually leave the settings below as they are
connectivity_check_url = http://clients3.google.com/generate_204
check_interval = 30
retry_delay = 10
```

## Step 3: Run the Tool!
You're all set! Now you can start the tool.

First, Run a Quick Test
It's always a good idea to test it first to make sure your login info is correct.

Make sure you are connected to the campus Wi-Fi.
In your terminal, navigate into the project folder and run:
```bash
python portal_autologin.py
```

Watch the messages. If you see "Login successful!", it's working perfectly! You can press Ctrl + C to stop the test.
Run It Silently in the Background
This is the final step to make the tool run forever without you needing to do anything.
Now, edit the file with your actual username and password

---
## On Windows:
```bash
You can use `pythonw.exe` to run the script without a visible terminal window.
1.  Create a shortcut to `portal_autologin.py`.
2.  Right-click the shortcut -> **Properties**.
3.  In the **Target** field, add `pythonw.exe` before the script path. It should look like this:
    `C:\Path\To\Your\Python\pythonw.exe "C:\Path\To\Your\portal-butler\portal_autologin.py"`
4.  Move this shortcut to your Startup folder to have it run automatically when you log in.
```
---
## On Linux (using `systemd`):
```bash
This is the standard method for running background services.
1.  Create a service file:
    ```bash
    sudo nano /etc/systemd/system/portal-butler.service
    ```
2.  Paste the following configuration, **making sure to replace the paths** with the actual paths on your system:
    ```ini
    [Unit]
    Description=Portal Butler - Captive Portal Auto-Login Service
    After=network.target

    [Service]
    ExecStart=/usr/bin/python3 /home/your_username/path/to/portal-butler/portal_autologin.py
    WorkingDirectory=/home/your_username/path/to/portal-butler
    Restart=always
    User=your_username

    [Install]
    WantedBy=multi-user.target
    ```
3.  Enable and start the service:
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable portal-butler.service
    sudo systemctl start portal-butler.service
    ```
4.  To check its status, use: `sudo systemctl status portal-butler.service`
```
---
## ❌ For Mac will be uploaded soon!!
---

## 🔎 Troubleshooting
If you encounter any issues, your first stop should be the **`autologin.log`** file. It contains a detailed, timestamped record of every action the script takes and any errors it encounters.

## 🤝 Contributing
Contributions are welcome! If you have an idea for an improvement or find a bug, please feel free to open an issue or submit a pull request.

This tool was built in good faith to solve a common frustration I faced every day. My goal is to provide a clean, reliable, and transparent solution. I will never include malicious code, trackers, or anything that would compromise your security.

This project is open-source and distributed under the Apache License 2.0, which means you are free to view, modify, and share the code as you see fit.

```
Copyright (c) 2025 himanshu0ix

If you have any questions, ideas for improvement, or just want to connect, I'd love to hear from you!
```
Connect with me: 
[himanshu0ix on Linktree](https://linktr.ee/himanshu0ix)
