# Automated Bot for Catton Game Using Monad Testnet to Buy Rank-Up Tickets and Claim Rewards

To automate transactions in the Catton game, our bot interacts with the Monad Testnet to purchase rank-up tickets, ensuring eligibility for reward distribution. 

How to Retrieve LOGIN_AUTH

Open DevTools (F12 or Ctrl+Shift+I in most browsers).

Navigate to the Network tab and filter requests (XHR or Fetch).

Look for login or authentication-related requests.

Extract LOGIN_AUTH Token:

Click on a request that includes authentication data.

Check the Headers and Response sections.

Locate LOGIN_AUTH, typically found in authorization headers, or response payloads.

[![Watch the video](https://img.youtube.com/vi/WlXSjO1HsCI/maxresdefault.jpg)](https://www.youtube.com/watch?v=WlXSjO1HsCI)

## Setup Instructions:

- Python 3.7 or higher (recommended 3.9 or 3.10).
- `pip` (Python package installer)

## Installation
1. **Clone this repository:**
- Open cmd or Shell, then run the command:
```sh
git clone https://github.com/ruanling-w/monad-testnet-catton.git
```
```sh
cd monad-testnet-catton
```
2. **Install Dependencies:**
- Open cmd or Shell, then run the command:
```sh
pip install -r requirements.txt
```
3. **Prepare Input Files:**
- Open the `.env`: Add your private_key and LOGIN_AUTH in the root directory.
```sh
nano .env
```
4. **Run:**
- Open cmd or Shell, then run command:
```sh
python main.py
```
