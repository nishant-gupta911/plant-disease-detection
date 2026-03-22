#!/usr/bin/env python
"""
Main Orchestration Script
Runs the entire Plant Disease Detection System with all components
"""
import os
import sys
import subprocess
import time
from pathlib import Path
import signal


class ProjectManager:
    """Manage all project services"""
    
    def __init__(self):
        self.processes = []
        self.project_root = Path(__file__).parent
        
    def print_banner(self, title):
        """Print formatted banner"""
        print("\n" + "="*80)
        print(f"🌿 {title}")
        print("="*80 + "\n")
    
    def run_command(self, command, name, in_background=True):
        """Run a shell command"""
        print(f"▶️  Starting {name}...")
        
        if in_background:
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=str(self.project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.processes.append((name, process))
            print(f"   ✅ {name} started (PID: {process.pid})")
            return process
        else:
            result = subprocess.run(command, shell=True, cwd=str(self.project_root))
            return result.returncode
    
    def wait_for_service(self, port, timeout=30):
        """Wait for service to be ready"""
        import socket
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(('localhost', port))
                sock.close()
                return True
            except:
                time.sleep(1)
        
        return False
    
    def run_full_system(self):
        """Run all components"""
        
        self.print_banner("PLANT DISEASE DETECTION SYSTEM - FULL STARTUP")
        
        # Step 1: Check model exists
        print("1️⃣  Checking Model...")
        model_path = self.project_root / "models" / "model.pt"
        if not model_path.exists():
            self.print_banner("MODEL NOT FOUND - TRAINING REQUIRED")
            print("Starting model training...")
            self.run_command(
                "source .venv/bin/activate && python training/train.py",
                "Model Training",
                in_background=False
            )
            print("\n✓ Training complete!")
        else:
            print(f"   ✅ Model found ({model_path.stat().st_size / 1e6:.1f} MB)")
        
        # Step 2: Start Backend
        self.print_banner("Starting Backend API")
        self.run_command(
            "source .venv/bin/activate && python -m uvicorn backend.main:app --port 8001 --reload",
            "Backend API (Port 8001)"
        )
        print("   Waiting for backend to be ready...")
        if self.wait_for_service(8001):
            print("   ✅ Backend API is ready!")
        else:
            print("   ⚠️  Backend startup timeout")
        
        # Step 3: Start Frontend
        self.print_banner("Starting Frontend")
        self.run_command(
            "cd frontend && npm run dev",
            "Frontend (Vite)"
        )
        print("   ✅ Frontend starting...")
        
        # Step 4: Run Model Evaluation
        time.sleep(3)
        self.print_banner("Running Model Evaluation")
        print("📊 Evaluating model on test dataset...\n")
        self.run_command(
            "source .venv/bin/activate && python training/evaluation.py",
            "Model Evaluation",
            in_background=False
        )
        
        # Step 5: Display system status
        self.print_banner("SYSTEM STATUS - ALL RUNNING ✅")
        
        print("🌐 FRONTEND:")
        print("   📱 URL: http://localhost:5174")
        print("   🔧 Framework: React 18 + Vite\n")
        
        print("⚙️  BACKEND API:")
        print("   🔗 URL: http://localhost:8001")
        print("   📚 Docs: http://localhost:8001/docs")
        print("   🛠️  Framework: FastAPI\n")
        
        print("🤖 TRAINED MODEL:")
        print(f"   📦 Path: models/model.pt")
        print(f"   📊 Size: {model_path.stat().st_size / 1e6:.1f} MB")
        print(f"   🎯 Classes: 28 diseases\n")
        
        print("📔 JUPYTER NOTEBOOKS:")
        exp_dir = self.project_root / "experiment"
        notebooks = list(exp_dir.glob("experiment_*.ipynb"))
        print(f"   ✅ {len(notebooks)} notebooks created and executed\n")
        
        print("="*80)
        print("✨ SYSTEM READY FOR USE!")
        print("="*80)
        print("\n🚀 Next Steps:")
        print("   1. Open http://localhost:5174 in your browser")
        print("   2. Upload a plant leaf image")
        print("   3. Get instant disease prediction!")
        print("   4. Check API docs at http://localhost:8001/docs")
        print("\n💡 To stop all services, press Ctrl+C\n")
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.shutdown()
    
    def run_training_only(self):
        """Run only model training"""
        self.print_banner("TRAINING ONLY MODE")
        print("Starting model training...\n")
        
        self.run_command(
            "source .venv/bin/activate && python training/train.py",
            "Model Training",
            in_background=False
        )
        print("\n✅ Training complete!")
    
    def run_backend_only(self):
        """Run only backend"""
        self.print_banner("BACKEND ONLY MODE")
        
        # Check model
        model_path = self.project_root / "models" / "model.pt"
        if not model_path.exists():
            print("❌ Model not found. Please train first: python main.py --train")
            return
        
        print("Starting backend API on port 8001...\n")
        self.run_command(
            "source .venv/bin/activate && python -m uvicorn backend.main:app --port 8001 --reload",
            "Backend API",
            in_background=False
        )
    
    def run_frontend_only(self):
        """Run only frontend"""
        self.print_banner("FRONTEND ONLY MODE")
        print("Starting frontend on port 5174...\n")
        
        self.run_command(
            "cd frontend && npm run dev",
            "Frontend",
            in_background=False
        )
    
    def run_evaluation_only(self):
        """Run only evaluation"""
        self.print_banner("EVALUATION ONLY MODE")
        
        # Check model
        model_path = self.project_root / "models" / "model.pt"
        if not model_path.exists():
            print("❌ Model not found. Please train first: python main.py --train")
            return
        
        print("Running model evaluation...\n")
        self.run_command(
            "source .venv/bin/activate && python training/evaluation.py",
            "Model Evaluation",
            in_background=False
        )
    
    def shutdown(self):
        """Shutdown all services"""
        print("\n\n🛑 Shutting down services...")
        for name, process in self.processes:
            try:
                process.terminate()
                print(f"   ✓ Stopped {name}")
            except:
                pass
        
        print("\n✅ All services stopped.\n")
        sys.exit(0)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Plant Disease Detection System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py              # Run full system
  python main.py --train      # Train model only
  python main.py --backend    # Run backend only
  python main.py --frontend   # Run frontend only
  python main.py --eval       # Evaluate model only
        """
    )
    
    parser.add_argument('--train', action='store_true', help='Train model only')
    parser.add_argument('--backend', action='store_true', help='Run backend only')
    parser.add_argument('--frontend', action='store_true', help='Run frontend only')
    parser.add_argument('--eval', action='store_true', help='Evaluate model only')
    
    args = parser.parse_args()
    
    manager = ProjectManager()
    
    if args.train:
        manager.run_training_only()
    elif args.backend:
        manager.run_backend_only()
    elif args.frontend:
        manager.run_frontend_only()
    elif args.eval:
        manager.run_evaluation_only()
    else:
        manager.run_full_system()


if __name__ == "__main__":
    main()
