    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-ssl-errors=true")
    options.add_argument("--ignore-certificate-errors")    
    
    options.binary_location="C:/Projects/quotesscraper/chromedriver.exe"
    driver = webdriver.Chrome('C:/PATH_TO/chromedriver_win32/chromedriver.exe',options=options)