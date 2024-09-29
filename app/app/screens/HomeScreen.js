import React, { useState, useEffect } from "react";
import { View, StyleSheet, Alert } from "react-native";
import Background from "../components/Background";
import Header from "../components/Header";
import AppIcon from "../components/AppIcon";
import Button from "../components/Button";
import { Camera } from 'expo-camera';
import { Audio } from 'expo-av';

export default function HomeScreen({ navigation }) {
  const [hasCameraPermission, setHasCameraPermission] = useState(null);
  const [hasAudioPermission, setHasAudioPermission] = useState(null);

  // Request permissions on component mount
  useEffect(() => {
    (async () => {
      const cameraPermission = await Camera.requestPermissionsAsync();
      const audioPermission = await Audio.requestPermissionsAsync();

      setHasCameraPermission(cameraPermission.status === 'granted');
      setHasAudioPermission(audioPermission.status === 'granted');
    })();
  }, []);

  // Handle camera functionality
  const handleCameraPress = () => {
    if (hasCameraPermission) {
      navigation.navigate("CameraScreen"); // Create this screen to handle camera input
    } else {
      Alert.alert("Camera Permission", "Permission to access camera is required.");
    }
  };

  // Handle microphone functionality
  const handleMicrophonePress = () => {
    if (hasAudioPermission) {
      // Implement microphone functionality here
      Alert.alert("Microphone", "Microphone functionality will be implemented here.");
    } else {
      Alert.alert("Microphone Permission", "Permission to access microphone is required.");
    }
  };

  return (
    <Background style={styles.wrapper}>
      <View style={styles.topright}>
        <Header>Welcome 💫</Header>
        <AppIcon filename={"camera.jpg"} functionality={handleCameraPress} />
        <AppIcon filename={"microphone.png"} functionality={handleMicrophonePress} />
      </View>
      <View style={styles.buttonContainer}>
        <Button onPress={() => navigation.navigate("FoodTypeScreen", { type: "Breakfast" })}>
          Breakfast
        </Button>
        <Button onPress={() => navigation.navigate("FoodTypeScreen", { type: "Lunch" })}>
          Lunch
        </Button>
        <Button onPress={() => navigation.navigate("FoodTypeScreen", { type: "Dinner" })}>
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
    flex: 1
  },
  b: {
    marginTop: 100
  },
  topright: {
    flexDirection: 'row',
    // justifyContent: 'flex-end',
    // alignItems: 'flex-start',
    marginBottom: 20,
  }
});