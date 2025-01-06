import aiohttp
from src.domain.exceptions import ValidationError


async def login_and_save_cookies(username: str, password: str, url: str = "https://my.sdu.edu.kz/"):
    base_url = url.rstrip('/')
    login_url = f"{base_url}/loginAuth.php"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as resp:
            if resp.status != 200:
                raise ValidationError("Failed to load login page")

        form_data = {
            'username': username,
            'password': password,
            'modstring': '',
            'LogIn': ' Log in '
        }

        async with session.post(login_url, data=form_data, ssl=False) as resp:
            if resp.status != 200:
                raise ValidationError("Вход не выполнен - проверьте учетные данные")

            cookie_jar = session.cookie_jar.filter_cookies(url)
            cookies_dict = {cookie.key: cookie.value for cookie in cookie_jar.values()}
            if cookies_dict.get("uname") is None:
                raise ValidationError("Вход не выполнен - проверьте учетные данные")
            return cookies_dict
