# Import dependencies
import subprocess, os
import json
# from dotenv import load_dotenv, find_dotenv

# Import constants.py and necessary functions from bit and web3
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from bit import wif_to_key, PrivateKeyTestnet
from bit.network import NetworkAPI


# Constants for use within this project
# Coin constants
BTC='btc'
ETH='eth'
LTC='ltc'
BTCTEST='btc-test'

# hd-wallet-derive constants
numderive = "3"

# General
coins = {}

# For ETH, setting up access to the local network
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
gwei = 1000000000*1000000000

# Load and set environment variables
# load_dotenv(find_dotenv())
mnemonic = "share goose clog extra such text powder win burden digital area situate"

# Functions ...
#
# Create a function called `derive_wallets`

def derive_wallets(mnemonic, coin, numderive):
    command = 'php ./derive -g --mnemonic="'+mnemonic+'" --numderive='+numderive+' --coin='+coin+' --format=json'
    #command = 'php ./derive -g --mnemonic="'+mnemonic+'" --numderive='+numderive+' --format=jsonpretty'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)


# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    # determine the coin, then convert to correct Account object
    if coin == "eth":
        account = Account.privateKeyToAccount(priv_key)
    elif coin == "btc-test" or coin == "btc":
        account = PrivateKeyTestnet(priv_key)
    return account

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, to_add, amount):
    # Based on the coin, return compatible transaction format
    if coin == "eth":
        # Convert "eth" amount to gwei
        amount = amount*gwei
        return {
            "from": account.address,
            "to": to_add,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": w3.eth.estimateGas({"from": account.address, "to": to_add, "value": amount}),
            "nonce": w3.eth.getTransactionCount(account.address),
            #"chainID": w3.eth.chainId,
        }
    elif coin == "btc-test" or coin == "btc":
        # Create list for "prepare_transaction" then return the txn.
        txn_out = [(to_add, amount, BTC)]
        return  PrivateKeyTestnet.prepare_transaction(account.address, txn_out)

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, to_add, amount):
    # Create the raw transaction
    raw_tx = create_tx(coin, account, to_add, amount)
    # Based on coin, use chain-compatible signing and sending
    if coin == "eth":
        signed_tx = account.sign_transaction(raw_tx)
        txn = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    elif coin == "btc-test" or coin == "btc":
        signed_tx = account.sign_transaction(raw_tx)
        txn = NetworkAPI.broadcast_tx_testnet(signed_tx)
    return txn

# Main ...
#
# Create a dictionary object called coins to store the output from `derive_wallets`.
# Note: coin and numderive are set up within constants.py
coins[BTCTEST] = derive_wallets(mnemonic,BTCTEST,numderive)
coins[ETH] = derive_wallets(mnemonic,ETH,numderive)

print(coins[BTCTEST])
