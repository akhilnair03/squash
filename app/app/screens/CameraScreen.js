import { CameraView, CameraType, useCameraPermissions } from 'expo-camera';
import { useState, useRef } from 'react';
import { Button, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import AppIcon from '../components/AppIcon';

export default function CameraScreen({ navigation }) {
  console.log("1");
  const [facing, setFacing] = useState('back');
  const cameraRef = useRef(null);
  console.log("2");
  const [permission, requestPermission] = useCameraPermissions();
  console.log("3");

  if (!permission) {
    // Camera permissions are still loading.
    return <View />;
  }
  console.log("4");

  if (!permission.granted) {
    // Camera permissions are not granted yet.
    return (
      <View style={styles.container}>
        <Text style={styles.message}>We need your permission to show the camera</Text>
        <Button onPress={requestPermission} title="grant permission" />
      </View>
    );
  }
  console.log("5");

  function toggleCameraFacing() {
    setFacing(current => (current === 'back' ? 'front' : 'back'));
  }
  console.log("6");

  const handleTakePhoto =  async () => {
    if (cameraRef.current) {
        const options = {
            quality: 1,
            base64: true,
            exif: false,
        };
        const data = await cameraRef.current.takePictureAsync(options);
        const base64Image = data["base64"]; // Your base64 string
        console.log(base64Image)
        const requestBody = {
            data: base64Image
        }

        // Make the fetch call
        fetch('http://localhost:8000/upload_receipt', {
            method: 'POST',
            body: JSON.stringify(requestBody)
            
        }).then(response => response.json())
        .then(data => {
          console.log('Success:', data);
        })
        .catch(error => {
          console.error('Error:', error);
        });
    }
  }; 

  return (
    <View style={styles.container}>
      <AppIcon filename={"back.png"} functionality={navigation.goBack} />
      <CameraView style={styles.camera} facing={facing} ref={cameraRef}>
        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.button} onPress={handleTakePhoto}>
            <Text style={styles.text}>Take Picture</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.button} onPress={toggleCameraFacing}>
            <Text style={styles.text}>Flip Camera</Text>
          </TouchableOpacity>
        </View>
      </CameraView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
  message: {
    textAlign: 'center',
    paddingBottom: 10,
  },
  camera: {
    flex: 1,
  },
  buttonContainer: {
    flex: 1,
    flexDirection: 'row',
    backgroundColor: 'transparent',
    margin: 64,
  },
  button: {
    flex: 1,
    alignSelf: 'flex-end',
    alignItems: 'center',
  },
  text: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  },
});
