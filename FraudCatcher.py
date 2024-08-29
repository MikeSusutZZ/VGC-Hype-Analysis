import requests
from datetime import datetime

# Step 1: Fetch the list of tournaments from the API
response = requests.get('https://labmaus-website-b7a5f5f01a05.herokuapp.com/api/tournaments')
tournaments = response.json()

# Step 2: Get user input for date range
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")

# Step 3: Get user input for regulation letter
regulation_letter = input("Enter the regulation letter (e.g., H, G, F): ")

# Convert user input to datetime objects
start_date = datetime.strptime(start_date, "%Y-%m-%d")
end_date = datetime.strptime(end_date, "%Y-%m-%d")

# Step 4: Filter by date range
filtered_tournaments = [
    tournament for tournament in tournaments
    if start_date <= datetime.strptime(tournament['date'], "%Y-%m-%d") <= end_date
]

# Step 5: Filter by number of players
filtered_tournaments = [
    tournament for tournament in filtered_tournaments
    if tournament['players'] >= 100
]

# Step 6: Filter by format (based on user input)
filtered_tournaments = [
    tournament for tournament in filtered_tournaments
    if tournament['regulation'] == f"Scarlet & Violet - Regulation {regulation_letter.upper()}"
]

# Step 7: Dictionary to store cumulative advancement rates, count, and total usages for each Pokémon
pokemon_advancement_data = {}

# Step 8: For each tournament, fetch detailed info and filter Pokémon
for tournament in filtered_tournaments:
    print(f"Analyzing {tournament['name']}...")

    tournament_id = tournament['id']
    details_response = requests.get(f'https://labmaus-website-b7a5f5f01a05.herokuapp.com/api/tournaments/{tournament_id}?language=en')
    tournament_details = details_response.json()

    # Step 9: Filter Pokémon with at least 10 appearances
    valid_pokemon = [
        pokemon for pokemon in tournament_details['pokemon']
        if pokemon['appearances'] >= 10
    ]

    # Step 10: Integer divide the number of participants by 4
    participants_divided = tournament['players'] // 4

    # Step 11: Make a new API call with the divided participants
    advancement_response = requests.get(f'https://labmaus-website-b7a5f5f01a05.herokuapp.com/api/tournaments/{tournament_id}/{participants_divided}?language=en')
    advancement_details = advancement_response.json()

    # Step 12: Match and accumulate advancement rates and usages
    for adv_pokemon in advancement_details['pokemon']:
        for pokemon in valid_pokemon:
            if pokemon['pokemon'] == adv_pokemon['pokemon']:
                if pokemon['pokemon'] not in pokemon_advancement_data:
                    pokemon_advancement_data[pokemon['pokemon']] = {
                        'total_advancement': 0.0,
                        'count': 0,
                        'total_usage': 0
                    }
                pokemon_advancement_data[pokemon['pokemon']]['total_advancement'] += float(adv_pokemon['advance_rate'].strip('%'))
                pokemon_advancement_data[pokemon['pokemon']]['count'] += 1
                pokemon_advancement_data[pokemon['pokemon']]['total_usage'] += pokemon['appearances']

# Step 13: Calculate and subtract 25 from average advancement rates
adjusted_advancement_data = {}
for pokemon_name, data in pokemon_advancement_data.items():
    average_advancement_rate = data['total_advancement'] / data['count']
    adjusted_advancement_data[pokemon_name] = {
        'adjusted_rate': average_advancement_rate - 25,
        'total_usage': data['total_usage']
    }

# Step 14: Sort the Pokémon by adjusted advancement rates in descending order
sorted_pokemon = sorted(adjusted_advancement_data.items(), key=lambda item: item[1]['total_usage'], reverse=True)

# Step 15: Print the sorted Pokémon with their adjusted advancement rates and total usages
print("\nAdjusted Advancement Rates (after subtracting 25) and Total Usages:")
for pokemon_name, data in sorted_pokemon:
    print(f"{pokemon_name}: {data['adjusted_rate']:.2f}%  ---  Total Usage: {data['total_usage']}")
