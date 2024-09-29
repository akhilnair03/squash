import React from "react";
import { TouchableOpacity, Image, StyleSheet } from "react-native";
import { getStatusBarHeight } from "react-native-status-bar-height";

const imageMap = {
  'back.png': require('../../assets/items/back.png'),
  'camera.jpg': require('../../assets/items/camera.jpg'),
  // Add more image files here if needed
  // 'otherImage.png': require('../../assets/items/otherImage.png'),
};

export default function AppIcon({ filename, functionality }) {
  console.log(filename)
  console.log(functionality)
  return (
    <TouchableOpacity onPress={functionality} style={styles.container}>
      <Image
        style={styles.image}
        source={imageMap[filename]}
      />
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    // position: "absolute",
    // top: 10 + getStatusBarHeight(),
    // left: 4,
  },
  image: {
    width: 24,
    height: 24,
  },
});
