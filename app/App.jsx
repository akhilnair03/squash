// App.jsx

import React, { useEffect } from "react";
import { Provider } from "react-native-paper";
import { useFonts } from 'expo-font';
import * as SplashScreen from 'expo-splash-screen';

import { theme } from "./app/core/theme";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import { createDrawerNavigator } from "@react-navigation/drawer";

import {
  StartScreen,
  LoginScreen,
  RegisterScreen,
  ResetPasswordScreen,
  HomeScreen,
  FoodBankScreen,
  InventoryScreen,
  FoodTypeScreen,
  CameraScreen
} from "./app/screens";

const Stack = createStackNavigator();
const Drawer = createDrawerNavigator();

// Prevent the splash screen from auto-hiding before asset loading is complete
SplashScreen.preventAutoHideAsync();

export default function App() {
  const [fontsLoaded] = useFonts({
    'Fredoka': require('./assets/fonts/Fredoka-Regular.ttf'), // Adjust the path as necessary
    // Add more fonts here if needed
  });

  useEffect(() => {
    const hideSplashScreen = async () => {
      if (fontsLoaded) {
        await SplashScreen.hideAsync();
      }
    };
    hideSplashScreen();
  }, [fontsLoaded]);

  if (!fontsLoaded) {
    return null; // Or return a loading indicator if desired
  }

  return (
    <Provider theme={theme}>
      <NavigationContainer>
        <Stack.Navigator
          initialRouteName="StartScreen"
          screenOptions={{ headerShown: false }}
        >
          <Stack.Screen name="StartScreen" component={StartScreen} />
          <Stack.Screen name="LoginScreen" component={LoginScreen} />
          <Stack.Screen name="RegisterScreen" component={RegisterScreen} />
          <Stack.Screen name="ResetPasswordScreen" component={ResetPasswordScreen} />
          <Stack.Screen name="HomeScreen" component={AppDrawerNavigator} />
          <Stack.Screen name="FoodTypeScreen" component={FoodTypeScreen} />
          <Stack.Screen name="CameraScreen" component={CameraScreen} />
        </Stack.Navigator>
      </NavigationContainer>
    </Provider>
  );
}

function AppDrawerNavigator() {
  return (
    <Drawer.Navigator initialRouteName="HomeScreen">
      <Drawer.Screen name="Home Screen" component={HomeScreen} />
      <Drawer.Screen name="Food Banks Near You" component={FoodBankScreen} />
      <Drawer.Screen name="Food Inventory" component={InventoryScreen} />
    </Drawer.Navigator>
  );
}
