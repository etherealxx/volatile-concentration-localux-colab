import os, shutil, sys, pickle

mode = ''

if len(sys.argv) == 2:
    arg = sys.argv[1]
    mode = arg
    
def manualcopytree(source_dir, destination_dir):
    os.makedirs(destination_dir, exist_ok=True)
    for root, dirs, files in os.walk(source_dir):
        # Create a relative path from the source directory to the current directory being walked
        relative_path = os.path.relpath(root, source_dir)
        destination_subdir = os.path.join(destination_dir, relative_path)

        # Create the corresponding subdirectory in the destination directory if it doesn't exist
        os.makedirs(destination_subdir, exist_ok=True)

        for file in files:
            source_file_path = os.path.join(root, file)
            destination_file_path = os.path.join(destination_subdir, file)

            # Check if the file already exists in the destination directory
            if not os.path.exists(destination_file_path):
                # Copy the file from the source to the destination
                shutil.copy2(source_file_path, destination_file_path)

temppath = "/usr/temp"
vclpath = "/usr/zhuyao"

if mode == "backup":
    if os.path.exists(temppath):
        shutil.rmtree(temppath)
    print("Backing up generated outputs before changing branch...")
    manualcopytree(os.path.join(vclpath, "outputs"), os.path.join(temppath, "outputs"))
    print("Backing up downloaded models before changing branch...")
    manualcopytree(os.path.join(vclpath, "models"), os.path.join(temppath, "models"))
    shutil.rmtree(vclpath)
        
elif mode == "restore":
    if os.path.exists(temppath):
        print("Restoring generated outputs after changing branch...")
        manualcopytree(os.path.join(temppath, "outputs"), os.path.join(vclpath, "outputs"))
        print("Restoring up downloaded models after changing branch...")
        manualcopytree(os.path.join(temppath, "models"), os.path.join(vclpath, "models"))
        shutil.rmtree(temppath)
