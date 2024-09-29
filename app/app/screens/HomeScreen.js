import React from "react";
import { View, StyleSheet } from "react-native";
import Background from "../components/Background";
import Logo from "../components/Logo";
import Header from "../components/Header";
import Paragraph from "../components/Paragraph";
import Button from "../components/Button";

export default function HomeScreen({ navigation }) {
  return (
    <Background style={styles.wrapper}>
      <View style={styles.topright}>
        <Header>Welcome 💫</Header>
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
  }
  // topright: {
  //   flexDirection: 'row', // Align items in a row
  //   justifyContent: 'flex-end', // Align contents to the right
  //   alignItems: 'flex-start', // Align items to the top
  //   marginBottom: 20, // Optional spacing below
  // }
});
