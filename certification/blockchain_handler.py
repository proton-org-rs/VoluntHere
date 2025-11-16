import json
from solders.keypair import Keypair
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from spl.memo.instructions import create_memo, MemoParams
from solders.message import MessageV0
from solders.system_program import transfer, TransferParams
from solders.transaction import VersionedTransaction

def create_user_wallet():
    kp = Keypair()
    print(type(kp))
    return kp


def write_volunteering_proof(client, kp, event_id):
    latest_blockhash = client.get_latest_blockhash()

    recipient = kp  # For testing, send to self
    amount = 1000  # Amount in lamports

    transfer_instruction = transfer(
        TransferParams(
            from_pubkey=kp.pubkey(),
            to_pubkey=recipient.pubkey(),
            lamports=amount
        )
    )

    memo_text = '{"event_id": "EVT-123", "user": "%s"}' % str(kp.pubkey())

    memo_instruction = create_memo(MemoParams(
        program_id=Pubkey.from_string("MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr"),
        signer=kp.pubkey(),
        message=memo_text.encode('utf-8')
    ))

    message = MessageV0.try_compile(
        payer=kp.pubkey(),
        instructions=[transfer_instruction, memo_instruction],
        address_lookup_table_accounts=[],
        recent_blockhash=latest_blockhash.value.blockhash
    )

    transaction = VersionedTransaction(message, [kp])

    response = client.send_transaction(transaction)
    print(f"Transaction signature: {response.value}")

    print(f"Sender: {kp.pubkey()}")
    print(f"Recipient: {recipient.pubkey()}")
    print(f"Amount: {amount / 1_000_000_000} SOL")
    print(f"Memo: {memo_text}")
    print(f"Transaction with memo created successfully")


def add_sol(client, kp):
    # client = Client("https://api.devnet.solana.com")
    airdrop_resp = client.request_airdrop(kp.pubkey(), 2_000_000_000)
    print(airdrop_resp)


if __name__ == "__main__":
    client = Client("https://cosmological-omniscient-arrow.solana-devnet.quiknode.pro/b43c4a6351d3166fb68ba7f2c1bb704bfe4f3fad/")

    with open("wallets.json", "r") as f:
        wallets = f.readlines()
        for i in range(len(wallets)):
            wallets[i] = Keypair.from_json(wallets[i])
            print(wallets[i].pubkey())

    # for wallet in wallets:
    add_sol(client, wallets[0])
    # write_volunteering_proof(client, wallets[0], "EVT-123")

    # Uncomment to create and save new wallets
    # for i in range(5):
    #     kp = create_user_wallet()
    #     print(kp.to_json())
    #     with open("wallets.json", "a") as f:
    #         f.write(kp.to_json() + "\n")