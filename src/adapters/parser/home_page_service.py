import aiohttp
from bs4 import BeautifulSoup
from src.domain.exceptions import ValidationError


async def parse_home_page_service(cookies_dict: dict, url: str = "https://my.sdu.edu.kz/index.php") -> str:
    async with aiohttp.ClientSession(cookies=cookies_dict) as session:
        try:
            async with session.get(url, ssl=False) as response:
                if response.status != 200:
                    raise ValidationError("Failed to load home page")

                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                fullname_row = soup.find('td', string=lambda x: x and 'Fullname :' in x)
                if not fullname_row:
                    raise ValidationError("Could not find fullname element")

                fullname_cell = fullname_row.find_next_sibling('td')
                if not fullname_cell:
                    raise ValidationError("Could not find fullname value")

                full_name = fullname_cell.get_text(strip=True)
                if not full_name:
                    raise ValidationError("Fullname is empty")

                return full_name

        except aiohttp.ClientError as e:
            raise ValidationError(f"Connection error: {str(e)}")
        except Exception as e:
            raise ValidationError(f"Error parsing page: {str(e)}")
