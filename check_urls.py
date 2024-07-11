import requests
import csv

def check_url(url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code
    except requests.RequestException as e:
        return str(e)

def check_urls_from_url(url):
    response = requests.get(url)
    urls = response.text.splitlines()
    results = []
    for url in urls:
        status = check_url(url)
        results.append((url, status))
    return results

def save_results_to_csv(results, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['URL', 'Status'])
        writer.writerows(results)

input_url = 'https://raw.githubusercontent.com/viejojavi/mk/main/listado_urls.txt'
output_file = 'results.csv'

results = check_urls_from_url(input_url)
save_results_to_csv(results, output_file)

print(f"Resultados guardados en {output_file}")
