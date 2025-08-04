#!/bin/bash

# NetworkingAI Service Fix Script
# This script fixes common issues and ensures all services are running properly

echo "🔧 NetworkingAI Service Fix Script"
echo "=================================="

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check service status
check_service() {
    local service=$1
    local status=$(sudo supervisorctl status $service | awk '{print $2}')
    if [[ "$status" == "RUNNING" ]]; then
        echo "✅ $service is running"
        return 0
    else
        echo "❌ $service is not running ($status)"
        return 1
    fi
}

# Function to install missing dependencies
install_dependencies() {
    echo "📦 Installing/updating dependencies..."
    
    # Install emergentintegrations if missing
    if ! python -c "import emergentintegrations" 2>/dev/null; then
        echo "Installing emergentintegrations..."
        pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
    fi
    
    # Update other dependencies
    cd /app/backend
    pip install -r requirements.txt
    
    cd /app/frontend
    yarn install --frozen-lockfile
}

# Function to fix permissions
fix_permissions() {
    echo "🔒 Fixing permissions..."
    sudo chown -R $(whoami):$(whoami) /app
    chmod +x /app/fix-services.sh
}

# Function to restart services
restart_services() {
    echo "🔄 Restarting services..."
    sudo supervisorctl restart all
    sleep 5
}

# Function to check ports
check_ports() {
    echo "🌐 Checking ports..."
    
    if netstat -tln | grep -q ":8001"; then
        echo "✅ Backend port 8001 is listening"
    else
        echo "❌ Backend port 8001 is not listening"
    fi
    
    if netstat -tln | grep -q ":3000"; then
        echo "✅ Frontend port 3000 is listening"
    else
        echo "❌ Frontend port 3000 is not listening"
    fi
}

# Function to test API endpoints
test_api() {
    echo "🧪 Testing API endpoints..."
    
    # Test backend health
    if curl -s -f "http://localhost:8001/api/health" > /dev/null; then
        echo "✅ Backend API is responding"
    else
        echo "❌ Backend API is not responding"
    fi
    
    # Test frontend
    if curl -s -f "http://localhost:3000" > /dev/null; then
        echo "✅ Frontend is responding"
    else
        echo "❌ Frontend is not responding"
    fi
}

# Function to check logs for errors
check_logs() {
    echo "📋 Checking recent logs for errors..."
    
    echo "Backend errors (last 10 lines):"
    tail -n 10 /var/log/supervisor/backend.err.log 2>/dev/null || echo "No backend error log found"
    
    echo "Frontend errors (last 5 lines):"
    tail -n 5 /var/log/supervisor/frontend.err.log 2>/dev/null || echo "No frontend error log found"
}

# Main execution
main() {
    echo "Starting diagnostic and fix process..."
    echo ""
    
    # Check current status
    echo "1. Checking current service status..."
    check_service "backend"
    check_service "frontend" 
    check_service "mongodb"
    echo ""
    
    # Fix permissions
    echo "2. Fixing permissions..."
    fix_permissions
    echo ""
    
    # Install dependencies
    echo "3. Installing/updating dependencies..."
    install_dependencies
    echo ""
    
    # Restart services
    echo "4. Restarting services..."
    restart_services
    echo ""
    
    # Check ports
    echo "5. Checking ports..."
    check_ports
    echo ""
    
    # Test API
    echo "6. Testing API endpoints..."
    test_api
    echo ""
    
    # Check logs
    echo "7. Checking logs..."
    check_logs
    echo ""
    
    # Final status check
    echo "8. Final service status check..."
    sudo supervisorctl status
    echo ""
    
    echo "🎉 Fix script completed!"
    echo ""
    echo "If issues persist, try:"
    echo "1. Check the logs: tail -f /var/log/supervisor/*.log"
    echo "2. Restart manually: sudo supervisorctl restart all"
    echo "3. Check the deployment guide: cat /app/DEPLOYMENT_GUIDE.md"
}

# Run the main function
main