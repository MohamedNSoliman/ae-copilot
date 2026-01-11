"""
Gong API client for fetching call transcripts and extracting signals.
"""

import os
import json
import re
from typing import Optional
from pathlib import Path
import requests
from .schemas import ExtractedSignals, EvidenceQuote


class GongClient:
    """Client for interacting with Gong API."""
    
    def __init__(self, base_url: Optional[str] = None, access_key: Optional[str] = None, 
                 access_secret: Optional[str] = None, mock_mode: bool = False):
        """
        Initialize Gong client.
        
        Args:
            base_url: Gong API base URL
            access_key: Gong access key
            access_secret: Gong access secret
            mock_mode: If True, use mock data instead of API calls
        """
        self.mock_mode = mock_mode or os.getenv("GONG_MOCK_MODE", "false").lower() == "true"
        self.base_url = base_url or os.getenv("GONG_BASE_URL", "https://api.gong.io")
        self.access_key = access_key or os.getenv("GONG_ACCESS_KEY")
        self.access_secret = access_secret or os.getenv("GONG_ACCESS_SECRET")
        
        if not self.mock_mode and (not self.access_key or not self.access_secret):
            raise ValueError("Gong credentials required when not in mock mode")
    
    def extract_call_id(self, url_or_id: str) -> str:
        """
        Extract call ID from Gong URL or return as-is if already an ID.
        
        Args:
            url_or_id: Gong URL or call ID
            
        Returns:
            Call ID string
        """
        # Try to extract from URL pattern
        patterns = [
            r'/calls/([a-zA-Z0-9_-]+)',
            r'callId=([a-zA-Z0-9_-]+)',
            r'call_id=([a-zA-Z0-9_-]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url_or_id)
            if match:
                return match.group(1)
        
        # If no pattern matches, assume it's already an ID
        return url_or_id.strip()
    
    def fetch_transcript(self, call_id: str) -> dict:
        """
        Fetch transcript from Gong API or mock data.
        
        Args:
            call_id: Gong call ID
            
        Returns:
            Transcript data as dictionary
        """
        if self.mock_mode:
            return self._load_mock_transcript()
        
        # Authenticate and fetch transcript
        # Note: This is a simplified implementation. Real Gong API may require OAuth.
        headers = {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json"
        }
        
        # Fetch call details
        response = requests.get(
            f"{self.base_url}/v2/calls/{call_id}",
            headers=headers
        )
        response.raise_for_status()
        call_data = response.json()
        
        # Fetch transcript
        transcript_response = requests.get(
            f"{self.base_url}/v2/calls/{call_id}/transcript",
            headers=headers
        )
        transcript_response.raise_for_status()
        transcript_data = transcript_response.json()
        
        return {
            "call_id": call_id,
            "call_data": call_data,
            "transcript": transcript_data
        }
    
    def _get_access_token(self) -> str:
        """
        Get access token for Gong API.
        Simplified implementation - real API may use OAuth flow.
        """
        # In a real implementation, this would handle OAuth or API key authentication
        # For MVP, we'll use basic auth or API key
        if self.access_key and self.access_secret:
            # This is a placeholder - actual Gong auth may differ
            return f"{self.access_key}:{self.access_secret}"
        raise ValueError("Gong credentials not configured")
    
    def _load_mock_transcript(self) -> dict:
        """Load mock transcript from sample data."""
        mock_path = Path(__file__).parent.parent / "data" / "sample_transcript.json"
        if mock_path.exists():
            with open(mock_path, 'r') as f:
                return json.load(f)
        
        # Return default mock data
        return {
            "call_id": "mock_call_123",
            "call_data": {
                "title": "Discovery Call - Acme Corp",
                "duration": 1800,
                "participants": ["John Doe", "Jane Smith"]
            },
            "transcript": {
                "text": "We have about 50 engineers on the team. Currently using GitHub Copilot and some custom tooling. We're looking to improve developer productivity. Our team spends about 5 hours per week on repetitive coding tasks. We're evaluating several solutions.",
                "speakers": [
                    {"name": "John Doe", "text": "We have about 50 engineers on the team.", "timestamp": 30},
                    {"name": "Jane Smith", "text": "Currently using GitHub Copilot and some custom tooling.", "timestamp": 45},
                    {"name": "John Doe", "text": "We're looking to improve developer productivity.", "timestamp": 120},
                    {"name": "John Doe", "text": "Our team spends about 5 hours per week on repetitive coding tasks.", "timestamp": 180},
                    {"name": "Jane Smith", "text": "We're evaluating several solutions.", "timestamp": 240}
                ]
            }
        }
    
    def extract_signals(self, transcript_data: dict) -> ExtractedSignals:
        """
        Extract structured signals from transcript.
        Uses simple pattern matching - in production, could use LLM for better extraction.
        
        Args:
            transcript_data: Transcript data from fetch_transcript
            
        Returns:
            ExtractedSignals with evidence
        """
        transcript_text = ""
        speakers = []
        
        # Extract transcript text and speakers
        if "transcript" in transcript_data:
            if isinstance(transcript_data["transcript"], dict):
                transcript_text = transcript_data["transcript"].get("text", "")
                speakers = transcript_data["transcript"].get("speakers", [])
            elif isinstance(transcript_data["transcript"], str):
                transcript_text = transcript_data["transcript"]
        
        # Combine all text
        full_text = transcript_text.lower()
        if speakers:
            speaker_text = " ".join([s.get("text", "") for s in speakers])
            full_text = (full_text + " " + speaker_text.lower()).strip()
        
        signals = ExtractedSignals()
        evidence = []
        
        # Extract team size
        team_size_patterns = [
            r'(\d+)\s+engineers?',
            r'team\s+of\s+(\d+)',
            r'(\d+)\s+people\s+on\s+the\s+engineering\s+team',
        ]
        for pattern in team_size_patterns:
            match = re.search(pattern, full_text)
            if match:
                signals.team_size_engineering = int(match.group(1))
                # Find quote with timestamp
                quote = self._find_quote_for_pattern(pattern, speakers, transcript_text)
                if quote:
                    evidence.append(EvidenceQuote(
                        field_name="team_size_engineering",
                        quote=quote["text"],
                        timestamp_seconds=quote.get("timestamp")
                    ))
                break
        
        # Extract current tooling
        tooling_keywords = ["github copilot", "copilot", "cursor", "windsurf", "cody", "tabnine", "codeium"]
        for tool in tooling_keywords:
            if tool in full_text:
                signals.current_tooling.append(tool.title())
                quote = self._find_quote_for_keyword(tool, speakers, transcript_text)
                if quote:
                    evidence.append(EvidenceQuote(
                        field_name="current_tooling",
                        quote=quote["text"],
                        timestamp_seconds=quote.get("timestamp")
                    ))
        
        # Extract hours saved (only if explicitly stated)
        hours_patterns = [
            r'(\d+(?:\.\d+)?)\s+hours?\s+per\s+week',
            r'spend\s+(\d+(?:\.\d+)?)\s+hours?',
            r'(\d+(?:\.\d+)?)\s+hours?\s+saved',
        ]
        for pattern in hours_patterns:
            match = re.search(pattern, full_text)
            if match:
                signals.hours_saved_per_engineer_per_week = float(match.group(1))
                quote = self._find_quote_for_pattern(pattern, speakers, transcript_text)
                if quote:
                    evidence.append(EvidenceQuote(
                        field_name="hours_saved_per_engineer_per_week",
                        quote=quote["text"],
                        timestamp_seconds=quote.get("timestamp")
                    ))
                break
        
        # Extract pain points (simple keyword matching)
        pain_keywords = ["slow", "frustrating", "inefficient", "bottleneck", "problem", "issue", "challenge"]
        for keyword in pain_keywords:
            if keyword in full_text:
                # Find context around keyword
                quote = self._find_quote_for_keyword(keyword, speakers, transcript_text)
                if quote and quote["text"] not in [e.quote for e in evidence]:
                    signals.pain_points.append(keyword)
                    evidence.append(EvidenceQuote(
                        field_name="pain_points",
                        quote=quote["text"],
                        timestamp_seconds=quote.get("timestamp")
                    ))
        
        # Extract buying stage
        if any(word in full_text for word in ["evaluating", "evaluation", "comparing", "demo"]):
            signals.buying_stage = "evaluating"
        elif any(word in full_text for word in ["exploring", "looking into", "researching"]):
            signals.buying_stage = "exploring"
        elif any(word in full_text for word in ["procurement", "purchase", "buying", "contract"]):
            signals.buying_stage = "procurement"
        else:
            signals.buying_stage = "unaware"
        
        signals.evidence = evidence
        return signals
    
    def _find_quote_for_pattern(self, pattern: str, speakers: list, transcript_text: str) -> Optional[dict]:
        """Find a quote containing the pattern."""
        # Check speakers first
        for speaker in speakers:
            text = speaker.get("text", "").lower()
            if re.search(pattern, text):
                return speaker
        
        # Check transcript text
        if transcript_text:
            sentences = transcript_text.split('.')
            for sentence in sentences:
                if re.search(pattern, sentence.lower()):
                    return {"text": sentence.strip(), "timestamp": None}
        
        return None
    
    def _find_quote_for_keyword(self, keyword: str, speakers: list, transcript_text: str) -> Optional[dict]:
        """Find a quote containing the keyword."""
        keyword_lower = keyword.lower()
        
        # Check speakers first
        for speaker in speakers:
            text = speaker.get("text", "").lower()
            if keyword_lower in text:
                return speaker
        
        # Check transcript text
        if transcript_text:
            sentences = transcript_text.split('.')
            for sentence in sentences:
                if keyword_lower in sentence.lower():
                    return {"text": sentence.strip(), "timestamp": None}
        
        return None
