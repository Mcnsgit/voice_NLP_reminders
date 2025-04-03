import * as tf from "@tensorflow/tfjs";
import * as speechComands from "@tensorflow-models/speech-commands";
import { Audio } from "expo-av";

//flag to track if regonition is in progress
let isRecognizing = false;
let recognizer = null;

/**!SECTION
 * initialize the recognizer model
 */
export const setupVoiceRecognition = async () => {
  try {
    //reques audio recording permissions
    const { status } = await Audio.requestPermissionsAsync();
    if (status !== "granted") {
      console.error("Audio recording permissions not granted");
      return false;
    }

    //load tensorflow model
    await tf.ready();
    console.log("tensorFlow.js ready");

    //create and load the recognizer
    recognizer = speechComands.create("BROWSER_FFT");
    await recognizer.ensureModelLoaded();
    console.log("Speech commands model loaded");

    return true;
  } catch (error) {
    console.error("Error setting up voice recognition:", error);
    return false;
  }
};

/*!SECTION
 * start listening for voice commands
 * @param {function} onTranscript - callback when text is recognized
 */
export const startListening = async (onTranscript) => {
  if (isRecognizing || !recognizer) {
    return false;
  }

  try {
    const recording = new Audio.Recording();
    await recording.prepareToRecordAsync(
      Audio.RecordingOptionsPresets.HIGH_QUALITY
    );
    await recording.startAsync();

    isRecognizing = true;

    // In a real implementation, we would stream audio data to the recognizer
    // This is a simplified version
    recognizer.listen(
      (result) => {
        // Process the recognition result
        if (result.scores[0] > 0.75) {
          const command = result.spectrogram.toString();
          onTranscript(command);
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

/**!SECTION
 * stop listenin for voice commands
 */

export const stopLiatening = async () => {
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
