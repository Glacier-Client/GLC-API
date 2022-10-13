import os
println("Starting update:")
println("Pulling git:")
os.system("git pull")
println("installing requirements:")
os.system("pip install -r requirements.txt")
println("starting server:")
os.system("uvicorn main:app --reload --host 0.0.0.0 --port 8083")
