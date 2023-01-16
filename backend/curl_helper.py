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
        token = os.getenv("INDEED_CSRF_TOKEN")
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
            -H 'Cookie: utmParams=||||; G_ENABLED_IDPS=google; _mwr_visitortype=true; G_AUTHUSER_H=2; mwr_fnnl_bn=f73b39fa-75cd-4330-9775-bb8e256458ba; _mwr_trk_m={"requiresidentify":"false","requiresignup":"true","userid":"b626dbc6-2142-4876-a7a4-d0e8c6427120","email":"importsolution.trinit@gmail.com","firstname":"Import","lastname":"Solution","cname":"gg","ctype":"Employer","cwebsite":null,"mediapermission":"TRUE","contactbyphonepermission":"TRUE","accountstatus":"Pending","planstatus":null,"noofjobs":null,"usertoken":"1rMurzCKu5NbtpH3lIcg98DoouDc_44kwY6gniGSkPcClWpTzwNiMASvuXcelwjWZJHU8S_hHyMr-O0ECOPvT5dWyn-Z5dVKHhvNqvNbWjKOiI5NHlwwUMVkNvR0pGQbkiQtoijRsmZzxz-444gMd9n-wc9OBiWjvGwEqg7H-EMpuOej7UwMcTElttTivMkZFFkJV01oNKzhJxV-o9o6BNsmsp5lmWT4vD7xpTRiukbi-zWG4prcdKjfmAGLrbAJ4aZ5XvIT0nwaQtkWpw9K2zy7E-EERr8tcUiRNu3px_lTo8uXR8pD21iNtuRMoQWMu2thHsz2Jt3CJ_Kja_madutR8InWEMjvFT0ohXHnoL5qPiBRK23_036yvz2L1dH88zcknQNYSDxX7gHW-jj7ymotN1Xy-it2NojH85KFq4fB_lDiu2Hk9MF7vspI0iHOvMboOtDFcSM7hW6h9Iy1zZIlN-oKlapcOQVoSNMN0FANbFIwdmyqCrZLgmgWdMMhgFYStZicEBy07CeqcgJIZEw9DVm6W7H6sZgMd2F1ygTYP7EneGLe4PCJyqvyqdL2edT1mN74uzQmofc3Mb2BSSGaRyIZqx6owW1VSpL9FJipx75TUE5rJ0rYaOP01dK8KjaduWHXz5fLSrM5A6OKvHyY7MHo-ff-gE9uvtLt5nyV1IsB63Gnx3QxvM3YGmLkhpxNsNI0US6kJEJsA1_NYN5E_oCbK5auwRjvfeyon7KxDiHWrQPcuNSL3fPZ687SD-Jmh5RkNxPOLrewSQMx_nIiuKBuoaj0ChOd86ZWwtQynK7AV6x4jgE758RUUcc2vzxTJCkf2HScl6oTglgeVfUBdI-dkOzLce6obkKgETO5rXzZHDE8ZjvHSlEyZftrbpwP5EbagIu_W4BQgYB9b5UvAWigpR0T3w7td1qfDtXDcLcQwVg2xlJesqZzMtHo"}; JobTap=y8M-Di2X5JwLnBFYMUAi0iPVnhZXse6Z3cjuC57A3Afn_CzJsyTZ-6uDPUrXiq3T784PobGSdE1-X09Pou-qFdyx4mJMO9aomNjSu98ma2oS-nJG42ot79HAtqsX-QeeOpJS_PVS_y7HDS6UvLFcXZEts3QfTP18fLrqTy6lhIJ9B_Mx1ML-S9IpuePfnzvcFdt2Y_R_DBai1VmgsGq-wIiEtfk-bfbKxucbPky-_164qrjkNTNgmlYpvZNA-tGgC1lt_AO4lLbw1qs-iu0YbFg5Zymwuif_Ya1UTGfjql4tstXXeMSolmSjokdtmoT5RTPiOuhayoWWH0THWALR5AbbJDDMUmkv8oJ8iYD9SCBQsBN_jlN9aD37mgDh0AAC55htXy46YiJ68bW-VZj_8zDwheDsZy8zjfFyBv8s9w0T9nLRdVdZjaUQp3KJ6Re3q3oWp795ncMwyQc5SIsrSTqsW7NTcuEKq7AIqrFGdiak91KE0vCm-i58__cs2G0DyeCBGChNVQl-pIlhv91dICGcYoTWnPyIMXLzCY_x7-gwL_q9jTGNfJ_Iq2kxDHPhyiE5ddy8Bb6o0zem88K_3zbosDJ8Pset1A0lN2eMB-yhZKMP8AoePFpLqQPAn_kZ; _mwr_trk=%7B%22requiresidentify%22%3A%22false%22%2C%22requiresignup%22%3A%22False%22%2C%22userid%22%3A%22b626dbc6-2142-4876-a7a4-d0e8c6427120%22%2C%22email%22%3A%22importsolution.trinit%40gmail.com%22%2C%22firstname%22%3A%22Import%22%2C%22lastname%22%3A%22Solution%22%2C%22cname%22%3A%22gg%22%2C%22ctype%22%3A%22Employer%22%2C%22cwebsite%22%3Anull%2C%22mediapermission%22%3A%22TRUE%22%2C%22contactbyphonepermission%22%3A%22TRUE%22%2C%22accountstatus%22%3A%22Pending%22%2C%22planstatus%22%3Anull%2C%22noofjobs%22%3Anull%2C%22usertoken%22%3A%221rMurzCKu5NbtpH3lIcg98DoouDc_44kwY6gniGSkPcClWpTzwNiMASvuXcelwjWZJHU8S_hHyMr-O0ECOPvT5dWyn-Z5dVKHhvNqvNbWjKOiI5NHlwwUMVkNvR0pGQbkiQtoijRsmZzxz-444gMd9n-wc9OBiWjvGwEqg7H-EMpuOej7UwMcTElttTivMkZFFkJV01oNKzhJxV-o9o6BNsmsp5lmWT4vD7xpTRiukbi-zWG4prcdKjfmAGLrbAJ4aZ5XvIT0nwaQtkWpw9K2zy7E-EERr8tcUiRNu3px_lTo8uXR8pD21iNtuRMoQWMu2thHsz2Jt3CJ_Kja_madutR8InWEMjvFT0ohXHnoL5qPiBRK23_036yvz2L1dH88zcknQNYSDxX7gHW-jj7ymotN1Xy-it2NojH85KFq4fB_lDiu2Hk9MF7vspI0iHOvMboOtDFcSM7hW6h9Iy1zZIlN-oKlapcOQVoSNMN0FANbFIwdmyqCrZLgmgWdMMhgFYStZicEBy07CeqcgJIZEw9DVm6W7H6sZgMd2F1ygTYP7EneGLe4PCJyqvyqdL2edT1mN74uzQmofc3Mb2BSSGaRyIZqx6owW1VSpL9FJipx75TUE5rJ0rYaOP01dK8KjaduWHXz5fLSrM5A6OKvHyY7MHo-ff-gE9uvtLt5nyV1IsB63Gnx3QxvM3YGmLkhpxNsNI0US6kJEJsA1_NYN5E_oCbK5auwRjvfeyon7KxDiHWrQPcuNSL3fPZ687SD-Jmh5RkNxPOLrewSQMx_nIiuKBuoaj0ChOd86ZWwtQynK7AV6x4jgE758RUUcc2vzxTJCkf2HScl6oTglgeVfUBdI-dkOzLce6obkKgETO5rXzZHDE8ZjvHSlEyZftrbpwP5EbagIu_W4BQgYB9b5UvAWigpR0T3w7td1qfDtXDcLcQwVg2xlJesqZzMtHo%22%2C%22isfreetrial%22%3A%22false%22%2C%22trialtype%22%3A%22non%20rollover%22%2C%22iraccountid%22%3A%22105169%22%2C%22isirconversion%22%3A%22false%22%7D' \
            -H 'Referer: https://recruiter.mightyrecruiter.com/resumes' \
            -H 'Sec-Fetch-Dest: empty' \
            -H 'Sec-Fetch-Mode: cors' \
            -H 'Sec-Fetch-Site: same-origin' \
            -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36' \
            -H 'sec-ch-ua: "Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"' \
            -H 'sec-ch-ua-mobile: ?1' \
            -H 'sec-ch-ua-platform: "Android"' \
            --compressed"""
        
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result_str = result.stdout.decode("utf-8")
        res_json = eval(result_str.replace("null", "None").replace("false", "False").replace("true", "True"))
        return res_json["ResultList"]
    
