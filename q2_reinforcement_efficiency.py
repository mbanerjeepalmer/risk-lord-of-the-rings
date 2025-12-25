import csv

def main():
    # Read the territories CSV
    with open('regions.csv', 'r') as infile:
        reader = csv.DictReader(infile)
        rows = []
        for row in reader:
            territories_count = int(row['territories_count'])
            reinforcements = int(row['reinforcements'])
            per_territory = reinforcements / territories_count
            rows.append([row['region'], row['territories_count'], row['colour'], row['reinforcements'], per_territory])
        # Sort by reinforcements_per_territory descending
        rows.sort(key=lambda x: x[4], reverse=True)
        # Prepare the output CSV
        with open('q2_reinforcement_efficiency.csv', 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['region', 'territories_count', 'colour', 'reinforcements', 'reinforcements_per_territory'])
            for row in rows:
                writer.writerow([row[0], row[1], row[2], row[3], f"{row[4]:.2f}"])

if __name__ == '__main__':
    main()