import os
import shutil

# Move manage.py to root
shutil.move('todoproject/manage.py', 'manage.py')

# Move inner todoproject directory contents to root level todoproject
src_dir = 'todoproject/todoproject'
dest_dir = 'todoproject_new'

# Create new directory
os.makedirs(dest_dir, exist_ok=True)

# Move contents
for item in os.listdir(src_dir):
    s = os.path.join(src_dir, item)
    d = os.path.join(dest_dir, item)
    shutil.move(s, d)

# Remove old directories
shutil.rmtree('todoproject')
# Rename new directory
os.rename('todoproject_new', 'todoproject')
