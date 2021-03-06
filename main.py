import json
import sys
import time

for _ in range(3):
    try:
        from lib.logger import Logger
        from lib.utils import DriverWrapper, stylesplit, quit_with_wait
        from lib import dbm  # prevent from conflict with selenium By
        from lib.dbm import DBManager
        break
    except ImportError:
        log.warning('필요한 모듈을 찾을 수 없습니다.')
        log.info('설치하는 중..')
        import pip
        pip.main(['install', '--disable-pip-version-check', 'wheel'])
        pip.main(['install', '--disable-pip-version-check', '-r', 'requirements.txt'])
        log.success('모든 모듈을 성공적으로 설치했습니다.')
        log.info('다시 시도하는 중..')

log = Logger()
db = DBManager()

from configs.ConfigLoader import Config, Statics
config = Config(log)
static = Statics()

for _ in range(3):
    try:
        import pyperclip
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.keys import Keys
        from selenium.common.exceptions import NoSuchElementException
        from webdriver_manager.chrome import ChromeDriverManager
        break
    except ImportError:
        log.warning('필요한 모듈을 찾을 수 없습니다.')
        log.info('설치하는 중..')
        import pip
        pip.main(['install', '--disable-pip-version-check', 'wheel'])
        pip.main(['install', '--disable-pip-version-check', '-r', 'requirements.txt'])
        log.success('모든 모듈을 성공적으로 설치했습니다.')
        log.info('다시 시도하는 중..')
log.success('모듈을 성공적으로 불러왔습니다.')

entry = static.ENTRY_POINT
current_account = None

with open("localcfgs/account.cfg", "r", encoding="utf-8") as f:
    accountConfig = json.load(f)
    log.success('계정 설정을 불러왔습니다.')

with open("localcfgs/global.cfg", "r", encoding="utf-8") as f:
    globalConfig = json.load(f)
    log.success('전역 설정을 불러왔습니다.')

for account in accountConfig:
    if not account["use"]:
        continue
    current_account = account
    entry += account["method"]

if not current_account:
    log.error("계정이 설정되어 있지 않습니다. accounts.cfg 파일을 수정해 계정을 추가해 주세요.")
    quit_with_wait()

log.info(f"""계정 정보:\n
로그인 사이트:{current_account['method']}\n
계정 아이디:{current_account['account_info']['id']}\n
계정 비밀번호:{'*' * len(current_account['account_info']['password'])}""")

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver_wrapper = DriverWrapper(driver)

driver.get(entry)

match current_account['method']:
    case "facebook":
        log.info('페이스북 로그인을 시도합니다.')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        driver_wrapper.send_keys_delay(
            driver.find_element(By.ID, "email"), current_account['account_info']['id']
        )
        driver_wrapper.send_keys_delay(
            driver.find_element(By.ID, "pass"), current_account['account_info']['password']
        )
        driver.find_element(By.ID, "loginbutton").click()
    case "naver":
        log.info('네이버 로그인을 시도합니다.')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "id"))
        )
        pyperclip.copy(current_account['account_info']['id'])
        driver.find_element(By.ID, "id").send_keys(Keys.CONTROL, "v")
        pyperclip.copy(current_account['account_info']['password'])
        driver.find_element(By.ID, "pw").send_keys(Keys.CONTROL, "v")
        driver.find_element(By.ID, "log.login").click()
    case "google":
        # log.info('Using google login method.')
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.ID, "identifierId"))
        # )
        # driver.find_element(By.ID, "identifierId").send_keys(
        # current_account['account_info']['id']
        # )
        # driver.find_element(By.ID, "identifierNext").click()
        # WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.NAME, "password"))
        # )
        # driver.find_element_by_name("password").send_keys(
        # current_account['account_info']['password']
        # )
        # driver.find_element(By.ID, "passwordNext").click()
        log.error('구글 계정 로그인은 현재 지원하지 않습니다. 죄송합니다.')
        quit_with_wait()
    case "kakao":
        log.info('카카오 로그인을 시도합니다.')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_email_2"))
        )
        driver_wrapper.send_keys_delay(
            driver.find_element(By.ID, "id_email_2"), current_account['account_info']['id']
        )
        driver_wrapper.send_keys_delay(
            driver.find_element(By.ID, "id_password_3"), current_account['account_info']['password']
        )
        driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()
    case "twitter":
        log.info('트위터 로그인을 시도합니다.')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username_or_email"))
        )
        driver_wrapper.send_keys_delay(
            driver.find_element(By.ID, "username_or_email"), current_account['account_info']['id']
        )
        driver_wrapper.send_keys_delay(
            driver.find_element(By.ID, "password"), current_account['account_info']['password']
        )
        driver.find_element(By.ID, "allow").click()
log.success('로그인 성공.')

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "kkuko"))
)
driver.get(f"{static.GAME_MAIN_ENTRY_POINT}{globalConfig['game']['server']}")

def wait_loop():
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, static.OUTGAME_USERNAME_CSS_SELECTOR))
    )
    username = ""
    while True:
        username = driver.find_elements(By.CSS_SELECTOR, static.OUTGAME_USERNAME_CSS_SELECTOR)[0].text
        if not username:
            continue
        log.info(f'유저 닉네임: {username}')
        break

    while True:
        if stylesplit(driver.find_element(By.ID, "GameBox").get_attribute('style'))['display'] == 'none':
            log.info('게임 대기중..')
            time.sleep(1)
            continue
        game_loop(username=username)

def game_loop(**kwargs):
    username = kwargs['username']
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, static.INGAME_USER_CSS_NAME))
    )
    inputbox = driver.find_element(By.CSS_SELECTOR, static.GAME_CHAT_CSS_SELECTOR)
    history = []
    while True:
        try:
            current_turn_user = driver.find_element(By.CLASS_NAME, static.INGAME_USER_CURRENT_CSS_NAME)
        except NoSuchElementException:
            continue
        turn_username = current_turn_user.find_element(By.CLASS_NAME, static.INGAME_USERNAME_CSS_NAME).text
        if turn_username == username:
            current_fchar = driver.find_element(By.CLASS_NAME, static.GAME_WORD_DISPLAY_CSS_NAME).text
            if len(current_fchar) != 1:
                continue
            try:
                recomm_word = db.get_word(dbm.By.HIGH_LENGTH, current_fchar, history)[0]
            except IndexError:
                log.warning('단어를 찾지 못했습니다.')
                log.warning('한방단어 혹은 단어를 모두 사용했을 수 있습니다.')
                time.sleep(1)
                continue
            driver_wrapper.send_keys_delay(inputbox, 
                                           recomm_word, 
                                           random=config.get('typing.delay_random'),
                                           delay_min=config.get('typing.delay_min'),
                                           delay_max=config.get('typing.delay_max')
            )
            if stylesplit(driver.find_element(By.ID, "GameBox").get_attribute('style'))['display'] != 'none':
                inputbox.send_keys(Keys.ENTER)
        else:
            pass
        try:
            first_history = driver.find_element(By.CLASS_NAME, static.INGAME_HISTORY_ITEM_CSS_NAME).get_attribute('innerHTML')
        except NoSuchElementException:
            continue
        first_history = first_history.replace('\t', '').replace('\n', '').replace(' ', '').replace('"', '')
        history_text = first_history[:first_history.find('<')]
        if history_text not in history:
            history.append(history_text)
            db.insert_word(history_text)

# ***************** #
wait_loop()
