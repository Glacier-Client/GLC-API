import os
print("checking installed:")
os.system("apt install python3-pip -y")
os.system("apt install git -y")
print("Starting update:")
print("Pulling git:")
os.system("git pull")
print("installing requirements:")
os.system("pip install fastapi")
os.system("apt install uvicorn -y")
print("starting server:")
os.system("uvicorn main:app --reload --host 0.0.0.0 --port 8083")
