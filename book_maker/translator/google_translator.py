import requests
import time
from termcolor import colored

from .base_translator import Base


class Google(Base):
    """
    google translate
    """

    def __init__(self, key, language, **kwargs) -> None:
        super().__init__(key, language)
        self.api_url = "https://translate.google.com/translate_a/single?client=it&dt=qca&dt=t&dt=rmt&dt=bd&dt=rms&dt=sos&dt=md&dt=gt&dt=ld&dt=ss&dt=ex&otf=2&dj=1&hl=en&ie=UTF-8&oe=UTF-8&sl=auto&tl=ja"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "GoogleTranslate/6.29.59279 (iPhone; iOS 15.4; en; iPhone14,2)",
        }
        # TODO support more models here
        self.session = requests.session()
        self.language = language
        self.retry_intervals = [60, 600, 3600]  # Retry intervals in seconds (1 min, 10 min, 1 hour)

    def rotate_key(self):
        pass

    def translate(self, text):
        print(text)
        retries = 0
        while retries < len(self.retry_intervals):
            r = self.session.post(
                self.api_url,
                headers=self.headers,
                data=f"q={requests.utils.quote(text)}",
            )
            if r.ok:
                t_text = "".join(
                    [sentence.get("trans", "") for sentence in r.json()["sentences"]],
                )
                print(colored(t_text, 'cyan'))
                return t_text
            else:
                print(colored(f'Error: {r.text}', 'red'))
                time.sleep(self.retry_intervals[retries])
                retries += 1
        return text
