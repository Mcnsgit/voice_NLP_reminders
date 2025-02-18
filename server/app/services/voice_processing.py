from datetime import datetime, timedelta
import re
from typing import Dict, Optional, Tuple
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import VoiceInputStatus
from app.models.voice_input import VoiceInput
from app.repositories.voice_input import VoiceInputRepository


class VoiceService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = VoiceInputRepository(VoiceInput, session)

    async def process_voice_input(
        self, user_id: int, audio_file: UploadFile
    ) -> VoiceInput:
        try:
            # For MVP, just save the raw file and mark as pending
            voice_input = await self.repository.create(
                user_id=user_id,
                raw_text="",  # Will be filled after processing
                status=VoiceInputStatus.PENDING,
                confidence_score=0.0,
                metadata={
                    "filename": audio_file.filename,
                    "content_type": audio_file.content_type,
                },
            )

            # Start async processing (implement in next phase)
            # For MVP, we'll just update with a placeholder
            await self.repository.update(
                voice_input.id,
                status=VoiceInputStatus.COMPLETED,
                processed_text="Voice processing to be implemented",
                confidence_score=1.0,
            )

            return voice_input
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=500, detail=f"Error processing voice input: {str(e)}"
            )

    def process_command(self, voice_input: str) -> Dict:
        """
        Process natural language voice input into structured data.
        Handles various ways users might naturally express their thoughts.
        """
        # Normalize input
        text = voice_input.lower().strip()

        # Determine the type of item (reminder, task, or note)
        item_type = self._determine_type(text)

        # Extract timing information
        timing = self._extract_timing(text)

        # Extract priority level
        priority = self._determine_priority(text)

        # Extract the main content
        content = self._extract_content(text, item_type)

        return {
            "type": item_type,
            "content": content,
            "timing": timing,
            "priority": priority,
        }

    def _determine_type(self, text: str) -> str:
        """
        Determine whether the input should be a reminder, task, or note
        based on natural language indicators.
        """
        for item_type, indicators in self.command_indicators.items():
            if any(indicator in text for indicator in indicators):
                return item_type

        # Default to note if no clear indicators
        # People often just want to capture a thought without categorizing it
        return "note"

    def _extract_timing(self, text: str) -> Optional[datetime]:
        """
        Extract timing information from natural language.
        Handles various ways people might specify time.
        """
        for pattern_name, pattern in self.time_patterns.items():
            match = re.search(pattern, text)
            if match:
                # Convert the matched timing to a datetime
                return self._parse_time_match(pattern_name, match.group(1))

        return None

    def _parse_time_match(self, pattern_name: str, time_str: str) -> datetime:
        """
        Convert matched time string into a datetime object.
        Handles various natural language time expressions.
        """
        now = datetime.now()

        if pattern_name == "today":
            # Parse "today at X" time
            time_parts = self._parse_time_string(time_str)
            return now.replace(hour=time_parts[0], minute=time_parts[1])

        elif pattern_name == "tomorrow":
            # Parse "tomorrow at X" time
            time_parts = self._parse_time_string(time_str)
            tomorrow = now + timedelta(days=1)
            return tomorrow.replace(hour=time_parts[0], minute=time_parts[1])

        elif pattern_name == "relative":
            # Parse "in X minutes/hours/days"
            amount, unit = time_str.split()
            amount = int(amount)
            if "minute" in unit:
                return now + timedelta(minutes=amount)
            elif "hour" in unit:
                return now + timedelta(hours=amount)
            elif "day" in unit:
                return now + timedelta(days=amount)

        return now

    def _parse_time_string(self, time_str: str) -> Tuple[int, int]:
        """
        Parse time string into hour and minute components.
        Handles various time formats like "3pm", "15:30", "3:45pm".
        """
        # Remove any whitespace
        time_str = time_str.strip().lower()

        # Initialize variables
        hour = 0
        minute = 0
        is_pm = "pm" in time_str

        # Remove am/pm indicators
        time_str = time_str.replace("am", "").replace("pm", "").strip()

        # Split into hours and minutes if colon exists
        if ":" in time_str:
            hour_str, minute_str = time_str.split(":")
            hour = int(hour_str)
            minute = int(minute_str)
        else:
            hour = int(time_str)

        # Adjust hour for PM times
        if is_pm and hour < 12:
            hour += 12

        return hour, minute

    def _determine_priority(self, text: str) -> str:
        """
        Determine priority based on language used.
        Defaults to medium if no priority indicators found.
        """
        for level, indicators in self.priority_indicators.items():
            if any(indicator in text for indicator in indicators):
                return level
        return "medium"

    def _extract_content(self, text: str, item_type: str) -> str:
        """
        Extract the main content from the voice input.
        Removes command indicators and timing information to get the core message.
        """
        # Remove command indicators
        for indicators in self.command_indicators.values():
            for indicator in indicators:
                text = text.replace(indicator, "")

        # Remove timing information
        for pattern in self.time_patterns.values():
            text = re.sub(pattern, "", text)

        # Remove priority indicators
        for indicators in self.priority_indicators.values():
            for indicator in indicators:
                text = text.replace(indicator, "")

        return text.strip()
