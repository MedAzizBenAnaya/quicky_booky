@echo off
start cmd /k "cd back\ebookGen && python app.py"
start cmd /k "cd front && npm run dev"
start cmd /k "C:\Users\azizo\Downloads\stripe_1.19.4_windows_x86_64\stripe.exe listen --forward-to http://localhost:5000/webhook"

