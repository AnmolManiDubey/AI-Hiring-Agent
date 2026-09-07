#!/bin/bash

# 🚀 LinkedIn Sourcing Agent Deployment Script
# This script helps you deploy your application to Vercel and Railway

set -e  # Exit on any error

echo "🚀 LinkedIn Sourcing Agent Deployment Script"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if git is initialized
if [ ! -d ".git" ]; then
    print_error "Git repository not initialized. Please run 'git init' first."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating template..."
    cat > .env << EOF
# LinkedIn Sourcing Agent Environment Variables
# Replace with your actual API keys

GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here
GROQ_API_KEY=your_groq_api_key_here
PORT=8000
EOF
    print_status "Created .env template. Please update with your actual API keys."
fi

# Function to deploy backend
deploy_backend() {
    print_status "Deploying backend to Railway..."
    
    # Check if Railway CLI is installed
    if ! command -v railway &> /dev/null; then
        print_warning "Railway CLI not found. Installing..."
        npm install -g @railway/cli
    fi
    
    # Check if logged in to Railway
    if ! railway whoami &> /dev/null; then
        print_status "Please login to Railway..."
        railway login
    fi
    
    # Deploy to Railway
    print_status "Deploying to Railway..."
    railway up
    
    # Get the deployment URL
    BACKEND_URL=$(railway status --json | grep -o '"url":"[^"]*"' | cut -d'"' -f4)
    
    if [ -n "$BACKEND_URL" ]; then
        print_success "Backend deployed successfully!"
        print_status "Backend URL: $BACKEND_URL"
        
        # Update vercel.json with the backend URL
        sed -i "s|https://your-backend-url.railway.app|$BACKEND_URL|g" frontend/vercel.json
        print_success "Updated frontend configuration with backend URL"
    else
        print_error "Failed to get backend URL"
        exit 1
    fi
}

# Function to deploy frontend
deploy_frontend() {
    print_status "Deploying frontend to Vercel..."
    
    # Check if Vercel CLI is installed
    if ! command -v vercel &> /dev/null; then
        print_warning "Vercel CLI not found. Installing..."
        npm install -g vercel
    fi
    
    # Deploy frontend
    cd frontend
    print_status "Deploying frontend..."
    vercel --prod
    
    cd ..
    print_success "Frontend deployed successfully!"
}

# Function to set environment variables
set_env_vars() {
    print_status "Setting environment variables..."
    
    # Read from .env file
    if [ -f ".env" ]; then
        source .env
        
        # Set Railway environment variables
        if [ -n "$GOOGLE_API_KEY" ] && [ "$GOOGLE_API_KEY" != "your_google_api_key_here" ]; then
            railway variables set GOOGLE_API_KEY="$GOOGLE_API_KEY"
        fi
        
        if [ -n "$GOOGLE_SEARCH_ENGINE_ID" ] && [ "$GOOGLE_SEARCH_ENGINE_ID" != "your_search_engine_id_here" ]; then
            railway variables set GOOGLE_SEARCH_ENGINE_ID="$GOOGLE_SEARCH_ENGINE_ID"
        fi
        
        if [ -n "$GROQ_API_KEY" ] && [ "$GROQ_API_KEY" != "your_groq_api_key_here" ]; then
            railway variables set GROQ_API_KEY="$GROQ_API_KEY"
        fi
        
        print_success "Environment variables set successfully!"
    else
        print_warning "No .env file found. Please set environment variables manually."
    fi
}

# Main deployment flow
main() {
    echo ""
    print_status "Starting deployment process..."
    
    # Check if we have uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        print_warning "You have uncommitted changes. Committing them..."
        git add .
        git commit -m "Deploy: $(date)"
    fi
    
    # Push to GitHub
    print_status "Pushing to GitHub..."
    git push origin main
    
    # Deploy backend
    deploy_backend
    
    # Set environment variables
    set_env_vars
    
    # Deploy frontend
    deploy_frontend
    
    echo ""
    print_success "🎉 Deployment completed successfully!"
    echo ""
    print_status "Your application is now live:"
    print_status "- Frontend: Check Vercel dashboard for URL"
    print_status "- Backend: $BACKEND_URL"
    echo ""
    print_status "Next steps:"
    print_status "1. Test your application"
    print_status "2. Set up custom domain (optional)"
    print_status "3. Configure monitoring and analytics"
}

# Check command line arguments
case "${1:-}" in
    "backend")
        deploy_backend
        ;;
    "frontend")
        deploy_frontend
        ;;
    "env")
        set_env_vars
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [backend|frontend|env|help]"
        echo ""
        echo "Commands:"
        echo "  backend   - Deploy only the backend to Railway"
        echo "  frontend  - Deploy only the frontend to Vercel"
        echo "  env       - Set environment variables on Railway"
        echo "  help      - Show this help message"
        echo ""
        echo "If no command is provided, deploys both frontend and backend."
        ;;
    "")
        main
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Use '$0 help' for usage information."
        exit 1
        ;;
esac 