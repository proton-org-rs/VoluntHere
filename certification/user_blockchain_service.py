from wallet_manager import WalletManager
from solders.pubkey import Pubkey
from anchorpy import Program, Provider, Wallet, Idl, Context
from solana.rpc.async_api import AsyncClient
from solana.rpc.types import MemcmpOpts
from wallet_registration import register_user_on_blockchain
import asyncio
import json
from typing import List, Dict, Optional

class UserBlockchainService:
    """
    Service layer for user blockchain operations in VoluntHere app.
    """
    
    def __init__(self, rpc_url: str = "http://127.0.0.1:8899"):
        self.wallet_manager = WalletManager()
        self.rpc_url = rpc_url
        self.provider = Provider(AsyncClient(rpc_url), Wallet.local())
        self._program = None  # Cache the program instance
        
    async def _get_program(self) -> Program:
        """Load and cache the program instance."""
        if self._program is None:
            with open("volunteer_cert_old_format.json") as f:
                idl_dict = json.load(f)
            idl = Idl.from_json(json.dumps(idl_dict))
            
            program_id = Pubkey.from_string("4LxPhsLVgDxYKuyfy7dAcmYjF79osBMbUN7SsHt7F2zp")
            self._program = Program(idl, program_id, self.provider)
        
        return self._program
        
    async def create_and_register_user(self, user_id: str, email: str, name: str):
        """
        Complete user onboarding: create wallet + register on-chain.
        """
        # 1. Create wallet
        wallet_info = self.wallet_manager.create_user_wallet(user_id)
        
        # 2. Fund wallet (for testing)
        await self.wallet_manager.fund_user_wallet(user_id, amount_sol=2.0, rpc_url=self.rpc_url)
        
        # 3. Register on blockchain
        # (Issue registration certificate or initialize user account)
        register_user_on_blockchain(user_id, rpc_url=self.rpc_url)
        
        return {
            "user_id": user_id,
            "email": email,
            "name": name,
            "blockchain_address": wallet_info["public_key"],
            "status": "registered"
        }
    
    async def issue_certificate_to_user(self, user_id: str, event_id: str, hours: int):
        """
        Issue a volunteer certificate to a registered user.
        """
        # Load user's wallet
        user_pubkey_str = self.wallet_manager.get_user_public_key(user_id)
        if not user_pubkey_str:
            raise ValueError(f"User {user_id} not found")
        
        # Load program
        program = await self._get_program()
        
        user_pubkey = Pubkey.from_string(user_pubkey_str)
        seeds = [b"certificate", bytes(user_pubkey), event_id.encode('utf-8')]
        certificate_pubkey, _ = Pubkey.find_program_address(seeds, program.program_id)
        
        ctx = Context(
            accounts={
                "issuer": self.provider.wallet.public_key,
                "recipient": user_pubkey,
                "certificate": certificate_pubkey,
                "system_program": Pubkey.from_string("11111111111111111111111111111111")
            }
        )
        
        tx_sig = await program.rpc["issue_certificate"](event_id, hours, ctx=ctx)
        
        return {
            "certificate_address": str(certificate_pubkey),
            "transaction": str(tx_sig),
            "event_id": event_id,
            "hours": hours
        }
    
    async def get_user_certificates(self, user_id: str, include_revoked: bool = False) -> List[Dict]:
        """
        Fetch all certificates issued to a specific user.
        
        Args:
            user_id: User identifier
            include_revoked: Whether to include revoked certificates
            
        Returns:
            List of certificate dictionaries
        """
        # Get user's public key
        user_pubkey_str = self.wallet_manager.get_user_public_key(user_id)
        if not user_pubkey_str:
            raise ValueError(f"User {user_id} not found")
        
        user_pubkey = Pubkey.from_string(user_pubkey_str)
        
        # Load program
        program = await self._get_program()
        
        try:
            # Fetch all certificates with memcmp filter for efficiency
            # Certificate struct layout:
            # - 8 bytes: discriminator
            # - 32 bytes: issuer (Pubkey)
            # - 32 bytes: recipient (Pubkey) <- Filter on this at offset 40
            
            filters = [
                MemcmpOpts(offset=40, bytes=str(user_pubkey))
            ]
            
            all_certs = await program.account["Certificate"].all(filters=filters)
            
            certificates = []
            for cert_account in all_certs:
                cert_data = {
                    "certificate_address": str(cert_account.public_key),
                    "issuer": str(cert_account.account.issuer),
                    "recipient": str(cert_account.account.recipient),
                    "event_id": cert_account.account.event_id,
                    "hours": cert_account.account.hours,
                    "issued_at": cert_account.account.issued_at,
                    "revoked": cert_account.account.revoked
                }
                
                # Filter out revoked certificates if requested
                if include_revoked or not cert_data["revoked"]:
                    certificates.append(cert_data)
            
            return certificates
            
        except Exception as e:
            print(f"❌ Error fetching certificates: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    async def get_user_certificate_by_event(self, user_id: str, event_id: str) -> Optional[Dict]:
        """
        Get a specific certificate for a user by event ID.
        
        Args:
            user_id: User identifier
            event_id: Event identifier
            
        Returns:
            Certificate dictionary or None if not found
        """
        user_pubkey_str = self.wallet_manager.get_user_public_key(user_id)
        if not user_pubkey_str:
            raise ValueError(f"User {user_id} not found")
        
        user_pubkey = Pubkey.from_string(user_pubkey_str)
        program = await self._get_program()
        
        # Compute the PDA for this specific certificate
        seeds = [b"certificate", bytes(user_pubkey), event_id.encode('utf-8')]
        certificate_pubkey, _ = Pubkey.find_program_address(seeds, program.program_id)
        
        try:
            # Fetch the specific certificate
            cert = await program.account["Certificate"].fetch(certificate_pubkey)
            
            return {
                "certificate_address": str(certificate_pubkey),
                "issuer": str(cert.issuer),
                "recipient": str(cert.recipient),
                "event_id": cert.event_id,
                "hours": cert.hours,
                "issued_at": cert.issued_at,
                "revoked": cert.revoked
            }
        except Exception as e:
            # Certificate doesn't exist
            return None
    
    async def get_user_total_hours(self, user_id: str) -> int:
        """
        Calculate total volunteer hours for a user (excluding revoked certificates).
        
        Args:
            user_id: User identifier
            
        Returns:
            Total hours volunteered
        """
        certificates = await self.get_user_certificates(user_id, include_revoked=False)
        total_hours = sum(cert["hours"] for cert in certificates)
        return total_hours
    
    async def get_user_statistics(self, user_id: str) -> Dict:
        """
        Get comprehensive statistics for a user's volunteer activity.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with user statistics
        """
        certificates = await self.get_user_certificates(user_id, include_revoked=True)
        
        active_certs = [c for c in certificates if not c["revoked"]]
        revoked_certs = [c for c in certificates if c["revoked"]]
        
        return {
            "user_id": user_id,
            "blockchain_address": self.wallet_manager.get_user_public_key(user_id),
            "total_certificates": len(certificates),
            "active_certificates": len(active_certs),
            "revoked_certificates": len(revoked_certs),
            "total_hours": sum(c["hours"] for c in active_certs),
            "certificates": active_certs
        }


# Demo usage
async def demo():
    """Demonstrate the UserBlockchainService"""
    
    service = UserBlockchainService()
    
    # Example 1: Create and register a new user
    print("="*60)
    print("1. Creating and registering new user")
    print("="*60)
    
    user_info = await service.create_and_register_user(
        user_id="demo_user_001",
        email="demo@volunthere.com",
        name="Demo User"
    )
    print(f"✅ User created: {user_info}")
    
    # Example 2: Issue certificates to the user
    print("\n" + "="*60)
    print("2. Issuing certificates")
    print("="*60)
    
    events = [
        ("beach_cleanup_2024", 5),
        ("food_bank_2024", 8),
        ("tree_planting_2024", 6)
    ]
    
    for event_id, hours in events:
        cert = await service.issue_certificate_to_user("demo_user_001", event_id, hours)
        print(f"✅ Certificate issued for {event_id}: {hours} hours")
    
    # Example 3: Get all user certificates
    print("\n" + "="*60)
    print("3. Fetching user certificates")
    print("="*60)
    
    certificates = await service.get_user_certificates("demo_user_001")
    print(f"Found {len(certificates)} certificates:")
    for cert in certificates:
        print(f"  - {cert['event_id']}: {cert['hours']} hours (revoked: {cert['revoked']})")
    
    # Example 4: Get user statistics
    print("\n" + "="*60)
    print("4. User statistics")
    print("="*60)
    
    stats = await service.get_user_statistics("demo_user_001")
    print(f"User: {stats['user_id']}")
    print(f"Total certificates: {stats['total_certificates']}")
    print(f"Active certificates: {stats['active_certificates']}")
    print(f"Total hours: {stats['total_hours']}")
    
    # Example 5: Get specific certificate
    print("\n" + "="*60)
    print("5. Getting specific certificate")
    print("="*60)
    
    specific_cert = await service.get_user_certificate_by_event("demo_user_001", "beach_cleanup_2024")
    if specific_cert:
        print(f"Certificate found:")
        print(f"  Event: {specific_cert['event_id']}")
        print(f"  Hours: {specific_cert['hours']}")
        print(f"  Address: {specific_cert['certificate_address']}")
    else:
        print("Certificate not found")

if __name__ == "__main__":
    asyncio.run(demo())
