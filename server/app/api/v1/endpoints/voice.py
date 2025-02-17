# @router.post("/voice/process", response_model=VoiceProcessingResponse)
# async def process_voice_command(
#     audio_data: UploadFile, current_user: User = Depends(get_current_user)
# ):
#     """Process voice command and convert to task/note"""


# @router.post("/voice/text", response_model=TextProcessingResponse)
# async def process_text_command(
#     command: TextCommand, current_user: User = Depends(get_current_user)
# ):
#     """Process natural language text command"""
