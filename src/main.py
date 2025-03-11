import sys
import os
from pathlib import Path
from copy_from_static import copy_static_to_public
from generate import generate_pages_recursive

def main(basepath="/"):
    """Main function to generate static pages with a basepath."""
    
    print(f"Using basepath: {basepath}")

    src = "static"
    dest = "docs"
    content = "content"
    template_path = "template.html"
    
    # Ensure public directory exists
    os.makedirs(dest, exist_ok=True)

    print("Copying static files...")
    copy_static_to_public(src, dest)
    
    print("Generating content...")
    generate_pages_recursive(content, template_path, dest, basepath)
    
    print("Done!")

# Get basepath from CLI args, default to "/"
if __name__ == "__main__":
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    main(basepath)
