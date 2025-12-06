# Run All
Write-Host "Starting Backend and Frontend..."

# Start Backend in a new process
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; uvicorn app.main:app --host 0.0.0.0 --port 8000 --env-file .env"

# Start Frontend in a new process
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "Both services starting..."
