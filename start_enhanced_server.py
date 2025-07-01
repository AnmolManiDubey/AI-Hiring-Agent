#!/usr/bin/env python3
"""
Start the Enhanced LinkedIn Sourcing Agent FastAPI server with Groq/Llama integration
"""

import uvicorn
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Starting Enhanced LinkedIn Sourcing Agent API Server...")
    print("🤖 Powered by Groq API + Llama models")
    print("📡 API will be available at: http://localhost:8000")
    print("🌐 Frontend will be available at: http://localhost:8000/frontend")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("💚 Health check at: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        uvicorn.run(
            "backend.enhanced_main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1) 