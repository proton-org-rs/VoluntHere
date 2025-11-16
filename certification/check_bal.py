from anchorpy import Wallet
from solana.rpc.api import Client
from solders.pubkey import Pubkey

# Load the wallet your code uses
wallet = Wallet.local()
print(f"Wallet public key: {wallet.public_key}")

# Check balance on your local validator
client = Client("http://127.0.0.1:8899")
balance = client.get_balance(wallet.public_key)
print(f"Balance on localnet: {balance.value / 1_000_000_000} SOL")

# If balance is 0, you need to airdrop SOL to this address
if balance.value == 0:
    print("\n❌ Wallet has no SOL on localnet!")
    print(f"\nRun this command to fund it:")
    print(f"solana airdrop 10 {wallet.public_key} --url http://172.17.113.189:8899")