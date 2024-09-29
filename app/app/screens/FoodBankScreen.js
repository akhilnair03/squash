import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, ActivityIndicator } from 'react-native';

export default function FoodBanksScreen() {
  const [foodBanks, setFoodBanks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFoodBanks = async () => {
      try {
        const response = await fetch('http://localhost:8000/find_food_banks'); // Update this if needed
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setFoodBanks(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchFoodBanks();
  }, []);

  if (loading) {
    return (
      <View style={styles.loader}>
        <ActivityIndicator size="large" color="#0000ff" />
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.container}>
        <Text style={styles.error}>{error}</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Food Banks Near You</Text>
      <FlatList
        data={foodBanks}
        keyExtractor={(item) => item.name}
        renderItem={({ item }) => (
          <View style={styles.item}>
            <Text style={styles.bankName}>{item.name}</Text>
            <Text>{item.address}</Text>
            <Text>Distance: {item.distance_km.toFixed(2)} km</Text>
            <Text style={styles.openingHours}>Opening Hours:</Text>
            {Array.isArray(item.opening_hours) ? (
              item.opening_hours.map((hour, index) => (
                <Text key={index}>{hour}</Text>
              ))
            ) : (
              <Text>{item.opening_hours}</Text>
            )}
            <Text>Phone: {item.phone_number}</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  item: {
    backgroundColor: '#fff',
    padding: 15,
    marginVertical: 10,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 3,
  },
  bankName: {
    fontSize: 20,
    fontWeight: '600',
  },
  openingHours: {
    fontWeight: 'bold',
    marginTop: 10,
  },
  loader: {
    flex: 1,
    justifyContent: 'center',
  },
  error: {
    color: 'red',
    textAlign: 'center',
    marginTop: 20,
  },
});