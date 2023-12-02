import requests
import os
import re

def download_from_krakenfiles(url, output_directory="."):
    """Download a file from KrakenFiles given its URL."""

    def _get_file_details(url):
        """Fetch the file details like token and server prefix from the URL page."""
        headers_for_page = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Referer": "https://krakenfiles.com/"
        }
        page_response = requests.get(url, headers=headers_for_page)
        content = page_response.text

        token_pattern = re.compile(r'name="token" value="(.*?)"')
        server_pattern = re.compile(r'form action="//(.*?).krakenfiles.com')

        token = token_pattern.search(content).group(1)
        server_prefix = server_pattern.search(content).group(1)

        return token, server_prefix

    def _get_download_link(url, token, server_prefix):
        """Fetch the actual download link using the token and server prefix."""
        file_id = url.split("/")[-2]
        api_url = f"https://{server_prefix}.krakenfiles.com/download/{file_id}"

        headers_for_api = {
            "Host": f"{server_prefix}.krakenfiles.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://krakenfiles.com",
            "Connection": "keep-alive",
            "Referer": "https://krakenfiles.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "DNT": "1",
            "Sec-GPC": "1",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers"
        }

        response = requests.post(api_url, headers=headers_for_api, data=f"token={token}")
        if response.status_code == 200 and response.json().get("status") == "ok":
            return response.json().get("url")
        else:
            raise ValueError("Failed to get download link. Check the provided URL.")

    token, server_prefix = _get_file_details(url)
    download_link = _get_download_link(url, token, server_prefix)

    headers_for_download = {
        "Host": f"{server_prefix}download.krakenfiles.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://krakenfiles.com/",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-User": "?1",
        "DNT": "1",
        "Sec-GPC": "1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }

    file_response = requests.get(download_link, headers=headers_for_download, stream=True)

    cd = file_response.headers.get('content-disposition')
    filename = cd.split("filename=")[-1].strip("\"") if cd else url.split("/")[-2] + ".unknown"
    filepath = os.path.join(output_directory, filename)

    with open(filepath, 'wb') as f:
        for chunk in file_response.iter_content(chunk_size=8192):
            f.write(chunk)

    return filepath
