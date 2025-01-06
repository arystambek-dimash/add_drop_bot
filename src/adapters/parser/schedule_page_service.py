import aiohttp
from bs4 import BeautifulSoup
from src.domain.exceptions import ValidationError


async def parse_schedule_page_service(
        cookies_dict: dict,
        year: int,
        term: int,
        base_url: str = "https://my.sdu.edu.kz/?mod=schedule",
) -> dict:
    schedule_url = f"{base_url}?mod=schedule&ajx=1&action=showSchedule&year={year}&term={term}&type=I"

    async with aiohttp.ClientSession(cookies=cookies_dict) as session:
        try:
            async with session.get(schedule_url, ssl=False) as response:
                if response.status != 200:
                    raise ValidationError("Failed to load schedule page")

                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                result = {
                    "year_term": f"{year} - term {term}",
                    "schedule": []
                    # ...
                }
                # ...
                return result

        except aiohttp.ClientError as e:
            raise ValidationError(f"Connection error: {str(e)}")
        except Exception as e:
            raise ValidationError(f"Error parsing schedule page: {str(e)}")
