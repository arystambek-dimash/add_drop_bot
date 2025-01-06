import aiohttp
from bs4 import BeautifulSoup
from src.domain.exceptions import ValidationError


async def parse_transcript_service(cookies_dict: dict, url: str="https://my.sdu.edu.kz/?mod=transkript") -> list:
    async with aiohttp.ClientSession(cookies=cookies_dict) as session:
        try:
            async with session.get(url, ssl=False) as response:
                if response.status != 200:
                    raise ValidationError(f"Failed to load transcript page. Status {response.status}")

                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                transcript_data = []
                current_semester = None
                courses_for_semester = []
                semester_footer = {}

                all_rows = soup.find_all("tr")
                for row in all_rows:
                    semester_header_td = row.find("td", attrs={"colspan": "8"})
                    if semester_header_td:
                        if current_semester and courses_for_semester:
                            transcript_data.append({
                                "semester_name": current_semester,
                                "courses": courses_for_semester,
                                "footer": semester_footer
                            })
                            courses_for_semester = []
                            semester_footer = {}

                        current_semester = semester_header_td.get_text(strip=True)
                        continue

                    if "color:Maroon" in row.get("style", ""):
                        tds = row.find_all("td")
                        if len(tds) >= 8:
                            semester_footer = {
                                "credits_semester": tds[2].get_text(strip=True),
                                "ects_semester": tds[3].get_text(strip=True),
                                "SA": tds[4].get_text(strip=True).replace("SA : ", ""),
                                "GA": tds[5].get_text(strip=True).replace("GA : ", ""),
                                "SPA": tds[6].get_text(strip=True).replace("SPA : ", ""),
                                "GPA": tds[7].get_text(strip=True).replace("GPA : ", "")
                            }
                        continue

                    tds = row.find_all("td")
                    if len(tds) == 8:
                        code = tds[0].get_text(strip=True)
                        title = tds[1].get_text(strip=True)
                        credit = tds[2].get_text(strip=True)
                        ects = tds[3].get_text(strip=True)
                        numeric_grade = tds[4].get_text(strip=True)
                        letter_grade = tds[5].get_text(strip=True)
                        point = tds[6].get_text(strip=True)
                        traditional = tds[7].get_text(strip=True)
                        if code:
                            courses_for_semester.append({
                                "course_code": code,
                                "course_title": title,
                                "credit": credit,
                                "ects": ects,
                                "numeric_grade": numeric_grade,
                                "letter_grade": letter_grade,
                                "point": point,
                                "traditional": traditional
                            })

                if current_semester and courses_for_semester:
                    transcript_data.append({
                        "semester_name": current_semester,
                        "courses": courses_for_semester,
                        "footer": semester_footer
                    })

                if not transcript_data:
                    raise ValidationError("No transcript data found")

                return transcript_data

        except aiohttp.ClientError as e:
            raise ValidationError(f"Connection error: {str(e)}")
        except Exception as e:
            raise ValidationError(f"Error parsing transcript: {str(e)}")
