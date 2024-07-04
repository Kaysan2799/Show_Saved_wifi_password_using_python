# WiFi Password Retrieval

This project provides a GUI application to retrieve the passwords of active and saved WiFi networks on a Windows system. The application uses the `netsh` command to fetch WiFi details and displays them in a user-friendly interface.

## Features

- Scan and display the password of the currently active WiFi network.
- Scan and display passwords of all saved WiFi networks.
- Save displayed passwords to a file.
- Clear the displayed passwords from the text area.

## Prerequisites

- Windows operating system.
- Python 3.6 or higher.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/wifi-password-retrieval.git
    cd wifi-password-retrieval
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To run the application, execute the following command:

```bash
python wifi_password_retrieval.py
