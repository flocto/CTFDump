from opcua import Client
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_water_treatment_plant():
    """
    Fix the water treatment plant by adjusting OPC UA parameters
    """
    # Placeholder OPC UA server URL
    opc_url = "opc.tcp://94.237.120.195:49894"
    
    try:
        # Create OPC UA client
        client = Client(opc_url)
        
        # Connect to the server
        logger.debug("Connecting to OPC UA server...")
        client.connect()
        
        # Get the root node
        root = client.get_root_node()
        
        # Browse the server structure first
        logger.debug("Browsing server structure...")
        objects = root.get_child("0:Objects")
        
        water_treatment_plant = objects.get_child("2:WaterTreatmentPlant")
        
        logger.debug(f"Found WaterTreatmentPlant: {water_treatment_plant.get_browse_name()}")

        for child in water_treatment_plant.get_children():
            logger.debug(f"  {child.get_browse_name()}")
        
        # Get the main components
        valve_section = water_treatment_plant.get_child("2:Valve")
        pump_section = water_treatment_plant.get_child("2:Pump")
        tank_section = water_treatment_plant.get_child("2:Tank")
        sensors_section = water_treatment_plant.get_child("2:Sensors")
        
        # # Browse each section to see what's available
        # logger.info("Valve section children:")
        # for child in valve_section.get_children():
        #     logger.info(f"  {child.get_browse_name()}")
            
        # logger.info("Pump section children:")
        # for child in pump_section.get_children():
        #     logger.info(f"  {child.get_browse_name()}")
            
        # logger.info("Tank section children:")
        # for child in tank_section.get_children():
        #     logger.info(f"  {child.get_browse_name()}")
            
        # logger.info("Sensors section children:")
        # for child in sensors_section.get_children():
        #     logger.info(f"  {child.get_browse_name()}")
        
        # Task 1: Set inlet valve to 100% open
        logger.debug("Setting inlet valve to 100% open...")
        inlet_valve = valve_section.get_child("2:PercentOpen")
        logger.info(f"Previous Inlet Valve value: {inlet_valve.get_value()}%")
        inlet_valve.set_value(100.0)  # 100% open
        logger.info(f"Inlet Valve verified: {inlet_valve.get_value()}%")
        
        # Task 2: Increase pump speed to 1600 RPM
        logger.debug("Setting pump speed to 1600 RPM...")
        pump_speed = pump_section.get_child("2:Speed")
        logger.info(f"Previous Pump Speed value: {pump_speed.get_value()} RPM")
        pump_speed.set_value(1600)  # 1600 RPM
        logger.info(f"Pump Speed verified: {pump_speed.get_value()} RPM")
        
        # Task 3: Fix flow sensor to 4 L/s
        logger.debug("Setting flow sensor to 4 L/s...")
        flow_sensor = sensors_section.get_child("2:FlowRate")
        logger.info(f"Previous Flow Sensor value: {flow_sensor.get_value()} L/s")
        flow_sensor.set_value(4.0)  # 4 L/s
        logger.info(f"Flow Sensor verified: {flow_sensor.get_value()} L/s")
        
        # Task 4: Raise tank water level to 5m
        logger.debug("Setting tank water level to 5m...")
        water_level = tank_section.get_child("2:WaterLevel")
        logger.info(f"Previous Water Level value: {water_level.get_value()} m")
        water_level.set_value(5.0)  # 5 meters
        logger.info(f"Water Level verified: {water_level.get_value()} m")
        
        logger.info("All tasks completed successfully!")

        # Wait a moment for any updates to propagate
        import time
        time.sleep(2)

        # Browse the entire maintenance section more thoroughly
        maintenance_section = water_treatment_plant.get_child("2:Maintenance")
        logger.info(f"Found Maintenance section: {maintenance_section.get_browse_name()}")
        
        # Browse all maintenance children
        logger.info("Maintenance section children:")
        for child in maintenance_section.get_children():
            child_name = child.get_browse_name()
            logger.info(f"  {child_name}")
            
            # Try to read the value of each maintenance child
            try:
                child_value = child.get_value()
                logger.info(f"    Value: {child_value}")
            except:
                logger.info(f"    No direct value")
                
                # If it has children, browse them too
                try:
                    for grandchild in child.get_children():
                        grandchild_name = grandchild.get_browse_name()
                        try:
                            grandchild_value = grandchild.get_value()
                            logger.info(f"      {grandchild_name}: {grandchild_value}")
                        except:
                            logger.info(f"      {grandchild_name}: No value")
                except:
                    pass

        # Also check if there are any new nodes that appeared after completing tasks
        logger.info("Re-checking WaterTreatmentPlant for any new children:")
        for child in water_treatment_plant.get_children():
            child_name = child.get_browse_name()
            logger.info(f"  {child_name}")
            
            # Check if there's a new section we missed
            if "Status" in str(child_name) or "Message" in str(child_name) or "Alert" in str(child_name):
                try:
                    value = child.get_value()
                    logger.info(f"    POTENTIAL FLAG: {value}")
                except:
                    pass

        
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
    fix_water_treatment_plant()