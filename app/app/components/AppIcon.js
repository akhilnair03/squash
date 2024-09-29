import React from "react";
import { TouchableOpacity, Image, StyleSheet } from "react-native";
import { getStatusBarHeight } from "react-native-status-bar-height";

const imageMap = {
  'back.png': require('../../assets/items/back.png'),
  'back1.png': require('../../assets/items/back.png'),
  // 'camera.jpg': require('../../assets/items/camera.jpg'),
  'microphone.png': require('../../assets/items/microphone.png')
  // Add more image files here if needed
  // 'otherImage.png': require('../../assets/items/otherImage.png'),
};

export default function AppIcon({ filename, functionality }) {
  console.log(filename)
  console.log(functionality)

  // Conditionally apply the container style for the back icon
  let containerStyle = styles.defaultContainer;
  if (filename === 'back.png') {
    containerStyle = styles.container;
  } else if (filename === 'microphone.png') {
    containerStyle = styles.voice_media;
  }
  else if (filename === 'back1.png') {
    containerStyle = styles.defaultContainer;
  }

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
  defaultContainer: {
    // A default style if no filename condition is matched
    position: "absolute", 
    top: 10 + getStatusBarHeight(), 
    left: 4,
  },
  container: {
    // position: "absolute", 
    // top: 10 + getStatusBarHeight(), 
    // left: 4, 
  },
  voice_media: {
    position: "absolute", 
    top: 10 + getStatusBarHeight(), 
    left: 350,
  },
  image: {
    width: 24,
    height: 24,
  },
});
