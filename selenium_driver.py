from proxy_interface import *
from selenium_stealth import stealth
# import undetected_chromedriver as uc

class selenium_with_proxy():
    def __init__(self):

        self.helper = Helper()
        self.driver_initialized = False
        self.driver = ''

        self.use_proxy = True

        if self.use_proxy:
            self.proxy_filename = 'data.json'
            self.pluginfile = 'proxy_auth_plugin.zip'

        self.proxy_handle = CWEBSHARE()

    def proxy_json_data(self):

        if not self.helper.is_file_exist(self.proxy_filename):
            self.proxy_handle.get_proxy_list(self.proxy_filename)

        proxy_date = self.helper.read_json_file(self.proxy_filename)['date']
        current_date = self.helper.get_time_stamp().split()[0]
        
        if proxy_date != current_date:
            self.proxy_handle.get_proxy_list(self.proxy_filename)

        all_proxies = self.helper.read_json_file(self.proxy_filename)['proxies']

        us_proxies = [proxy for proxy in all_proxies if proxy.get("country_code") == "US"]

        # while 1:
        #     random_index = random.randint(0,len(all_proxies)-1)
        #     current_proxy = all_proxies[random_index]
        #     if current_proxy['valid']:
        #         break

        while 1:
            random_index = random.randint(0,len(us_proxies)-1)
            current_proxy = us_proxies[random_index]
            if current_proxy['valid']:
                break

        # ylyncxyw  :  zweu7p3c0xln  :  154.92.112.235  :  5256
        PROXY_USER = current_proxy['username']
        PROXY_PASS = current_proxy['password']
        PROXY_HOST = current_proxy['proxy_address']
        PROXY_PORT = current_proxy['ports']['socks5']

        print(f'{PROXY_USER}:{PROXY_PASS}:{PROXY_HOST}:{PROXY_PORT}')

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
            ],
            "background": {
            "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
            var config = {
                mode: "fixed_servers",
                rules: {
                    singleProxy: {
                        scheme: "http",
                        host: "%s",
                        port: parseInt(%s)
                    },
                    bypassList: ["localhost"]
                }
            };

            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

                    function callbackFn(details) {
                    return {
                    authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {urls: ["<all_urls>"]},
        ['blocking']
        );
        """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

        with zipfile.ZipFile(self.pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

    def get_driver(self):
        opts = webdriver.ChromeOptions()
        # opts = uc.ChromeOptions()
        # opts['headless'] = None
        # opts.add_argument('--headless')

        if self.use_proxy:
            print("Adding Chrome extension for proxy")
            self.proxy_json_data()
            opts.add_extension(self.pluginfile)
        
        self.driver = webdriver.Chrome(options=opts)
        # self.driver = uc.Chrome(options=opts)
        stealth(self.driver, 
                user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
            )
        
        self.driver_initialized = True
        # input()
        return self.driver

    def close_driver(self):
        if self.driver_initialized:
            self.driver.quit()
            self.driver_initialized = False

    
    def main(self):
        driver = self.get_driver()
        driver.get('https://www.google.com/maps/')
        time.sleep(10)


if __name__ == "__main__":
    selenium_proxy = selenium_with_proxy()
    selenium_proxy.proxy_json_data()