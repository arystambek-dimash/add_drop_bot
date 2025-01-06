import aiohttp
from bs4 import BeautifulSoup

from src.domain.exceptions import ValidationError


async def parse_year_terms_service(cookies_dict: dict, url: str="https://my.sdu.edu.kz/index.php?mod=schedule") -> list:
    async with aiohttp.ClientSession(cookies=cookies_dict) as session:
        try:
            async with session.get(url, ssl=False) as response:
                if response.status != 200:
                    raise ValidationError(f"Failed to load page for year-term list, status={response.status}")

                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                select_el = soup.find("select", id="ysem")
                if not select_el:
                    raise ValidationError("Could not find select#ysem on the page")

                options = select_el.find_all("option")

                result = []
                for opt in options:
                    val = opt.get("value", "").strip()
                    label = opt.get_text(strip=True)

                    if val == "1#1" or "Select" in label:
                        continue
                    if "#" not in val:
                        continue

                    year_str, term_str = val.split("#", maxsplit=1)
                    try:
                        year = int(year_str)
                        term = int(term_str)
                    except:
                        continue

                    result.append({
                        "year": year,
                        "term": term,
                        "label": label
                    })

                if not result:
                    raise ValidationError("No valid year-term options found.")

                return result

        except aiohttp.ClientError as e:
            raise ValidationError(f"Connection error: {str(e)}")
        except Exception as e:
            raise ValidationError(f"Error parsing year-term options: {str(e)}")
