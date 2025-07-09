import os
import re
from xml.etree import ElementTree as ET

def extract_text_from_svg(svg_file):
    """Extract all text content from an SVG file."""
    try:
        tree = ET.parse(svg_file)
        root = tree.getroot()
        
        # Find all text elements (handle namespaces)
        text_elements = root.findall('.//{http://www.w3.org/2000/svg}text')
        if not text_elements:
            # Try without namespace
            text_elements = root.findall('.//text')
        
        texts = []
        for text_elem in text_elements:
            if text_elem.text:
                texts.append(text_elem.text.strip())
            # Also check for text in child elements
            for child in text_elem:
                if child.text:
                    texts.append(child.text.strip())
        
        return texts
    except Exception as e:
        print(f"Error processing {svg_file}: {e}")
        return []

def main():
    # Get all SVG files in current directory
    svg_files = [f for f in os.listdir('.') if f.lower().endswith('.svg')]
    
    if not svg_files:
        print("No SVG files found in current directory")
        return
    
    for svg_file in svg_files:
        print(f"\n--- {svg_file} ---")
        texts = extract_text_from_svg(svg_file)
        
        total_text = ''
        if texts:
            for text in texts:
                if text:  # Only print non-empty text
                    # print(text)
                    total_text += text
            
            open('output.txt', 'a').write(total_text + '\n')
        else:
            print("No text found")

if __name__ == "__main__":
    main()