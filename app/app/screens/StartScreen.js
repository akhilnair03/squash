import React from "react";

import Background from "../components/Background";
import Logo from "../components/Logo";
import Header from "../components/Header";
import Button from "../components/Button";
import Paragraph from "../components/Paragraph";
import { usePermissions } from 'expo-media-library';
import { useCameraPermissions, useMicrophonePermissions } from 'expo-camera';

export default function StartScreen({ navigation }) {
  const [cameraPermissions, requestCameraPermission] = useCameraPermissions();
  const [microphonePermission, requestMicrophonePermission] = useMicrophonePermissions();
  const [mediaLibraryPermission, requestMediaLibraryPermission] = usePermissions();

  async function handleContinue() {
    const allPermissions = await requestAllPermissions();
    if (!allPermissions) {
      Alert.alert("To continue please provide permissions in settings");
    } else {
      router.replace("LoginScreen");
    }
  }

  async function requestAllPermissions() {
    const cameraStatus = await requestCameraPermission();
    if (!cameraStatus.granted) {
      Alert.alert("Error", "Camera permission is required")
      return false;
    }

    const microphoneStatus = await requestMicrophonePermission();
    if (!microphoneStatus.granted) {
      Alert.alert("Error", "Microphone permission is required")
      return false;
    }

    const mediaLibraryStatus = await requestMediaLibraryPermission();
    if (!mediaLibraryStatus.granted) {
      Alert.alert("Error", "Media library permission is required")
      return false;
    }
    await AsyncStorage.setItem("hasOpened", "true");
    return true;
  }
  return (
    <Background>
      <Logo />
      <Header>Squash</Header>
      <Paragraph>
        Your friendly and sustainable meal planner
      </Paragraph>
      <Button
        mode="contained"
        onPress={async () => {
          await handleContinue();
          navigation.navigate("LoginScreen")
        }}
      >
        Log in
      </Button>
      <Button
        mode="outlined"
        onPress={() => navigation.navigate("RegisterScreen")}
      >
        Create an account
      </Button>
    </Background>
  );
}
