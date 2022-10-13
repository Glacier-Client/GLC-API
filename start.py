import os
print("Starting update:")
print("Pulling git:")
os.system("git pull")
print("installing requirements:")
os.system("pip install -r requirements.txt")
print("starting server:")
os.system("uvicorn main:app --reload --host 0.0.0.0 --port 8083")
