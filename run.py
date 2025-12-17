#!/usr/bin/env python3
"""
Dummy OpenAI API Launcher

A simple launcher script for starting the Dummy OpenAI API server
with easy configuration options.

Usage:
    python run.py                    # Start with defaults
    python run.py --port 3000        # Custom port
    python run.py --key my-secret    # Custom API key
    python run.py --debug            # Enable debug mode
    python run.py --help             # Show all options
"""

import argparse
import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def print_banner():
    """Print startup banner."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    Dummy OpenAI API                         ║
║                                                              ║
║  🚀 Starting local OpenAI-compatible API server...          ║
║                                                              ║
║  📖 API Documentation: http://localhost:{port}             ║
║  🔑 Default API Key: {api_key}                              ║
║  🔧 Debug Mode: {debug}                                     ║
║                                                              ║
║  💡 Test the API: python client_example.py                  ║
║  🧪 Run tests: python test_api.py                           ║
╚══════════════════════════════════════════════════════════════╝
"""
    return banner

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import flask
        import flask_cors
        print("✓ Dependencies check passed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("\nPlease install dependencies:")
        print("  pip install -r requirements.txt")
        return False

def open_browser(url, delay=2):
    """Open browser to API documentation after a delay."""
    time.sleep(delay)
    try:
        webbrowser.open(url)
        print(f"✓ Opened browser to {url}")
    except Exception:
        print(f"⚠️  Could not open browser automatically")
        print(f"   Please visit: {url}")

def main():
    """Main launcher function."""
    parser = argparse.ArgumentParser(
        description="Launch Dummy OpenAI API Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                    # Start with default settings
  python run.py --port 3000        # Use custom port
  python run.py --key secret123    # Use custom API key
  python run.py --debug            # Enable debug logging
  python run.py --no-browser       # Don't open browser automatically

Environment Variables:
  PORT           Server port (default: 8000)
  API_KEY        API key (default: sk-dummy)
  DEBUG          Enable debug mode (default: False)
  HOST           Server host (default: 0.0.0.0)

Quick Start:
  1. python run.py
  2. Open http://localhost:8000 in your browser
  3. Test with: python client_example.py
        """
    )

    parser.add_argument(
        '--port', '-p',
        type=int,
        default=int(os.getenv('PORT', 8000)),
        help='Port to run the server on (default: 8000)'
    )

    parser.add_argument(
        '--api-key', '-k',
        type=str,
        default=os.getenv('API_KEY', 'sk-dummy'),
        help='API key for authentication (default: sk-dummy)'
    )

    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        default=os.getenv('DEBUG', 'False').lower() == 'true',
        help='Enable debug mode'
    )

    parser.add_argument(
        '--host',
        type=str,
        default=os.getenv('HOST', '0.0.0.0'),
        help='Host to bind to (default: 0.0.0.0)'
    )

    parser.add_argument(
        '--no-browser',
        action='store_true',
        help='Don\'t open browser automatically'
    )

    parser.add_argument(
        '--check-deps',
        action='store_true',
        help='Check dependencies and exit'
    )

    parser.add_argument(
        '--env-file',
        type=str,
        help='Load environment variables from file'
    )

    args = parser.parse_args()

    # Load environment file if specified
    if args.env_file:
        if os.path.exists(args.env_file):
            print(f"Loading environment from {args.env_file}")
            with open(args.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip().strip('"\'')
        else:
            print(f"⚠️  Environment file not found: {args.env_file}")

    # Check dependencies if requested
    if args.check_deps:
        if check_dependencies():
            print("✓ All dependencies are installed")
            sys.exit(0)
        else:
            print("✗ Some dependencies are missing")
            sys.exit(1)

    # Always check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Set environment variables
    os.environ['PORT'] = str(args.port)
    os.environ['API_KEY'] = args.api_key
    os.environ['DEBUG'] = 'True' if args.debug else 'False'
    os.environ['HOST'] = args.host

    # Print banner
    banner = print_banner().format(
        port=args.port,
        api_key=args.api_key,
        debug='Enabled' if args.debug else 'Disabled'
    )
    print(banner)

    # Check if app.py exists
    app_path = Path(__file__).parent / 'app.py'
    if not app_path.exists():
        print(f"✗ Error: app.py not found in {app_path.parent}")
        print("Make sure you're running this script from the dummy-openai-api directory")
        sys.exit(1)

    # Prepare command
    cmd = [sys.executable, 'app.py']

    # Print startup information
    print("🚀 Starting server...")
    print(f"   Command: {' '.join(cmd)}")
    print(f"   Port: {args.port}")
    print(f"   API Key: {args.api_key}")
    print(f"   Debug: {args.debug}")
    print(f"   Host: {args.host}")
    print()

    # Open browser in background if not disabled
    if not args.no_browser:
        docs_url = f"http://localhost:{args.port}"
        import threading
        browser_thread = threading.Thread(
            target=open_browser,
            args=(docs_url,),
            daemon=True
        )
        browser_thread.start()

    # Start the server
    try:
        print("=" * 60)
        print("🌟 Server is starting... (Press Ctrl+C to stop)")
        print("=" * 60)
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("Thanks for using Dummy OpenAI API! 👋")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error starting server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
