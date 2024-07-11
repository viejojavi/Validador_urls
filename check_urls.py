import requests
from concurrent.futures import ThreadPoolExecutor
import csv

def check_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return url, response.status_code
    except requests.RequestException as e:
        return url, str(e)

def check_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]

    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_url, url) for url in urls]
        for future in futures:
            results.append(future.result())

    return results

def save_results_to_csv(results, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Status"])
        writer.writerows(results)

if __name__ == "__main__":
    input_file = 'https://raw.githubusercontent.com/viejojavi/mk/main/listado_urls.txt'  # Archivo con las URLs a verificar
    output_file = 'results.csv'  # Archivo de salida con los resultados

    results = check_urls_from_file(input_file)
    save_results_to_csv(results, output_file)

    print(f"Resultados guardados en {output_file}")
