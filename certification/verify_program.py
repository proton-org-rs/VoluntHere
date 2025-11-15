from solders.pubkey import Pubkey
from solana.rpc.api import Client
import base64
import zlib
import json

IDL_ACCOUNT = "Dxb5wSicJPLuQqTpDhUfCdniAKur7E4hEzLtRVhjp1ik"

client = Client("http://172.17.113.189:8899")

print("Fetching and decoding IDL...")
print("="*60)

idl_pubkey = Pubkey.from_string(IDL_ACCOUNT)
response = client.get_account_info(idl_pubkey)

if response.value:
    # Get raw data
    data = base64.b64decode(response.value.data[0]) if isinstance(response.value.data, list) else response.value.data
    
    print(f"Total data length: {len(data)} bytes")
    
    # Anchor IDL format:
    # - First 8 bytes: discriminator/header
    # - Next 4 bytes: authority (32 bytes pubkey after expansion)
    # - Remaining: compressed IDL data
    
    try:
        # Skip the first 44 bytes (8 byte discriminator + 32 byte authority + 4 byte length prefix)
        # The actual compressed data starts after that
        
        # Let's try different offsets to find the zlib stream
        for offset in [0, 8, 40, 44, 48]:
            try:
                compressed_data = data[offset:]
                decompressed = zlib.decompress(compressed_data)
                idl_json = json.loads(decompressed)
                
                print(f"\n✅ Successfully decompressed IDL (offset: {offset})!")
                print(f"\nIDL Content:")
                print("="*60)
                print(json.dumps(idl_json, indent=2))
                
                # Save to file
                with open("volunteer_cert_decoded.json", "w") as f:
                    json.dump(idl_json, f, indent=2)
                print(f"\n✅ Saved to volunteer_cert_decoded.json")
                break
                
            except Exception as e:
                continue
        else:
            print("❌ Could not decompress IDL at any offset")
            print("\nRaw hex (first 200 bytes):")
            print(data[:200].hex())
            
    except Exception as e:
        print(f"❌ Error decoding IDL: {e}")
        print("\nRaw hex (first 200 bytes):")
        print(data[:200].hex())
else:
    print("❌ IDL account not found")