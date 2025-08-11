import torch
import cv2
import numpy as np
from PIL import Image
from pathlib import Path
import logging
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime, timezone
from ultralytics import YOLO  # Use ultralytics YOLO instead of torch.hub

from app.core.config import settings

logger = logging.getLogger(__name__)


class YOLOService:
    """Service for YOLO-based lung nodule detection"""
    
    def __init__(self):
        self.model = None
        self.device = None
        self.model_loaded = False
        self.confidence_threshold = 0.3
        self.nms_threshold = 0.4
        
    async def initialize_model(self):
        """Initialize the YOLOv11 model"""
        try:
            # Set device
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            logger.info(f"Using device: {self.device}")
            
            # Load model
            model_path = Path(settings.YOLO_MODEL_PATH)
            if not model_path.exists():
                raise FileNotFoundError(f"YOLO model not found at {model_path}")
            
            # Load YOLOv11 model using ultralytics
            self.model = YOLO(str(model_path))
            
            # Move model to device
            self.model.to(self.device)
            
            self.model_loaded = True
            logger.info("YOLOv11 model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load YOLOv11 model: {str(e)}")
            raise
    
    def preprocess_image(self, image_path: str) -> str:
        """YOLOv11 handles preprocessing internally, just return path"""
        try:
            # Verify image exists and is readable
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not load image from {image_path}")
            
            return image_path  # YOLOv11 handles preprocessing internally
            
        except Exception as e:
            logger.error(f"Image validation failed: {str(e)}")
            raise
    
    async def detect_nodules(self, image_path: str) -> Dict[str, Any]:
        """Detect lung nodules in X-ray image using YOLOv11"""
        if not self.model_loaded:
            await self.initialize_model()
        
        try:
            # Validate image
            processed_image_path = self.preprocess_image(image_path)
            
            # Run inference with YOLOv11
            results = self.model(
                processed_image_path,
                conf=self.confidence_threshold,
                iou=self.nms_threshold,
                verbose=False  # Reduce output verbosity
            )
            
            # Parse results
            detections = self._parse_detections_v11(results)
            
            # Calculate overall confidence
            overall_confidence = self._calculate_overall_confidence(detections)
            
            # Generate summary
            summary = self._generate_detection_summary(detections)
            
            # Get image dimensions
            image = cv2.imread(image_path)
            image_size = image.shape[:2] if image is not None else (0, 0)
            
            return {
                "detected_objects": detections,
                "total_detections": len(detections),
                "confidence": overall_confidence,
                "processing_time": 0.0,  # YOLOv11 doesn't expose timing in the same way
                "image_size": image_size,
                "summary": summary,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            logger.error(f"Nodule detection failed: {str(e)}")
            raise
    
    def _parse_detections_v11(self, results) -> List[Dict[str, Any]]:
        """Parse YOLOv11 detection results"""
        detections = []
        
        try:
            # YOLOv11 returns a list of Results objects
            for result in results:
                if result.boxes is not None:
                    boxes = result.boxes
                    
                    # Get coordinates, confidence, and classes
                    xyxy = boxes.xyxy.cpu().numpy()  # x1, y1, x2, y2
                    conf = boxes.conf.cpu().numpy()  # confidence scores
                    cls = boxes.cls.cpu().numpy()   # class indices
                    
                    # Get image dimensions
                    img_height, img_width = result.orig_shape
                    
                    for i in range(len(xyxy)):
                        x1, y1, x2, y2 = xyxy[i]
                        confidence = float(conf[i])
                        class_id = int(cls[i])
                        
                        # Calculate center point and dimensions
                        center_x = (x1 + x2) / 2
                        center_y = (y1 + y2) / 2
                        width = x2 - x1
                        height = y2 - y1
                        area = width * height
                        
                        # Get class name
                        class_name = "nodule"  # Default
                        if hasattr(self.model, 'names') and class_id < len(self.model.names):
                            class_name = self.model.names[class_id]
                        
                        detection_info = {
                            "class_id": class_id,
                            "class_name": class_name,
                            "confidence": confidence,
                            "bbox": {
                                "x1": float(x1),
                                "y1": float(y1),
                                "x2": float(x2),
                                "y2": float(y2),
                                "center_x": float(center_x),
                                "center_y": float(center_y),
                                "width": float(width),
                                "height": float(height),
                                "area": float(area)
                            },
                            "severity": self._assess_nodule_severity(confidence, area, img_width * img_height)
                        }
                        
                        detections.append(detection_info)
        
        except Exception as e:
            logger.error(f"Error parsing YOLOv11 results: {str(e)}")
        
        # Sort by confidence
        detections.sort(key=lambda x: x["confidence"], reverse=True)
        
        return detections
    
    def _assess_nodule_severity(self, confidence: float, nodule_area: float, image_area: float) -> str:
        """Assess the severity of detected nodule"""
        if image_area <= 0:
            return "unknown"
            
        # Calculate nodule size relative to image
        relative_size = nodule_area / image_area
        
        # Assessment based on confidence and size
        if confidence >= 0.8:
            if relative_size > 0.01:  # Large nodule
                return "high"
            elif relative_size > 0.005:  # Medium nodule
                return "moderate"
            else:
                return "low"
        elif confidence >= 0.5:
            if relative_size > 0.01:
                return "moderate"
            else:
                return "low"
        else:
            return "low"
    
    def _calculate_overall_confidence(self, detections: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence for the analysis"""
        if not detections:
            return 0.0
        
        # Weight by confidence and number of detections
        total_confidence = sum(det["confidence"] for det in detections)
        avg_confidence = total_confidence / len(detections)
        
        # Boost confidence if multiple high-confidence detections
        high_conf_count = sum(1 for det in detections if det["confidence"] > 0.7)
        confidence_boost = min(0.1, high_conf_count * 0.03)
        
        return min(1.0, avg_confidence + confidence_boost)
    
    def _generate_detection_summary(self, detections: List[Dict[str, Any]]) -> str:
        """Generate a text summary of detections"""
        if not detections:
            return "No lung nodules detected in the X-ray image."
        
        high_severity = [d for d in detections if d["severity"] == "high"]
        moderate_severity = [d for d in detections if d["severity"] == "moderate"]
        low_severity = [d for d in detections if d["severity"] == "low"]
        
        summary_parts = []
        
        if high_severity:
            summary_parts.append(f"{len(high_severity)} high-confidence nodule(s)")
        if moderate_severity:
            summary_parts.append(f"{len(moderate_severity)} moderate-confidence nodule(s)")
        if low_severity:
            summary_parts.append(f"{len(low_severity)} low-confidence nodule(s)")
        
        summary = f"Detected {len(detections)} potential lung nodule(s): " + ", ".join(summary_parts)
        
        # Add confidence note
        if detections:
            max_confidence = max(det["confidence"] for det in detections)
            if max_confidence >= 0.8:
                summary += ". High confidence detections require medical review."
            elif max_confidence >= 0.5:
                summary += ". Moderate confidence detections recommended for professional evaluation."
            else:
                summary += ". Low confidence detections may be artifacts or require further imaging."
        
        return summary
    
    async def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        if not self.model_loaded:
            return {"status": "not_loaded"}
        
        return {
            "status": "loaded",
            "device": str(self.device),
            "confidence_threshold": self.confidence_threshold,
            "nms_threshold": self.nms_threshold,
            "model_path": settings.YOLO_MODEL_PATH,
            "model_type": "YOLOv11",
            "classes": getattr(self.model, 'names', {}),
            "cuda_available": torch.cuda.is_available()
        }


# Global YOLO service instance
yolo_service = YOLOService()