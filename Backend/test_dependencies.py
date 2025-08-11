# test_dependencies.py
def test_imports():
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
        print(f"   CUDA available: {torch.cuda.is_available()}")
        
        import torchvision
        print(f"✅ Torchvision: {torchvision.__version__}")
        
        import cv2
        print(f"✅ OpenCV: {cv2.__version__}")
        
        import PIL
        print(f"✅ Pillow: {PIL.__version__}")
        
        import numpy as np
        print(f"✅ NumPy: {np.__version__}")
        
        import ultralytics
        print(f"✅ Ultralytics: {ultralytics.__version__}")
        
        from groq import Groq
        print("✅ Groq client imported successfully")
        
        import aiofiles
        print("✅ Aiofiles imported successfully")
        
        print("\n🎉 All dependencies installed successfully!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")

if __name__ == "__main__":
    test_imports()