import { VoiceProcessingResult } from '@/types';
import axios from 'axios';


const API_URL = import.meta.env.VITE_FASTAPI_URL || "https://myapi.onrender.com"|| 'http://localhost:8000/api/v1';

const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
      'Content-Type': 'multipart/form-data',
    },
});

export const voiceApi = {
  // Process voice recording
  processVoice: async (audioFile: string): Promise<VoiceProcessingResult> => {
    try {
      // Create form data
      const formData = new FormData();
      formData.append('file', {
        uri: audioFile,
        name: 'recording.wav',
        type: 'audio/wav',
      } as any);
      
      const response = await apiClient.post('/voice/process', formData);
      return response.data;
    } catch (error) {
      console.error('Error processing voice:', error);
      throw error;
    }
  },
};
export default apiClient;