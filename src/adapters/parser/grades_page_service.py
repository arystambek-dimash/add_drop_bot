import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict

from src.domain.exceptions import ValidationError


async def parse_grades_page_service(cookies_dict: dict, term: str) -> List[Dict]:
    base_url = "https://my.sdu.edu.kz/index.php?mod=grades"
    async with aiohttp.ClientSession(cookies=cookies_dict) as session:
        try:
            async with session.get(base_url, ssl=False) as response:
                if response.status != 200:
                    raise ValidationError(f"Failed to load transcript page. Status {response.status}")

                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                grades_data = []
                for course_table in soup.find_all("table", id="coursesTable"):
                    th_text = course_table.find("td", class_="thtext")
                    if not th_text:
                        continue

                    semester_grades = []
                    for tr in course_table.find_all("tr", class_="csrow"):
                        td = tr.find_all("td", class_="crtd")
                        if len(td) < 7:
                            continue

                        course_data = {
                            "code": td[0].text.strip(),
                            "course_name": td[1].text.strip(),
                            "credits": td[2].text.strip(),
                            "ects": td[3].text.strip(),
                            "absence": td[4].text.strip(),
                            "total": td[5].text.strip(),
                            "letter_grade": td[6].text.strip(),
                        }
                        semester_grades.append(course_data)

                    if semester_grades:
                        grades_data.append({
                            "semester": th_text.get_text(strip=True),
                            "grades": semester_grades,
                        })
                return grades_data

        except aiohttp.ClientError as e:
            raise ValidationError(f"Connection error: {str(e)}")
        except Exception as e:
            raise ValidationError(f"Error parsing transcript: {str(e)}")


asyncio.run(parse_grades_page_service({"PHPSESSID": "fvo5vcm2eqii4gqqv5iiag3udo", "uname": "210107073"}))
