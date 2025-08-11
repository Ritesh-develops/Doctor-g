from groq import Groq
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """Service for LLM-based medical analysis interpretation"""
    
    def __init__(self):
        self.client = None
        self.model = settings.GROQ_MODEL
        self.initialized = False
    
    async def initialize(self):
        """Initialize the Groq client and validate API key"""
        try:
            if not settings.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY not provided in settings")
            
            if settings.GROQ_API_KEY == "your_groq_api_key_here" or len(settings.GROQ_API_KEY) < 20:
                raise ValueError("GROQ_API_KEY appears to be placeholder or invalid")
            
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            
            # Actually validate the API key by making a test call
            await self.validate_api_key()
            
            self.initialized = True
            logger.info("LLM service initialized and API key validated successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize LLM service: {str(e)}")
            raise
    
    async def validate_api_key(self) -> bool:
        """Validate Groq API key with actual API call"""
        try:
            # Test with a minimal request
            test_response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": "Hello"}],
                model=self.model,
                max_tokens=5,
                temperature=0.1
            )
            
            logger.info("✅ Groq API key validation successful")
            return True
            
        except Exception as e:
            logger.error(f"❌ Groq API key validation failed: {str(e)}")
            raise ValueError(f"Invalid Groq API key: {str(e)}")
    
    async def analyze_xray_results(
        self, 
        yolo_results: Dict[str, Any], 
        patient_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generate patient-friendly analysis from YOLO results"""
        if not self.initialized:
            await self.initialize()
        
        try:
            # Create system prompt
            system_prompt = self._create_system_prompt()
            
            # Create user prompt with YOLO results
            user_prompt = self._create_analysis_prompt(yolo_results, patient_context)
            
            # Generate response
            response = await self._generate_response(system_prompt, user_prompt)
            
            return response
            
        except Exception as e:
            logger.error(f"LLM analysis failed: {str(e)}")
            raise
    
    async def answer_followup_question(
        self,
        question: str,
        yolo_results: Dict[str, Any],
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        """Answer follow-up questions about the X-ray analysis"""
        if not self.initialized:
            await self.initialize()
        
        try:
            system_prompt = self._create_followup_system_prompt()
            user_prompt = self._create_followup_prompt(question, yolo_results, conversation_history)
            
            response = await self._generate_response(system_prompt, user_prompt)
            return response
            
        except Exception as e:
            logger.error(f"Follow-up question answering failed: {str(e)}")
            raise
    
    def _create_system_prompt(self) -> str:
        """Create system prompt for X-ray analysis"""
        return """You are Dr. AI, a medical assistant specialized in interpreting chest X-ray analysis results. Your role is to:

1. Explain X-ray findings in clear, understandable language for patients
2. Provide educational information about lung nodules and chest X-rays
3. Always emphasize the importance of professional medical consultation
4. Be empathetic and supportive while being medically accurate
5. Avoid causing unnecessary anxiety while being honest about findings

Guidelines:
- Use simple, non-technical language
- Explain what lung nodules are and their significance
- Always recommend consulting with a healthcare provider
- Be clear about the limitations of AI analysis
- Provide context about next steps in medical care
- Do not provide specific medical advice or diagnosis

Remember: You are providing information to help patients understand their results, not replacing professional medical consultation."""
    
    def _create_analysis_prompt(
        self, 
        yolo_results: Dict[str, Any], 
        patient_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create analysis prompt with YOLO results"""
        
        # Extract key information
        detections = yolo_results.get("detected_objects", [])
        total_detections = yolo_results.get("total_detections", 0)
        overall_confidence = yolo_results.get("confidence", 0.0)
        summary = yolo_results.get("summary", "")
        
        prompt = f"""Please analyze these chest X-ray results and explain them in patient-friendly terms:

ANALYSIS RESULTS:
- Number of potential findings: {total_detections}
- Overall confidence level: {overall_confidence:.1%}
- Technical summary: {summary}

DETAILED FINDINGS:
"""
        
        if detections:
            for i, detection in enumerate(detections[:5], 1):  # Limit to top 5 detections
                confidence = detection.get("confidence", 0.0)
                severity = detection.get("severity", "unknown")
                class_name = detection.get("class_name", "nodule")
                
                prompt += f"""
Finding {i}:
- Type: {class_name}
- Confidence: {confidence:.1%}
- Severity assessment: {severity}
- Location: Center area of lung field
"""
        else:
            prompt += "\nNo significant findings detected in the chest X-ray."
        
        if patient_context:
            prompt += f"\nPATIENT CONTEXT:\n{json.dumps(patient_context, indent=2)}"
        
        prompt += """

Please provide a comprehensive, patient-friendly explanation that includes:

1. **What was found**: Explain the findings in simple terms
2. **What this might mean**: Discuss possible significance without diagnosing
3. **Next steps**: Recommend appropriate follow-up with healthcare providers
4. **Important notes**: Emphasize limitations of AI analysis and importance of professional review
5. **Reassurance**: Provide appropriate context to reduce anxiety while being honest

Keep the tone professional yet compassionate, and always emphasize that this is preliminary analysis requiring medical professional review."""
        
        return prompt
    
    def _create_followup_system_prompt(self) -> str:
        """Create system prompt for follow-up questions"""
        return """You are Dr. AI, continuing a conversation with a patient about their chest X-ray results. You should:

1. Answer questions clearly and compassionately
2. Refer back to the original analysis when relevant
3. Provide educational information about chest X-rays and lung health
4. Always emphasize consulting with healthcare professionals
5. Avoid giving specific medical advice or diagnoses
6. Be supportive and reduce unnecessary anxiety

Remember to maintain consistency with previous analysis and always recommend professional medical consultation for specific medical decisions."""
    
    def _create_followup_prompt(
        self,
        question: str,
        yolo_results: Dict[str, Any],
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        """Create follow-up question prompt"""
        
        prompt = f"""PATIENT QUESTION: {question}

ORIGINAL X-RAY ANALYSIS:
- Findings: {yolo_results.get('total_detections', 0)} potential areas of interest
- Confidence: {yolo_results.get('confidence', 0.0):.1%}
- Summary: {yolo_results.get('summary', 'No summary available')}
"""
        
        if conversation_history:
            prompt += "\nCONVERSATION HISTORY:\n"
            for i, msg in enumerate(conversation_history[-5:], 1):  # Last 5 messages
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')
                prompt += f"{role.title()} {i}: {content[:200]}{'...' if len(content) > 200 else ''}\n"
        
        prompt += "\nPlease provide a helpful, accurate response that addresses the patient's question while maintaining appropriate medical boundaries."
        
        return prompt
    
    async def _generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generate response using Groq API"""
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=self.model,
                temperature=0.3,  # Lower temperature for more consistent medical responses
                max_tokens=1024,
                top_p=1,
                stop=None,
                stream=False,
            )
            
            response = chat_completion.choices[0].message.content
            
            # Log the interaction (without sensitive data)
            logger.info(f"LLM response generated successfully. Length: {len(response)} chars")
            
            return response
            
        except Exception as e:
            logger.error(f"Groq API call failed: {str(e)}")
            raise
    
    async def get_service_status(self) -> Dict[str, Any]:
        """Get service status information"""
        status = {
            "initialized": self.initialized,
            "model": self.model,
            "api_key_configured": bool(settings.GROQ_API_KEY),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        if self.initialized:
            try:
                api_valid = await self.validate_api_key()
                status["api_key_valid"] = api_valid
            except:
                status["api_key_valid"] = False
        
        return status


# Global LLM service instance
llm_service = LLMService()