#!/usr/bin/env python3

import re
import requests
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# ANSI escape codes for coloring
class Colors:
    URL_FOUND_COLOR = '\033[94m'  # Blue for "URL Found: "
    URL_COLOR = '\033[0m'         # White for the URL
    PATTERN_COLOR = '\033[92m'     # Green for "Pattern: " and matched patterns
    FAIL = '\033[91m'              # Red for errors
    ENDC = '\033[0m'               # Reset to default

# Define the regex pattern
pattern = r'(access_key|access_token|admin_pass|admin_user|algolia_admin_key|algolia_api_key|alias_pass|alicloud_access_key|amazon_secret_access_key|amazonaws|ansible_vault_password|aos_key|api_key|api_key_secret|api_key_sid|api_secret|api\.googlemaps AIza|apidocs|apikey|apiSecret|app_debug|app_id|app_key|app_log_level|app_secret|appkey|appkeysecret|application_key|appsecret|appspot|auth_token|authorizationToken|authsecret|aws_access|aws_access_key_id|aws_bucket|aws_key|aws_secret|aws_secret_key|aws_token|AWSSecretKey|b2_app_key|bashrc password|bintray_apikey|bintray_gpg_password|bintray_key|bintraykey|bluemix_api_key|bluemix_pass|browserstack_access_key|bucket_password|bucketeer_aws_access_key_id|bucketeer_aws_secret_access_key|built_branch_deploy_key|bx_password|cache_driver|cache_s3_secret_key|cattle_access_key|cattle_secret_key|certificate_password|ci_deploy_password|client_secret|client_zpk_secret_key|clojars_password|cloud_api_key|cloud_watch_aws_access_key|cloudant_password|cloudflare_api_key|cloudflare_auth_key|cloudinary_api_secret|cloudinary_name|codecov_token|config|conn\.login|connectionstring|consumer_key|consumer_secret|credentials|cypress_record_key|database_password|database_schema_test|datadog_api_key|datadog_app_key|db_password|db_server|db_username|dbpasswd|dbpassword|dbuser|deploy_password|digitalocean_ssh_key_body|digitalocean_ssh_key_ids|docker_hub_password|docker_key|docker_pass|docker_passwd|docker_password|dockerhub_password|dockerhubpassword|dot-files|dotfiles|droplet_travis_password|dynamoaccesskeyid|dynamosecretaccesskey|elastica_host|elastica_port|elasticsearch_password|encryption_key|encryption_password|env\.heroku_api_key|env\.sonatype_password|eureka\.awssecretkey)'

def check_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        content = response.text
        
        # Check for the pattern in the content
        matches = set()  # Use a set to avoid duplicate matches
        for line in content.splitlines():
            found_matches = re.findall(pattern, line, re.IGNORECASE)
            matches.update(found_matches)  # Add all matches found in this line
        
        if matches:
            # Print all matches found for this URL, joined by commas
            matches_list = ', '.join(matches)
            print(f"{Colors.URL_FOUND_COLOR}URL Found: {Colors.URL_COLOR}{url}{Colors.ENDC} - {Colors.PATTERN_COLOR}Pattern: {Colors.ENDC}{matches_list}{Colors.ENDC}")
    except requests.RequestException as e:
        print(f"{Colors.FAIL}Error fetching {url}: {e}{Colors.ENDC}")

if __name__ == "__main__":
    # Read URLs from standard input
    urls = [line.strip() for line in sys.stdin if line.strip()]  # Filter out empty lines

    # Use ThreadPoolExecutor to fetch URLs concurrently with a limit of 20 threads
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_url, url): url for url in urls}
        
        for future in as_completed(futures):
            url = futures[future]
            try:
                future.result()  # This will raise an exception if the thread raised one
            except Exception as e:
                print(f"{Colors.FAIL}Error processing {url}: {e}{Colors.ENDC}")
