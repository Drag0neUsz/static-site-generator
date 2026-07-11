import os
import shutil

# wd = "..\\static"

# source_dir = os.getcwd() + "/static"
# target_dir = os.getcwd() + "/public"

def copy_files(source_dir, target_dir):
    logs = []
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)
    for file in os.listdir(source_dir):
        if os.path.isfile(os.path.join(source_dir, file)):
            logs.append(f"{file} + {os.path.join(source_dir, file)} -> {os.path.join(target_dir, file)}")
            shutil.copy(os.path.join(source_dir, file), os.path.join(target_dir, file))
        elif os.path.isdir(os.path.join(source_dir, file)):
            copy_files(os.path.join(source_dir, file), os.path.join(target_dir, file))
    with open(os.path.join(target_dir, "logs.txt"), "w") as f:
        for log in logs:
            f.write(log + "\n")
    
