import * as tf from "@tensorflow/tfjs";
import * as speechCommands from "@tensorflow-models/speech-commands";
import { Audio } from "expo-av";
// Flag to track if recognition is in progress
let isRecognizing = false;
let recognizer: speechCommands.SpeechCommandRecognizer | null = null;
/**
 * Initialize the recognizer model
 */
export const setupVoiceRecognition = async (): Promise<boolean> => {
  try {
    // Request audio recording permissions
    const { status } = await Audio.requestPermissionsAsync();
    if (status !== "granted") {
      console.error("Audio recording permissions not granted");
      return false;
    }
    // Load TensorFlow model
    await tf.ready();
    console.log("TensorFlow.js ready");
    // Create and load the recognizer
    recognizer = speechCommands.create("BROWSER_FFT");
    await recognizer.ensureModelLoaded();
    console.log("Speech commands model loaded");
    return true;
  } catch (error) {
    console.error("Error setting up voice recognition:", error);
    return false;
  }
};
/**
 * Start listening for voice commands
 * @param {function} onTranscript - Callback when text is recognized
 */
export const startListening = async (onTranscript: (command: string) => void): Promise<boolean> => {
  if (isRecognizing || !recognizer) {
    return false;
  }
  try {
    const recording = new Audio.Recording();
    await recording.prepareToRecordAsync(Audio.RecordingOptionsPresets.HIGH_QUALITY);
    await recording.startAsync();
    isRecognizing = true;
    // In a real implementation, we would stream audio data to the recognizer
    // This is a simplified version
    recognizer.listen(
      async (result) => {
        // Process the recognition result
        if (typeof result.scores[0] === "number" && result.scores[0] > 0.75) {
          const command = result.spectrogram ? result.spectrogram.toString() : "";
          await onTranscript(command);
        }
      },
      { probabilityThreshold: 0.75 }
    );
    return true;
  } catch (error) {
    console.error("Error starting voice recognition:", error);
    isRecognizing = false;
    return false;
  }
};
/**
 * Stop listening for voice commands
 */
export const stopListening = async (): Promise<boolean> => {
  if (!isRecognizing || !recognizer) {
    return false;
  }
  try {
    recognizer.stopListening();
    isRecognizing = false;
    return true;
  } catch (error) {
    console.error("Error stopping voice recognition:", error);
    return false;
  }
};