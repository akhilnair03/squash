import React, { useState, useEffect } from "react";
import { View, StyleSheet, Alert, Text } from "react-native";
import Background from "../components/Background";
import Header from "../components/Header";
import AppIcon from "../components/AppIcon"; // Your microphone icon component
import Button from "../components/Button";
import { Audio } from 'expo-av';
import * as FileSystem from 'expo-file-system';
import Constants from 'expo-constants';

export default function HomeScreen({ navigation }) {
  const [recording, setRecording] = useState(null);
  const [transcription, setTranscription] = useState('');
  const [isRecording, setIsRecording] = useState(false);

  useEffect(() => {
    (async () => {
      const audioPermission = await Audio.requestPermissionsAsync();
      if (audioPermission.status !== 'granted') {
        Alert.alert("Microphone Permission", "Permission to access microphone is required.");
      }
    })();
  }, []);

  const startRecording = async () => {
    try {
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });
      const { recording } = await Audio.Recording.createAsync(
        Audio.RECORDING_OPTIONS_PRESET_HIGH_QUALITY
      );
      setRecording(recording);
      setIsRecording(true);
    } catch (err) {
      console.error('Failed to start recording', err);
    }
  };

  const stopRecording = async () => {
    try {
      setIsRecording(false);
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI(); // Get the recording file URI
      console.log('Recording finished and stored at', uri);
  
      // Transcribe the audio after recording stops
      setTimeout(async () => {
        // Transcribe the audio after a delay
        await transcribeAudio(recording);
      }, 3000); 
    } catch (error) {
      console.error('Failed to stop recording', error);
    }
  };
  
  const transcribeAudio = async (recording) => {
    try {
        const uri = recording.getURI(); // Get the URI of the recording
        const response = await fetch(uri);
        const blob = await response.blob();

        const reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onloadend = async () => {
            const base64data = reader.result.split(',')[1]; // Extract the base64 part
            console.log(base64data);
            const requestBody = {
                transcript: base64data, // Use the Base64 data here
            };

            try {
                const apiResponse = await fetch('http://localhost:8000/upload_speech', { // Change localhost to your local IP
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestBody),
                });

                const responseData = await apiResponse.json();

                // Assuming your API returns the transcribed text
                if (responseData && responseData.transcribedText) {
                    setTranscription(responseData.transcribedText);
                } else {
                    console.warn('No transcription available in response:', responseData);
                    setTranscription('No transcription available.');
                }
            } catch (error) {
                console.error('Error during transcription:', error);
                setTranscription('Transcription failed.');
            }
        };
    } catch (error) {
        console.error('Failed to transcribe audio:', error);
        setTranscription('Transcription failed.');
    }
};


  const handleMicrophonePress = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  return (
    <Background style={styles.wrapper}>
      <View style={styles.topright}>
        <Header>Welcome 💫</Header>
        <AppIcon filename={"microphone.png"} functionality={handleMicrophonePress} />
      </View>

      <View style={styles.buttonContainer}>
        <Button onPress={() => navigation.navigate("FoodTypeScreen", { type: "breakfast" })}>
          Breakfast
        </Button>
        <Button onPress={() => navigation.navigate("FoodTypeScreen", { type: "lunch" })}>
          Lunch
        </Button>
        <Button onPress={() => navigation.navigate("FoodTypeScreen", { type: "dinner" })}>
          Dinner
        </Button>
      </View>

      <Button
        mode="contained"
        onPress={() =>
          navigation.reset({
            index: 0,
            routes: [{ name: "StartScreen" }],
          })
        }
        style={styles.b}
      >
        Sign out
      </Button>

      {transcription ? <Text style={styles.transcriptionText}>{transcription}</Text> : null}
    </Background>
  );
}

const styles = StyleSheet.create({
  buttonContainer: {
    marginTop: 20,
    width: '100%',
    alignItems: 'center',
  },
  wrapper: {
    flex: 1,
  },
  b: {
    marginTop: 100,
  },
  topright: {
    flexDirection: 'row',
    marginBottom: 20,
  },
  transcriptionText: {
    marginTop: 20,
    fontSize: 16,
    color: 'black',
    textAlign: 'center',
  },
});
