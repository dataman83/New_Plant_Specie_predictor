import random
import pandas as pd

# Load the dataset
file_path = 'Tasmanian_plant_trait_data.csv'
tasmanian_plant_data = pd.read_csv(file_path)

# Extract relevant traits
existing_species = tasmanian_plant_data[['Plant_height_(m)', 'Leaf_Area_cm2', 'Seed_Mass_g']].to_dict('records')

# Define the range of traits based on the existing dataset
traits_range = {
    'Plant_height_(m)': (min(species['Plant_height_(m)'] for species in existing_species), max(species['Plant_height_(m)'] for species in existing_species)),
    'Leaf_Area_cm2': (min(species['Leaf_Area_cm2'] for species in existing_species), max(species['Leaf_Area_cm2'] for species in existing_species)),
    'Seed_Mass_g': (min(species['Seed_Mass_g'] for species in existing_species), max(species['Seed_Mass_g'] for species in existing_species))
}

# Fitness function
def fitness(species):
    survivability = 1.0 / abs(species['Plant_height_(m)'])  # Favor height around 15 meters
    leaf_area_advantage = 1.0 / abs(species['Leaf_Area_cm2'] - 10)  # Favor leaf area around 10 cm2
    seed_mass_advantage = 1.0 / abs(species['Seed_Mass_g'] - 0.01)  # Favor seed mass around 0.01 g
    return survivability + leaf_area_advantage + seed_mass_advantage

# Generate potential new traits
def generate_new_traits(existing_species):
    new_traits = {}
    for trait in existing_species[0].keys():
        # Combine traits from existing species with slight random variations
        new_traits[trait] = random.uniform(
            min(species[trait] for species in existing_species) * 0.9,
            max(species[trait] for species in existing_species) * 1.1
        )
    return new_traits

# Backtracking function
def backtrack(existing_species, attempts, max_attempts):
    if attempts >= max_attempts:
        return None  # Exceeded the maximum number of attempts

    new_species = generate_new_traits(existing_species)
    if fitness(new_species) > fitness(max(existing_species, key=fitness)):
        return new_species  # Found a viable new species

    # Recursively try to find a viable new species
    return backtrack(existing_species, attempts + 1, max_attempts)

# Main function
def find_new_species(existing_species, max_attempts):
    new_species = backtrack(existing_species, 0, max_attempts)
    if new_species:
        print(f"Predicted new plant species: {new_species}")
    else:
        print("Could not find a viable new species within the given attempts.")

# Parameters
max_attempts = 1000

# Run the algorithm
find_new_species(existing_species, max_attempts)
