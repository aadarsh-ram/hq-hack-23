import os
import urllib.parse as urlparse
import concurrent.futures
from requests_html import HTMLSession
import json

class SiteCurler():
    def __init__(self, incoming_query, offset):
        self.incoming_query = incoming_query
        self.offset = offset

    def curl_indeed(self):
        """
        Curls indeed.com resumes for a given query
        """
        query = urlparse.quote(self.incoming_query)

        # This token is user-specific and is obtained from the indeed.com resumes page.
        token = os.getenv("INDEED_CSRF_TOKEN", "TNy4j2yk6FPxU53dPeajS2LDdHKdu3g9")
        indeed_url = f"https://resumes.indeed.com/rpc/search?q={query}&start={self.offset}&indeedcsrftoken={token}"

        cmd = f"""curl '{indeed_url}' """ + """\
                    -H 'authority: resumes.indeed.com' \
                    -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
                    -H 'accept-language: en-US,en;q=0.9' \
                    -H 'cache-control: max-age=0' \
                    -H 'cookie: CTK=1fpupi4gonpvr800; indeed_rcc=CTK; _cfuvid=AKqDXC6iuLQW3VVq29ZNDl5OlrcIhC9OKG7fJPvRdro-1673670484741-0-604800000; SURF=3mSlNoqUFZxNDnD6HnErb8WA1u5QnGiS; CSRF=TNy4j2yk6FPxU53dPeajS2LDdHKdu3g9; gonetap=1; g_state={"i_p":1673682464422,"i_l":1}; LC=co=IN&hl=en; RF="TFTzyBUJoNoikq4ksxWsSolP9KKeKMkQbhmDZeIEWqfpXan9PwRLda6Wlg2YoWpSGTvP0rW7SX42bsZnoEbJL79Ve9yG0S9wMkF5avsYZ7MJALa28h1tBWUQsACYQLunyPMYzFac7Z3dWFF3AMfFyfpCC5tyq4JAIMILVTtDK58="; OptanonAlertBoxClosed=2023-01-14T06:31:20.828Z; SOCK="yokuHKsrfzlKiZOTfyBCqfX0-us="; SHOE="AE3EGFRZBV2RfnEltePZkRxjYWtaeyBcqIC1rNQA3avZLOBdPhow6_bxdEYJd9xuXQPpt8dvhGHoQu9NChYVwe_g1KtVyrksQZ7ymkxeLxNI9f8FTXuy22KgRiZepxCNZPRBefU0Hzep"; PCA=b07f83493a59a384; ADOC=6584093354954250; ENC_CSRF=mlG48pSLBdNgALkpn6k5VS8HHTkxzFTI; IRF=2OjkVS608cRBJyDN80nHtHDzwzzxoxWIV0Ae_fa5Cq-OutJyB0t_LQ==; INDEEDADS_HOME=c0d1269afcb1d74d|anlyts; LOCALE=en_IN; CO=IN; leftNavExpanded=false; REZEMP_TK=1gmnpsfg8kvks800; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Jan+14+2023+15%3A01%3A02+GMT%2B0530+(India+Standard+Time)&version=6.37.0&isIABGlobal=false&hosts=&consentId=a6bb86eb-dc40-45b6-af7a-d6fb7faa9331&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0%2CC0007%3A0&AwaitingReconsent=false&geolocation=%3B; PPID=eyJraWQiOiI4MWQxMmYxNC0yMzIxLTRiNWItYmJmNi0yOGU4YzBkMGFhNjQiLCJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiJlZTg2NmJjYjRlMzNjMmVjIiwiYXVkIjoiYzFhYjhmMDRmIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJjcmVhdGVkIjoxNjczNjg3NjcyMDAwLCJyZW1fbWUiOnRydWUsImlzcyI6Imh0dHBzOlwvXC9zZWN1cmUuaW5kZWVkLmNvbSIsImV4cCI6MTY3MzcwNTc2MCwiaWF0IjoxNjczNzAzOTYwLCJsb2dfdHMiOjE2NzM2ODc2NzQwODcsImVtYWlsIjoiNjAwOTlhYWRhcnNoLmdia21AZ21haWwuY29tIn0.J3sGxtBJWyFdtlWySODxWF2hk3x9e-XpUjTnNwLHKJlaXGPLg87IZYfkSGrXSPc4Lg3vwiJC7Cigwct26qajVQ; _dd_s=' \
                    -H 'sec-ch-ua: "Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"' \
                    -H 'sec-ch-ua-mobile: ?1' \
                    -H 'sec-ch-ua-platform: "Android"' \
                    -H 'sec-fetch-dest: document' \
                    -H 'sec-fetch-mode: navigate' \
                    -H 'sec-fetch-site: none' \
                    -H 'sec-fetch-user: ?1' \
                    -H 'upgrade-insecure-requests: 1' \
                    -H 'user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36' \
                    --compressed"""
        result_str = os.popen(cmd).read()
        res_json = eval(result_str.replace("null", "None").replace("false", "False").replace("true", "True"))
        return res_json["results"]

    def curl_pjf(self):
       
        """
        Curls postjobfree.com resumes for a given query
        """
        session = HTMLSession()
        result = []

        def scrape_div(div):
            link = div.find('a',first=True)
            url = "https://www.postjobfree.com" + link.attrs['href']
            try:
                next_page_response = session.get(url)
                data = next_page_response.html.find('div.normalText', first=True)
                if data:
                    return {'candidate':data.text}
                else:
                    return {'candidate':'Data not found'}
            except Exception as e:
                return {'candidate':'Error', 'error': str(e)}

        url = f'https://www.postjobfree.com/resumes?q=&l=India&radius=25&r=20&p={self.offset+1}'
        try:
            r = session.get(url)
            divs = r.html.find('div.snippetPadding')
            with concurrent.futures.ThreadPoolExecutor() as executor:
                result += list(executor.map(scrape_div, divs))
        except Exception as e:
            result.append({'candidate':'Error', 'error': str(e)})
        return json.dumps(result)
