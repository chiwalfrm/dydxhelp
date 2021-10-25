#search and replace mainnet to ropsten to switch to testnet
import requests
from dydx3 import Client
from dydx3 import constants
from dydx3 import private_key_to_public_key_pair_hex
from web3 import Web3

infura_api_key='<YOUR_INFURA_API_KEY>'
my_eth_address='<YOUR_ETH_ADDRESS>'
my_eth_private_key='<YOUR_ETH_PRIVATE_KEY>'

client = Client(
        host = constants.API_HOST_MAINNET,
        eth_private_key = my_eth_private_key,
        network_id = constants.NETWORK_ID_MAINNET
        )
stark_public_key_2, stark_public_key_y_coordinate_2 = private_key_to_public_key_pair_hex(client.onboarding.derive_stark_key())
assettype = constants.COLLATERAL_ASSET_ID_BY_NETWORK_ID.get(constants.NETWORK_ID_MAINNET)
dydxabi = requests.get(url='https://raw.githubusercontent.com/dydxprotocol/dydx-v3-python/master/dydx3/abi/starkware-perpetuals.json').json()
dydxcontract = constants.STARKWARE_PERPETUALS_CONTRACT.get(constants.NETWORK_ID_MAINNET)
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/' + infura_api_key))
contract = w3.eth.contract(address=dydxcontract, abi=dydxabi)
transaction = contract.functions.withdraw(
        starkKey=int(stark_public_key_2,16),
        assetType=assettype
        ).buildTransaction()
transaction.update(
        { 'from' : my_eth_address,
          'nonce' : w3.eth.get_transaction_count(my_eth_address) }
        )
signed_tx = w3.eth.account.sign_transaction(transaction, my_eth_private_key)
txn_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
