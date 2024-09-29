import React, { useEffect, useState } from "react";
import Background from "../components/Background";
import AppIcon from "../components/AppIcon";
import { View, Text, StyleSheet, ActivityIndicator, FlatList } from "react-native";

export default function FoodType({ route, navigation }) {
  console.log("ROUTE", route)
  const { type } = route.params;
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        console.log("Type", type)
        const response = await fetch('http://localhost:8000/get_recipes', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ "food_type": type }),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        setRecipes(data); // Assuming the response is an array of recipes
        console.log("before")
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
        <Text style={styles.title}>{type.charAt(0).toUpperCase() + type.slice(1)} Menu</Text>
        <FlatList
          data={recipes}
          keyExtractor={(item) => item.name} // Assuming name is unique
          renderItem={({ item }) => (
            <View style={styles.recipeItem}>
              <Text style={styles.recipeTitle}>{item.name}</Text>
              <Text style={styles.label}>Ingredients:</Text>
              {item.ingredients.map((ingredient, index) => (
                <Text key={index}>
                  {ingredient.ingredient_name}: {ingredient.quantity}
                </Text>
              ))}
              <Text style={styles.label}>Cooking Time: {item.time}</Text>
              <Text style={styles.label}>Instructions:</Text>
              {item.instructions.map((step, index) => (
                <Text key={index}>
                  {index + 1}. {step}
                </Text>
              ))}
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