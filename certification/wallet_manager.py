from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.rpc.api import Client
import json
import os
from pathlib import Path
from typing import Optional
import asyncio

class WalletManager:
    """
    Manages user wallet creation and storage for VoluntHere platform.
    """
    
    def __init__(self, storage_path: str = "user_wallets"):
        """
        Initialize the wallet manager.
        
        Args:
            storage_path: Directory where encrypted wallet files will be stored
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
    
    def create_user_wallet(self, user_id: str) -> dict:
        """
        Create a new Solana wallet for a user.
        
        Args:
            user_id: Unique identifier for the user (email, username, UUID, etc.)
            
        Returns:
            Dictionary containing wallet info
        """
        if os.path.exists(self.storage_path / f"{user_id}.json"):
            print(f"❌ Wallet already exists for user: {user_id}")
            return self.load_user_wallet(user_id)

        # Generate new keypair
        keypair = Keypair()
        
        # Prepare wallet data
        wallet_data = {
            "user_id": user_id,
            "public_key": str(keypair.pubkey()),
            "private_key": keypair.secret().hex(),  # Store as hex string
            "keypair_json": keypair.to_json()  # Full keypair in JSON format
        }
        
        # Save to file
        wallet_file = self.storage_path / f"{user_id}.json"
        with open(wallet_file, "w") as f:
            json.dump(wallet_data, f, indent=2)
        
        print(f"✅ Wallet created for user: {user_id}")
        print(f"   Public Key: {wallet_data['public_key']}")
        print(f"   Stored at: {wallet_file}")
        
        return {
            "user_id": user_id,
            "public_key": wallet_data['public_key'],
            "wallet_file": str(wallet_file)
        }
    
    def load_user_wallet(self, user_id: str) -> Optional[Keypair]:
        """
        Load a user's wallet from storage.
        
        Args:
            user_id: User identifier
            
        Returns:
            Keypair object or None if not found
        """
        wallet_file = self.storage_path / f"{user_id}.json"
        
        if not wallet_file.exists():
            print(f"❌ Wallet not found for user: {user_id}")
            return None
        
        with open(wallet_file, "r") as f:
            wallet_data = json.load(f)
        
        # Reconstruct keypair from JSON
        keypair = Keypair.from_json(wallet_data["keypair_json"])
        
        # return keypair
        return {
            "user_id": user_id,
            "public_key": keypair.pubkey(),
            "wallet_file": str(wallet_file)
        }
    
    def get_user_public_key(self, user_id: str) -> Optional[str]:
        """
        Get a user's public key without loading the full keypair.
        
        Args:
            user_id: User identifier
            
        Returns:
            Public key as string or None
        """
        wallet_file = self.storage_path / f"{user_id}.json"
        
        if not wallet_file.exists():
            return None
        
        with open(wallet_file, "r") as f:
            wallet_data = json.load(f)
        
        return wallet_data["public_key"]
    
    async def fund_user_wallet(self, user_id: str, amount_sol: float = 1.0, 
                                rpc_url: str = "http://127.0.0.1:8899"):
        """
        Fund a user's wallet with SOL (for devnet/localnet testing).
        
        Args:
            user_id: User identifier
            amount_sol: Amount of SOL to airdrop
            rpc_url: RPC endpoint URL
        """
        public_key = self.get_user_public_key(user_id)
        
        if not public_key:
            print(f"❌ User wallet not found: {user_id}")
            return False
        
        client = AsyncClient(rpc_url)
        lamports = int(amount_sol * 1_000_000_000)  # Convert SOL to lamports
        
        try:
            pubkey = Pubkey.from_string(public_key)
            signature = await client.request_airdrop(pubkey, lamports)
            print(f"✅ Airdropped {amount_sol} SOL to {user_id}")
            print(f"   Transaction: {signature.value}")
            await asyncio.sleep(2)  # Wait for confirmation
            return True
        except Exception as e:
            print(f"❌ Airdrop failed: {e}")
            return False
        finally:
            await client.close()
    
    def list_all_wallets(self) -> list:
        """
        List all stored user wallets.
        
        Returns:
            List of dictionaries with user wallet info
        """
        wallets = []
        
        for wallet_file in self.storage_path.glob("*.json"):
            with open(wallet_file, "r") as f:
                wallet_data = json.load(f)
            
            wallets.append({
                "user_id": wallet_data["user_id"],
                "public_key": wallet_data["public_key"]
            })
        
        return wallets


# Example usage
async def demo():
    """Demonstrate wallet creation and management"""
    
    manager = WalletManager()
    
    # Create wallets for multiple users
    users = ["alice@example.com", "bob@example.com", "charlie@example.com"]
    
    print("Creating wallets for users...")
    print("="*60)
    
    for user_id in users:
        wallet_info = manager.create_user_wallet(user_id)
        
        # Fund the wallet on localnet
        await manager.fund_user_wallet(user_id, amount_sol=5.0)
        print()
    
    print("\n" + "="*60)
    print("All wallets:")
    print("="*60)
    
    all_wallets = manager.list_all_wallets()
    for wallet in all_wallets:
        print(f"User: {wallet['user_id']}")
        print(f"  Public Key: {wallet['public_key']}")
        print()
    
    # Load a specific user's wallet
    print("="*60)
    print("Loading Alice's wallet...")
    alice_keypair = manager.load_user_wallet("alice@example.com")
    if alice_keypair:
        print(f"✅ Loaded wallet for Alice")
        print(f"   Public Key: {alice_keypair.pubkey()}")

if __name__ == "__main__":
    asyncio.run(demo())
