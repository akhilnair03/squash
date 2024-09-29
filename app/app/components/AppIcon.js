import React from "react";
import { TouchableOpacity, Image, StyleSheet } from "react-native";
import { getStatusBarHeight } from "react-native-status-bar-height";

const imageMap = {
  'back.png': require('../../assets/items/back.png'),
  // 'camera.jpg': require('../../assets/items/camera.jpg'),
  'microphone.png': require('../../assets/items/microphone.png')
  // Add more image files here if needed
  // 'otherImage.png': require('../../assets/items/otherImage.png'),
};

export default function AppIcon({ filename, functionality }) {
  console.log(filename)
  console.log(functionality)

  // Conditionally apply the container style for the back icon
  const containerStyle = filename === 'back.png' ? styles.container : styles.media;

  return (
    <TouchableOpacity onPress={functionality} style={containerStyle}>
      <Image
        style={styles.image}
        source={imageMap[filename]}
      />
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    position: "absolute", 
    top: 10 + getStatusBarHeight(), 
    left: 4, 
  },
  media: {
    position: "absolute", 
    top: 10 + getStatusBarHeight(), 
    left: 350,
  },
  image: {
    width: 24,
    height: 24,
  },
});
