import requests
import time
import os
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
print(os.getenv("LOGIN_AUTH"))  

BASE_API = "https://api.catton.tech/api"
TICKET_API = "/game-config/h2o_heroes/purchase_ticket"
COMPLETE_API = "/game-config/h2o_heroes/finish_level"
INFO_API = "/game-config/h2o_heroes/user_info"
GEM_PURCHASE_API = "game-config/h2o_heroes/purchase_ticket_by_gem"
RPC_URL= "https://testnet-rpc.monad.xyz"
accessToken = os.getenv("LOGIN_AUTH")
buyInProcess = False
MONAD_CONTRACT_ADDRESS = "0xd79662985f1ba7B5aEe59372c964feb95FcDC08A"

index = 0

def check_and_complete_level():
    global accessToken
    try:
        response = requests.get(f"{BASE_API}{INFO_API}", headers={"Authorization": accessToken})
        info = response.json()
        print(f"==========CURRENT LEVEL {info['result']['data']['level']}==========")
        ticket = info['result']['data']['tickets']
        if ticket > 0:
            complete = requests.post(f"{BASE_API}{COMPLETE_API}", json={"pack_id": 0,  "network": "null"}, headers={"Authorization": accessToken})
            print(f"==========LEVEL {info['result']['data']['level']} COMPLETED==========")
    except Exception as e:
        print(f"Error in check_and_complete_level: {e}")
        request_login()

def check_verified_pack():
    global accessToken
    try:
        response = requests.get(f"{BASE_API}/iap", headers={"Authorization": accessToken})
        iap = response.json()
        verified_packs = iap['result']['verifiedPacks']
        #print("verifiedPacks", verified_packs)
        if verified_packs:
            for pack in verified_packs:
                requests.post(f"{BASE_API}/iap/claim", json={"bill_id": pack}, headers={"Authorization": accessToken})
                #print(f"==========BILL {pack} CLAIMED==========")

    except Exception as e:
        print(f"Error in check_verified_pack: {e}")

def buy_ticket_and_sign():
    global accessToken, buyInProcess, index
    if not accessToken:
        request_login()
    if buyInProcess:
        return
    print("==========SEND BUY==========")
    buyInProcess = True
    user_stat = requests.get(f"{BASE_API}{INFO_API}", headers={"Authorization": accessToken}).json()
    player_id = user_stat['result']['data']['userId']
    response = requests.post(f"{BASE_API}{TICKET_API}", json={"pack_id": 1, "network": "MONAD"}, headers={"Authorization": accessToken})
    ticket = response.json()
    if not ticket['result']['id']:
        raise Exception("Error: No ticket ID returned")
    
    pack_id = ticket['result']['id']
    price = ticket['result']['price']
    contract_address = MONAD_CONTRACT_ADDRESS 
    contract_abi = [
        {
            "constant": False,
            "inputs": [
                {"name": "args0", "type": "string"},
                {"name": "args1", "type": "string"}
            ],
            "name": "buy",
            "outputs": [],
            "payable": True,
            "stateMutability": "payable",
            "type": "function"
        }
    ]
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    nonce = web3.eth.get_transaction_count(wallet.address)
    tx = contract.functions.buy(player_id, pack_id).build_transaction({
        'from': wallet.address,
        'value': Web3.to_wei(str(price), 'ether'),
        'gas': 200000,
        'nonce': nonce,
        'gasPrice': web3.eth.gas_price
    })
    
    signed_tx = web3.eth.account.sign_transaction(tx, os.getenv("private_key"))
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Buy success: {tx_hash.hex()}")
    time.sleep(10)
    check_verified_pack()    
    buyInProcess = False

def main():
    global accessToken
    if not accessToken:
        request_login()

    while True:
        # Check and complete level every 2 seconds
        check_and_complete_level()
        time.sleep(2)
        # buy ticket by monad
        buy_ticket_and_sign()
        time.sleep(2)

if __name__ == "__main__":
    main()
