import os
import shutil
def copy_static_to_public(src, dest):
    """Recursively copies all contents from src to dest after clearing dest."""
    
    # Step 1: Delete destination directory if it exists
    if os.path.exists(dest):
        shutil.rmtree(dest)
        print(f"Deleted existing destination: {dest}")

    # Step 2: Recreate the destination directory
    os.makedirs(dest)
    print(f"Created destination directory: {dest}")

    # Step 3: Recursively copy files and directories
    def recursive_copy(src_path, dest_path):
        for item in os.listdir(src_path):
            src_item = os.path.join(src_path, item)
            dest_item = os.path.join(dest_path, item)

            if os.path.isdir(src_item):
                # If it's a directory, create it in destination & recurse
                os.makedirs(dest_item)
                print(f"Created directory: {dest_item}")
                recursive_copy(src_item, dest_item)
            else:
                # If it's a file, copy it
                shutil.copy2(src_item, dest_item)
                print(f"Copied file: {src_item} → {dest_item}")

    # Start recursive copying
    recursive_copy(src, dest)