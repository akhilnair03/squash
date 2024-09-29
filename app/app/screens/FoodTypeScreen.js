import React from "react";
import Background from "../components/Background";
import AppIcon from "../components/AppIcon";
import { View, Text, StyleSheet } from "react-native";

export default function FoodType({ route, navigation }) {
  const { type } = route.params;

  return (
    <Background>
        <AppIcon filename={"back.png"} functionality={navigation.goBack} />
        <View style={styles.container}>
            <Text style={styles.title}>{type} Menu</Text>
            {/* Add your food items or logic here based on type */}
        </View>

    </Background>
    
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
  },
});
