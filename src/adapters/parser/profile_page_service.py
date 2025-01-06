import aiohttp
from bs4 import BeautifulSoup

from src.domain.exceptions import ValidationError


async def parse_profile_page(cookies_dict: dict, url: str = "https://my.sdu.edu.kz/index.php?mod=profile") -> str:
    async with aiohttp.ClientSession(cookies=cookies_dict) as session:
        try:
            async with session.get(url, ssl=False) as response:
                if response.status != 200:
                    raise ValidationError("Failed to load profile page")

                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                profile_data = extract_profile_data(soup)
                return format_profile_data(profile_data)

        except aiohttp.ClientError as e:
            raise ValidationError(f"Connection error: {str(e)}")
        except Exception as e:
            raise ValidationError(f"Error parsing page: {str(e)}")


def extract_profile_data(soup: BeautifulSoup) -> dict:
    data = {}
    table = soup.find("table", class_="clsTbl")
    if not table:
        return data
    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) == 2:
            key = cols[0].get_text(strip=True).rstrip(":")
            value = cols[1].get_text(strip=True)
            data[key] = value

    return data


def format_profile_data(data: dict) -> str:
    lines = []
    for key, value in data.items():
        lines.append(f"<b>{key}:</b> {value}")
    formatted_text = "\n".join(lines)
    return formatted_text
