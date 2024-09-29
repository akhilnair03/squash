import React, { useEffect, useState } from "react";
import Background from "../components/Background";
import AppIcon from "../components/AppIcon";
import { View, Text, StyleSheet } from "react-native";

export default function FoodType({ route, navigation }) {
  const { type } = route.params;
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        const response = await fetch('localhost:8000/get_recipes/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ FoodType: type }),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        setRecipes(data); // Assuming the response is an array of recipes
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchRecipes();
  }, [type]);

  if (loading) {
    return (
      <Background>
        <ActivityIndicator size="large" color="#0000ff" />
      </Background>
    );
  }

  if (error) {
    return (
      <Background>
        <Text style={styles.errorText}>{error}</Text>
      </Background>
    );
  }

  return (
    <Background>
      <AppIcon filename={"back.png"} functionality={navigation.goBack} />
      <View style={styles.container}>
        <Text style={styles.title}>{type} Menu</Text>
        <FlatList
          data={recipes}
          keyExtractor={(item) => item.id.toString()} // Make sure item has a unique key
          renderItem={({ item }) => (
            <View style={styles.recipeItem}>
              <Text style={styles.recipeTitle}>{item.title}</Text>
              <Text>{item.description}</Text> {/* Adjust based on the structure of your recipe objects */}
            </View>
          )}
        />
      </View>
    </Background>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  recipeItem: {
    marginVertical: 10,
    padding: 15,
    backgroundColor: '#f9f9f9',
    borderRadius: 10,
    width: '100%', // You can adjust this as needed
  },
  recipeTitle: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  errorText: {
    color: 'red',
    fontSize: 18,
  },
});