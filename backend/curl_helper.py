import os
import urllib.parse as urlparse
import concurrent.futures
from requests_html import HTMLSession
import subprocess

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
        token = os.getenv("INDEED_CSRF_TOKEN", "0CbbOf9KlHI0L9BQni13yLZvlg7JMh8Z")
        indeed_url = f"https://resumes.indeed.com/rpc/search?q={query}&start={self.offset}&indeedcsrftoken={token}"

        cmd = f"""curl '{indeed_url}' """ + """\
            -H 'authority: resumes.indeed.com' \
            -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
            -H 'accept-language: en-US,en;q=0.9' \
            -H 'cache-control: max-age=0' \
            -H 'cookie: CTK=1fpupi4gonpvr800; indeed_rcc=CTK; g_state={"i_p":1673682464422,"i_l":1}; LC=co=IN&hl=en; RF="TFTzyBUJoNoikq4ksxWsSolP9KKeKMkQbhmDZeIEWqfpXan9PwRLda6Wlg2YoWpSGTvP0rW7SX42bsZnoEbJL79Ve9yG0S9wMkF5avsYZ7MJALa28h1tBWUQsACYQLunyPMYzFac7Z3dWFF3AMfFyfpCC5tyq4JAIMILVTtDK58="; OptanonAlertBoxClosed=2023-01-14T06:31:20.828Z; PCA=b07f83493a59a384; ADOC=6584093354954250; IRF=2OjkVS608cRBJyDN80nHtHDzwzzxoxWIV0Ae_fa5Cq-OutJyB0t_LQ==; CO=IN; leftNavExpanded=false; CSRF=3uuAtkmjoMA506z2Nyl9oSMfs660LKra; SURF=W9T6JRpxqKJZhIp9G6P4xjtH7xeaxxo6; PPEDIT=1673806662; PPID=eyJraWQiOiI4MWQxMmYxNC0yMzIxLTRiNWItYmJmNi0yOGU4YzBkMGFhNjQiLCJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJzdWIiOiJlZTg2NmJjYjRlMzNjMmVjIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBob25lX3Njb3BlIjpbXSwiYXV0aCI6Imdvb2dsZSIsImNyZWF0ZWQiOjE2NzM2ODc2NzIwMDAsImlzcyI6Imh0dHBzOlwvXC9zZWN1cmUuaW5kZWVkLmNvbSIsImxvZ190cyI6MTY3MzgwNjY2MjQ5NCwiYXVkIjoiYzFhYjhmMDRmIiwicmVtX21lIjp0cnVlLCJwaG9uZV9udW1iZXIiOiIrMTgxNDU1NjQ2ODIiLCJleHAiOjE2NzM4MDg0NjIsImlhdCI6MTY3MzgwNjY2MiwiZW1haWwiOiI2MDA5OWFhZGFyc2guZ2JrbUBnbWFpbC5jb20ifQ.CirWO2QgK2nmwLIX3Rt9x_y-sJwZxoYMwCnfQoTrZcCwec4q86bTD2IlsTP9i4sYDKZaPmyomS6XGEwAZ1MK2w; SOCK="7MWIA1EAqGneKzXTwvg3ZLA8GII="; SHOE="-VIFUU56_E95AZh_0tjSUK-h68-vtYLT_eQx4gDcPznOR0uDDXcMvIVf4vgtU9JhU1s2XzP8h-ury6Qbm3dkf8LO8kyZSu1ksNCmOY_giBmSo4_wbf2Vk3BdxrMY4SMadeSMEfgUQfZ1dPKokSvON03Z"; REZEMP_TK=1gmradtjg22ca000; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Jan+15+2023+23%3A47%3A53+GMT%2B0530+(India+Standard+Time)&version=6.37.0&isIABGlobal=false&hosts=&consentId=a6bb86eb-dc40-45b6-af7a-d6fb7faa9331&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0%2CC0007%3A0&AwaitingReconsent=false&geolocation=%3B; _dd_s=rum=1&id=f31452b2-8504-4d2c-a2ad-7fb7279ed81f&created=1673806478133&expire=1673807593969' \
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
        try:
            res_json = eval(result_str.replace("null", "None").replace("false", "False").replace("true", "True"))
        except:
            # No results
            res_json = {"results":{}}

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
        return result


    def curl_mrec(self):
        """
        Curls mightyrecruiter.com resumes for a given query
        """
        query = urlparse.quote(self.incoming_query)

        mrec_url = f"https://recruiter.mightyrecruiter.com/resumes/Get?jobID=0&page_number={self.offset+1}&page_size=20&search_on=jt&search_string={query}&location=&sortBy=score&radius=30&min_experience=0&max_experience=1200&mned=NA&min_age=0&max_age=90&hide_viewed_resume=false&hide_reviewed_resume=false&documentId=0&similarResumeSearch=false'"
        cmd = f"""curl '{mrec_url} """ + """ \
                    -H 'Accept: application/json, text/plain, */*' \
                    -H 'Accept-Language: en-US,en;q=0.9' \
                    -H 'Connection: keep-alive' \
                    -H 'Cookie: G_ENABLED_IDPS=google; mwr_fnnl_bn=f73b39fa-75cd-4330-9775-bb8e256458ba; _mwr_visitortype=true; G_AUTHUSER_H=2; JobTap=jECrVeU1nkhcixINeVx6SiZKWard4zX2MMScUiTPl5uoxeZTR-SX5VBmDqhcuaWL3-WnysaGlPdk5ls6oGlLUaNtdwQycfGUr2cSNzG5wg1d_OWKLA8f5LIZzkP0sOKYYGxumXI2Y4oQ9pPQj6dZoYe4ssSjvyB3IH48y5LQa3rm6glU7AM6nmEINIncj7xOxvDI_ATJh6MJBpc2_DkBgNyJI9ED2qzjGz0ykhdQr_5zRs8mTdrcxEmpm-JJu8eeh0nMkxHuYfmI6ukV_35DXZJ4xx8FowYgccq8F0Mh_hRxDZOszRCrM5hIkJalVlv8i5Y5NBSoOCFeQu9Ghs5Xky4QR0jOv0m--roXRCaUv_lQdwVZH_DldeqyXszae-uBYmoyImnFVBC8iMgCHk5iffB_2unnTC6_VM8YxjqgrCaJ9x10bVO9NYEwGRIY0ZMdnGozTcsVS1vHUXyJPY0FbkQ5Z2OGf7oiBrEUlF1ORbQYG5nZ5muo0k4LCeJ70V_YAPqxkQHmCOto6fc-dU89X8KHLkgvo2hPCMTVJ3W02Z7DcufkUFQvm6rjoV7xYvDqfy1zX_Of_aGsjiX5CUyzThMUvjIw7YlpALhD_9PNlcw; _mwr_trk=%7B%22requiresignin%22%3A%22False%22%2C%22userid%22%3A%22b626dbc6-2142-4876-a7a4-d0e8c6427120%22%2C%22email%22%3A%22importsolution.trinit%40gmail.com%22%2C%22firstname%22%3A%22Import%22%2C%22lastname%22%3A%22Solution%22%2C%22cname%22%3A%22gg%22%2C%22usertoken%22%3A%22FRIjHBxqTjtqXyu5WGieHRPNsGgFWzpX3emv-vhpj2aHOi68olCKMoMkzv5j8dwYHTXrLhsHj2uErYbI8O0ITlu6XqqeL1Zoo0k4sGnkxVt1aNrCMZmDCdrpdaUxyCXCULbnqr7VgXGTDy9jS2a2yQS9tK5gkVziRCcri-mx2N32gdGxWLr-9q2OwS3bswYQiPmpo_ySQqvkhl3II1uvTSjL7xgc5oCKCwEAuBUWnLfSdk4mSWD94sM_ovIPtn3pmPa-R_82t2gZ4Y_fRirHDqvfTYUmViGHklqxa41uK3edzgrX4rpc7qxUUo0dWCfS7JiUG1iBknnzrrkMHtkIujSY3CV9qDNEM2ZcQ1iNyMrhaayEJpqTXprblfoiGZjtXPPIDS4kZuB4flrtSx2ZS57d8-zFGIf02NPLA4D8fgCL6E8CAsF6yYnPo1W4UGpQTI27LWGJxR5e5CN2IphiqckVEFKwBYO_7_Skd0jnG8G0HVtoBu5SEb3k0sGoLarWnvIahPID9tlCEUl00vR82o51myKxqaBOAzymR1lUbvg2uOXNT-hMGbXssZuK2CxNFEm1L-QPN4wFIsOZ4t06QVjH-QIxuaB7cioFLANAR6JjtVzzwJxTT3Biq1lcFS6MQ6p7v3R77rw-SB75UWcnhZqpNssdJgEKOSstpx9wCZf73UkVgxkC5t1-TiSX8pQC4l0y8dV7kuamCXt8LP38Af1slEH6nJFoFictRRGc7WwRHLAJvq2_8g5mEwLIKY-SIVThXrX_7Jm0w2kv8lzn14bu-_OEOTjH-kKz0fKyg7mGt09k0fL_rsNwpbkUOg3RCkmWey_dMmt1qaQTLvYVo5mQ7cmJjvwaYpHPgH-DoztHiAExf9cRiJD-89dD9wE1_MwS1rUdfJJpvN4Q_VmLqGKBFB6t8oUvzJu2kKPHT45MjBbHkmHj8_Izk2qpOMrT%22%2C%22requiresidentify%22%3A%22false%22%2C%22requiresignup%22%3A%22False%22%2C%22ctype%22%3A%22Employer%22%2C%22cwebsite%22%3A%22null%22%2C%22mediapermission%22%3A%22TRUE%22%2C%22contactbyphonepermission%22%3A%22TRUE%22%2C%22accountstatus%22%3A%22Pending%22%2C%22planstatus%22%3A%22null%22%2C%22noofjobs%22%3A%22null%22%2C%22isfreetrial%22%3A%22false%22%2C%22trialtype%22%3A%22non%20rollover%22%2C%22iraccountid%22%3A%22105169%22%2C%22isirconversion%22%3A%22false%22%7D' \
                    -H 'Referer: https://recruiter.mightyrecruiter.com/resumes' \
                    -H 'Sec-Fetch-Dest: empty' \
                    -H 'Sec-Fetch-Mode: cors' \
                    -H 'Sec-Fetch-Site: same-origin' \
                    -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36' \
                    -H 'sec-ch-ua: "Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"' \
                    -H 'sec-ch-ua-mobile: ?1' \
                    -H 'sec-ch-ua-platform: "Android"' \
                    --compressed """
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result_str = result.stdout.decode("utf-8")
        try:
            res_json = eval(result_str.replace("null", "None").replace("false", "False").replace("true", "True"))
        except:
            # No results
            res_json = {"ResultList":{}}
        return res_json["ResultList"]

