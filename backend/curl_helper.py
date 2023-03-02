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
                    -H 'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7' \
                    -H 'Connection: keep-alive' \
                    -H 'Cookie: optimizelyEndUserId=oeu1673665295434r0.06641821869420994; ajs_anonymous_id=%22fba4497d-38a5-4afe-875f-9d25cf1620ac%22; G_ENABLED_IDPS=google; fpestid=6hVBBnhueKxFXVqFSDGqT7ECk6Ixn2GTCsQFoZnSYO5K0HTpz4Irt96-6FAz6C3TMgHcwg; mp_0568fc1726576866d45cfa17ad4837b9_mixpanel=%7B%22distinct_id%22%3A%20%22185ae39be9e946-01adb3e79a949f-26021151-144000-185ae39be9f147a%22%2C%22%24device_id%22%3A%20%22185ae39be9e946-01adb3e79a949f-26021151-144000-185ae39be9f147a%22%2C%22mp_lib%22%3A%20%22Segment%3A%20web%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Frecruitcrm.io%2F%22%2C%22%24initial_referring_domain%22%3A%20%22recruitcrm.io%22%2C%22%24search_engine%22%3A%20%22google%22%7D; utmParams=||||; _gid=GA1.2.680123674.1677774869; __insp_wid=473465058; __insp_nv=true; __insp_targlpu=aHR0cHM6Ly93d3cubWlnaHR5cmVjcnVpdGVyLmNvbS8%3D; __insp_targlpt=SG9tZXBhZ2UgfCBNaWdodHlSZWNydWl0ZXI%3D; __insp_norec_sess=true; _ga=GA1.2.794228522.1673665297; mwr_fnnl_bn=a77bd31a-aac0-4752-a2f2-0057bea0cafb; _ga_H9YPXGDPVB=GS1.1.1677774868.3.1.1677774895.33.0.0; _mwr_trk_m={"requiresidentify":"false","requiresignup":"true","userid":"65fbe9c2-a58b-4635-987a-e67f341c004b","email":"darkhunterhere@gmail.com","firstname":"Devil","lastname":"Hunter","cname":"team","ctype":"Employer","cwebsite":"team.com","mediapermission":"TRUE","contactbyphonepermission":"FALSE","accountstatus":"Pending","planstatus":null,"noofjobs":null,"usertoken":"zxR3uWCC2069Aa4auM4nQSVkGyFCY4U34FrpBzprA2s4D8LeClyE2c3YNXXBuLbo6ZZj6IFNEvftj7slUF_HyiEAzemRMFD6ScSZjOI3MkFsV9j4ONtuahF3u-EjFGj1ON8xUPWBMSF-_Rb5cIkjXbG40Lp0x2CK1sLLmP0L-51qfAckermmIjGASTcq4tsve_O1Ywk7nHJXNt3N2-9T2MuO-lMf07qXvqH5PLNvP4Je_IgmW1h-qQ_qv1wymiTV-YALV2W5ueoJdu-0gH7ARqLr4A7QdbF3Mjc7nF4AiJX-OD_uKCHebbINVDYvqjz-5e5Q_DUIUulKaErcgrA64CIH_bBjVb0EvkMfPZ8eOD5wdJ8cgXmgzQlQu8dMwiO-iPCnrOqI-4uvHZjPIPfj3LgkxC0xrMh19erpCOE9TFnGWwKBJm8Y2-4B2YfWoIpbiuadpHnFiJ8cleTW67QpHiSRGfotRcsDo5oVj--5_fKKV6sBCqTK1hcQjC8pCEthR9mxrRuyViFtDMapK9N5JTkz-ZuPAUdeepPc5CmHIl_BgZ9vzakN9n4tm2DiAgl_H7R-QTpgFYpspzc83Fuwh2VmEOkdH3l1M2cHn8xUwr71KuVHBbsFZU0qLBbfvOHjmeLOu8CHLZvHJXqb2HRQrwb3oniQqvwqiY7FKoR1PcNWDCZRHtl20KHAw4TS9cVmpuwnCtnIdL1ItTBWJd8t43KptZG8qsH-OY3YKphSTLwIAzEoi-C_XLCe7Yq_xnihl8pSj_ZG1oCBM50HkeP-r-qUAlAbwXaFZEjDrj-GStZQA1ZseqD-cyxcqwzYEwRueZRBecT7cZieJyAYaxhXREKBDfUkJ_fN-Z-94OJAjlXaeWJIRcgdWwShFcCWrLKY6vxTO1sPKri-qvmgX729GkAViGBv_vRJdI_fF2GKrKTp0xZmizIw8999zf_96_ZL"}; JobTap=fWfQyKZg7C-yqjfvMyrmNeCHJM7dU8wU4waganGzTdsVu_vimqbr3aMtWxfSDQ2-FF4yjt9Lgx0QPYcrJ8IHEhqrI_Xm5c4ANGaScRojh32VrBMoS9a8kyMvaz97IRPnMZ7l_bBW_hwG_2vli3c_VGiHklbJr-pjaW7YJw7g0jYMc39DGxE9f-VjbiowKqPtT4XmYdBlj0uSnX6rYUDbwU0SELdd2S4Dmzmq5eZqz0YTIgFQqVp7r576l-ZgrrJJMjLWd_Z8v-zJj53VVUjP8yJfR6PIkHn3YYdhc99fFw_w3L_CuSV-_fJf0AWKW6cOhv9Up0OIrGm9PGR5pqWEppl0wpprVz2FV1DwbPoEDXUKzKSVFvUbo98vt3An-v6fn8hSZIURorm5HigDDf7iFDZBiGLx5DFZI8DzDqLSJz2UjCGlIAhjyQbSnmAHXGr9K2UwVonK-t-TJanAeH5OpgjDMNTFfBtoL1zMOJTOtiHp13KyKRtgv0mwUx2ZlnrzXiMeIsSAF-Rtf5fEucaI2DSLicos-thCgBcJpZ27SY2QYAaMlUyDEetVfOJBBTxsw4xG6jmeGgsqHKGpHB37T-XVYjVN0fo3XGvv0uKWO8xjykHPIsVPuQ7Qp9w3jrCm; _mwr_visitortype=true; ajs_user_id=%2265fbe9c2-a58b-4635-987a-e67f341c004b%22; __ssid=fedabf91918a7f614be18b08455a47c; IR_gbd=mightyrecruiter.com; IR_5168=1677775009508%7C0%7C1677775009508%7C%7C; _mwr_trk=%7B%22requiresidentify%22%3A%22false%22%2C%22requiresignup%22%3A%22False%22%2C%22userid%22%3A%2265fbe9c2-a58b-4635-987a-e67f341c004b%22%2C%22email%22%3A%22darkhunterhere%40gmail.com%22%2C%22firstname%22%3A%22Devil%22%2C%22lastname%22%3A%22Hunter%22%2C%22cname%22%3A%22team%22%2C%22ctype%22%3A%22Employer%22%2C%22cwebsite%22%3A%22team.com%22%2C%22mediapermission%22%3A%22TRUE%22%2C%22contactbyphonepermission%22%3A%22FALSE%22%2C%22accountstatus%22%3A%22Pending%22%2C%22planstatus%22%3Anull%2C%22noofjobs%22%3Anull%2C%22usertoken%22%3A%22zxR3uWCC2069Aa4auM4nQSVkGyFCY4U34FrpBzprA2s4D8LeClyE2c3YNXXBuLbo6ZZj6IFNEvftj7slUF_HyiEAzemRMFD6ScSZjOI3MkFsV9j4ONtuahF3u-EjFGj1ON8xUPWBMSF-_Rb5cIkjXbG40Lp0x2CK1sLLmP0L-51qfAckermmIjGASTcq4tsve_O1Ywk7nHJXNt3N2-9T2MuO-lMf07qXvqH5PLNvP4Je_IgmW1h-qQ_qv1wymiTV-YALV2W5ueoJdu-0gH7ARqLr4A7QdbF3Mjc7nF4AiJX-OD_uKCHebbINVDYvqjz-5e5Q_DUIUulKaErcgrA64CIH_bBjVb0EvkMfPZ8eOD5wdJ8cgXmgzQlQu8dMwiO-iPCnrOqI-4uvHZjPIPfj3LgkxC0xrMh19erpCOE9TFnGWwKBJm8Y2-4B2YfWoIpbiuadpHnFiJ8cleTW67QpHiSRGfotRcsDo5oVj--5_fKKV6sBCqTK1hcQjC8pCEthR9mxrRuyViFtDMapK9N5JTkz-ZuPAUdeepPc5CmHIl_BgZ9vzakN9n4tm2DiAgl_H7R-QTpgFYpspzc83Fuwh2VmEOkdH3l1M2cHn8xUwr71KuVHBbsFZU0qLBbfvOHjmeLOu8CHLZvHJXqb2HRQrwb3oniQqvwqiY7FKoR1PcNWDCZRHtl20KHAw4TS9cVmpuwnCtnIdL1ItTBWJd8t43KptZG8qsH-OY3YKphSTLwIAzEoi-C_XLCe7Yq_xnihl8pSj_ZG1oCBM50HkeP-r-qUAlAbwXaFZEjDrj-GStZQA1ZseqD-cyxcqwzYEwRueZRBecT7cZieJyAYaxhXREKBDfUkJ_fN-Z-94OJAjlXaeWJIRcgdWwShFcCWrLKY6vxTO1sPKri-qvmgX729GkAViGBv_vRJdI_fF2GKrKTp0xZmizIw8999zf_96_ZL%22%2C%22isfreetrial%22%3A%22false%22%2C%22trialtype%22%3A%22non%20rollover%22%2C%22iraccountid%22%3A%22106043%22%2C%22isirconversion%22%3A%22false%22%7D; IR_PI=7368b9b3-b918-11ed-98bc-4b84c6173b47%7C1677861409508; _uetsid=1a3dbeb0b91811ed92244f8d454581ff; _uetvid=c347eb1093b711ed892b8730f944bcb9; __insp_slim=1677775025849' \
                    -H 'Referer: https://recruiter.mightyrecruiter.com/resumes' \
                    -H 'Sec-Fetch-Dest: empty' \
                    -H 'Sec-Fetch-Mode: cors' \
                    -H 'Sec-Fetch-Site: same-origin' \
                    -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36' \
                    -H 'sec-ch-ua: "Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"' \
                    -H 'sec-ch-ua-mobile: ?0' \
                    -H 'sec-ch-ua-platform: "Windows"' \
                    --compressed  """
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result_str = result.stdout.decode("utf-8")
        try:
            res_json = eval(result_str.replace("null", "None").replace("false", "False").replace("true", "True"))
        except:
            # No results
            res_json = {"ResultList":{}}
        return res_json["ResultList"]

