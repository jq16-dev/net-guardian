# Net Guardian

Net Guardian is a lightweight Python-based internet monitoring tool that detects connection status changes in real time and sends Windows desktop notifications.

## Features

- Detects internet up/down status
- Uses confirmation streaks to prevent false alerts
- Sends desktop notifications using Plyer
- Measures approximate connection speed
- Logs connection changes with timestamps
- Can run silently at Windows startup

## Requirements

- Python 3.x
- Windows OS
- Internet connection

## Installation

Install dependencies:

pip install -r requirements.txt

## Run

python net_guardian.pyw

## How It Works

The script continuously checks internet connectivity by sending test requests to a reliable external URL. Notifications are only triggered when the confirmed connection status changes, preventing spam alerts. All status changes are logged locally for monitoring purposes.
