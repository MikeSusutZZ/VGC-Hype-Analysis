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

# Step 7: Dictionary to store total usages before and after dividing participants by 4
pokemon_usage_data = {}

# Step 8: For each tournament, fetch detailed info and accumulate usage data
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

    # Step 10: Accumulate total usages before dividing participants by 4
    for pokemon in valid_pokemon:
        if pokemon['pokemon'] not in pokemon_usage_data:
            pokemon_usage_data[pokemon['pokemon']] = {
                'total_usage_before': 0,
                'total_usage_after': 0
            }
        pokemon_usage_data[pokemon['pokemon']]['total_usage_before'] += pokemon['appearances']

    # Step 11: Integer divide the number of participants by 4
    participants_divided = tournament['players'] // 4

    # Step 12: Make a new API call with the divided participants
    advancement_response = requests.get(f'https://labmaus-website-b7a5f5f01a05.herokuapp.com/api/tournaments/{tournament_id}/{participants_divided}?language=en')
    advancement_details = advancement_response.json()

    # Step 13: Accumulate total usages after taking top 25% cut
    for adv_pokemon in advancement_details['pokemon']:
        if adv_pokemon['pokemon'] in pokemon_usage_data:
            pokemon_usage_data[adv_pokemon['pokemon']]['total_usage_after'] += adv_pokemon['appearances']

# Step 14: Calculate the ratio, subtract 25, and store the results
adjusted_usage_data = {}
for pokemon_name, data in pokemon_usage_data.items():
    if data['total_usage_after'] > 0:  # Avoid division by zero
        ratio = (data['total_usage_after'] / data['total_usage_before']) * 100 - 25
    else:
        ratio = 0
    adjusted_usage_data[pokemon_name] = {
        'adjusted_ratio': ratio,
        'total_usage_before': data['total_usage_before'],
        'total_usage_after': data['total_usage_after']
    }

# Step 15: Sort the Pokémon by adjusted ratio in descending order
sorted_pokemon = sorted(adjusted_usage_data.items(), key=lambda item: item[1]['total_usage_before'], reverse=True)

# Step 16: Print the sorted Pokémon with their adjusted ratios and total usages
print("\nAdjusted Usage Ratios")
for pokemon_name, data in sorted_pokemon:
    print(f"{pokemon_name}: {data['adjusted_ratio']:.2f}% (Total: {data['total_usage_before']}, Top 25%: {data['total_usage_after']})")
