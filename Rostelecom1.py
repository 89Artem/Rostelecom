from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class TestAuthorizationPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()  # Убедитесь, что ChromeDriver установлен и доступен
        self.driver.get("https://b2c.passport.rt.ru")  # URL страницы авторизации

    def tearDown(self):
        self.driver.quit()

    def wait_for_element(self, by, value):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, value)))

    def test_successful_login(self):
        driver = self.driver
        self.wait_for_element(By.NAME, "username").send_keys("корректный_логин")  # Заменить на свой логин
        self.wait_for_element(By.NAME, "password").send_keys("корректный_пароль")  # Заменить на свой пароль
        self.wait_for_element(By.XPATH, "//button[contains(text(), 'Войти')]").click()  # Кнопка "Войти"

        # Ожидание загрузки страницы после входа
        WebDriverWait(driver, 10).until(EC.title_contains("Личный кабинет"))
        self.assertIn("Личный кабинет", driver.title)  # Заголовок главной страницы после входа

    def test_incorrect_password(self):
        driver = self.driver
        self.wait_for_element(By.NAME, "username").send_keys("корректный_логин")
        self.wait_for_element(By.NAME, "password").send_keys("неверный_пароль")
        self.wait_for_element(By.XPATH, "//button[contains(text(), 'Войти')]").click()

        # Ожидание появления сообщения об ошибке
        error_message = self.wait_for_element(By.XPATH,
                                              "//div[contains(@class, 'alert') and contains(text(), 'Неверный пароль')]").text
        self.assertEqual(error_message, "Неверный пароль")  # Проверить сообщение об ошибке

    def test_empty_username(self):
        driver = self.driver
        self.wait_for_element(By.NAME, "password").send_keys("корректный_пароль")
        self.wait_for_element(By.XPATH, "//button[contains(text(), 'Войти')]").click()

        # Ожидание появления сообщения об ошибке
        error_message = self.wait_for_element(By.XPATH,
                                              "//div[contains(@class, 'alert') and contains(text(), 'Введите логин')]").text
        self.assertEqual(error_message, "Введите логин")  #Проверить сообщение об ошибке

    def test_empty_password(self):
        driver = self.driver
        self.wait_for_element(By.NAME, "username").send_keys("корректный_логин")
        self.wait_for_element(By.XPATH, "//button[contains(text(), 'Войти')]").click()

        # Ожидание появления сообщения об ошибке
        error_message = self.wait_for_element(By.XPATH,
                                              "//div[contains(@class, 'alert') and contains(text(), 'Введите пароль')]").text
        self.assertEqual(error_message, "Введите пароль")  # Проверьте сообщение об ошибке

    def test_remember_me(self):
        driver = self.driver
        self.wait_for_element(By.NAME, "username").send_keys("корректный_логин")
        self.wait_for_element(By.NAME, "password").send_keys("корректный_пароль")
        self.wait_for_element(By.XPATH, "//input[@type='checkbox']").click()  # Чекбокс "Запомнить меня"
        self.wait_for_element(By.XPATH, "//button[contains(text(), 'Войти')]").click()

        # Ожидание загрузки страницы после входа
        WebDriverWait(driver, 10).until(EC.title_contains("Личный кабинет"))

        # Повторное открытие страницы для проверки автозаполнения
        driver.get("https://b2c.passport.rt.ru")

        username_field = self.wait_for_element(By.NAME, "username")

        self.assertEqual(username_field.get_attribute('value'), "корректный_логин")  # Проверка автозаполнения

    def test_forgot_password_functionality(self):
        driver = self.driver
        self.wait_for_element(By.LINK_TEXT, "Забыли пароль?").click()  # Кнопка "Забыли пароль?"

        # Ожидание загрузки формы восстановления пароля
        WebDriverWait(driver, 10).until(EC.title_contains("Восстановление пароля"))
        self.assertIn("Восстановление пароля", driver.title)  # Заголовок формы восстановления пароля

    def test_terms_of_service_link(self):
        driver = self.driver
        self.wait_for_element(By.LINK_TEXT,
                              "Пользовательское соглашение").click()  # Ссылка на пользовательское соглашение
        WebDriverWait(driver, 10).until(
            EC.title_contains("Условия использования"))  # Ожидание загрузки страницы соглашения
        self.assertIn("Условия использования", driver.title)  # Проверить заголовок страницы соглашения
        driver.back()  # Вернуться на страницу авторизации

    def test_registration_link(self):
        driver = self.driver
        self.wait_for_element(By.LINK_TEXT, "Нет аккаунта? Зарегистрироваться").click()  # Ссылка на регистрацию
        WebDriverWait(driver, 10).until(EC.title_contains("Регистрация"))  # Ожидание загрузки страницы регистрации
        self.assertIn("Регистрация", driver.title)  # Проверить заголовок страницы регистрации
        driver.back()  # Вернуться на страницу авторизации

    def test_phone_format_validation(self):
        driver = self.driver
        self.wait_for_element(By.NAME, "username").send_keys(
            "некорректный_номер_телефона")  # Ввести некорректный номер телефона
        self.wait_for_element(By.XPATH, "//button[contains(text(), 'Войти')]").click()  # Кнопка "Войти"

        # Ожидание появления сообщения об ошибке
        error_message = self.wait_for_element(By.XPATH,
                                              "//div[contains(@class, 'alert') and contains(text(), 'Некорректный формат телефона')]").text
        self.assertEqual(error_message, "Некорректный формат телефона")  # Проверить сообщение об ошибке

    def test_multiple_incorrect_logins(self):
        driver = self.driver

        for _ in range(3):  # Повторяем попытку входа несколько раз с некорректными данными
            self.wait_for_element(By.NAME, "username").send_keys("некорректный_email")
            self.wait_for_element(By.NAME, "password").send_keys("некорректный_пароль")
            self.wait_for_element(By.XPATH, "//button[contains(text(), 'Войти')]").click()

            # Ожидание появления сообщения об ошибке
            error_message = self.wait_for_element(By.XPATH,
                                                  "//div[contains(@class, 'alert') and contains(text(), 'Неверный логин или пароль')]").text
            self.assertEqual(error_message, "Неверный логин или пароль")  # Проверить сообщение об ошибке

            # Очистка полей ввода для следующей попытки
            username_field = self.wait_for_element(By.NAME, "username")
            password_field = self.wait_for_element(By.NAME, "password")
            username_field.clear()
            password_field.clear()

    def test_captcha_entry(self):
        driver = self.driver

        # Ввод некорректных данных для активации CAPTCHA
        for _ in range(3):  # Повторяем попытку входа несколько раз с некорректными данными
            self.wait_for_element(By.NAME, "username").send_keys("некорректный_email")
            self.wait_for_element(By.NAME, "password").send_keys("некорректный_пароль")
            self.wait_for_element(By.XPATH, "//button[contains(text(), 'Войти')]").click()

            # Ожидание появления CAPTCHA
            captcha_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "captcha")))
            if captcha_input.is_displayed():
                break  # CAPTCHA появилась

    def test_captcha_refresh(self):
        driver = self.driver

        # Ввод некорректных данных для активации CAPTCHA
        for _ in range(3):  # Повторяем попытку входа несколько раз с некорректными данными
            self.wait_for_element(By.NAME, "username").send_keys("некорректный_email")
            self.wait_for_element(By.NAME, "password").send_keys("некорректный_пароль")
            self.wait_for_element(By.XPATH, "//button[contains(text(), 'Войти')]").click()

            # Ожидание появления CAPTCHA и кнопки обновления
            captcha_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "captcha")))
            refresh_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(@class,'refresh-captcha')]")))

        for _ in range(5):  # Нажимаем на кнопку обновления CAPTCHA несколько раз
            refresh_button.click()
            WebDriverWait(driver, 2).until(EC.staleness_of(captcha_input))  # Ждем обновления CAPTCHA
            captcha_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "captcha")))  # Получаем новый элемент CAPTCHA

        if __name__ == "__main__":
            unittest.main()

    def test_email_format_validation(self):
        driver = self.driver
        self.wait_for_element(By.NAME, "username").send_keys("некорректный_email")  # Ввод некорректного email
        self.wait_for_element(By.NAME, "password").send_keys(
            "корректный_пароль")  # Можно оставить пароль корректным
        self.wait_for_element(By.XPATH, "//button[contains(text(), 'Войти')]").click()

        # Ожидание появления сообщения об ошибке
        error_message = self.wait_for_element(By.XPATH,
                                                      "//div[contains(@class, 'alert') and contains(text(), 'Некорректный формат электронной почты')]").text
        self.assertEqual(error_message,
                        "Некорректный формат электронной почты")  # Проверить сообщение об ошибке

    def test_displaying_errors(self):
        driver = self.driver
        self.wait_for_element(By.NAME, "username").send_keys("некорректный_email")
        self.wait_for_element(By.NAME, "password").send_keys("некорректный_пароль")
        self.wait_for_element(By.XPATH, "//button[contains(text(), 'Войти')]").click()

        # Ожидание появления списка ошибок
        error_list = self.wait_for_element(By.XPATH,
                                                   "//div[contains(@class, 'error-list')]")  # Предполагается, что ошибки отображаются в этом элементе
        error_items = error_list.find_elements(By.TAG_NAME,
                                                       "li")  # Предполагается, что ошибки отображаются в виде списка <li>

        self.assertGreater(len(error_items), 0)  # Проверка, что ошибки отображаются

    def test_support_service_accessibility(self):
        driver = self.driver
        support_info = self.wait_for_element(By.XPATH,
                                                "//div[contains(text(), 'Служба поддержки')]")  # Предполагается наличие элемента с информацией о поддержке
        support_phone = support_info.find_element(By.XPATH,
                                                          ".//span[contains(@class, 'support-phone')]").text  # Предполагается наличие элемента с номером телефона
        support_email = support_info.find_element(By.XPATH,
                                                          ".//span[contains(@class, 'support-email')]").text  # Предполагается наличие элемента с email

        self.assertTrue(support_phone)  # Проверка наличия номера телефона
        self.assertTrue(support_email)  # Проверка наличия email

    def test_cookies_info_display(self):
        driver = self.driver
        cookies_info = self.wait_for_element(By.XPATH,
                                                "//div[contains(text(), 'Cookies')]")  # Предполагается наличие элемента с информацией о Cookies
        cookies_text = cookies_info.text

        self.assertIn("согласие", cookies_text)  # Проверка наличия текста о согласии с использованием Cookies

    def test_age_restriction_display(self):
        driver = self.driver
        age_restriction_info = self.wait_for_element(By.XPATH,
                                                "//div[contains(text(), '18+')]")  # Предполагается наличие элемента с информацией о возрастном ограничении

        self.assertTrue(age_restriction_info.is_displayed())  # Проверка отображения информации о возрасте

        if __name__ == "__main__":
            unittest.main()

    def test_email_format_validation(self):
        driver = self.driver
        self.wait_for_element(By.NAME, "username").send_keys("некорректный_email")  # Ввод некорректного email
        self.wait_for_element(By.NAME, "password").send_keys("корректный_пароль")  # Можно оставить пароль корректным
        self.wait_for_element(By.XPATH, "//button[contains(text(), 'Войти')]").click()

        # Ожидание появления сообщения об ошибке
        error_message = self.wait_for_element(By.XPATH,
                                              "//div[contains(@class, 'alert') and contains(text(), 'Некорректный формат электронной почты')]").text
        self.assertEqual(error_message, "Некорректный формат электронной почты")  # Проверить сообщение об ошибке

    def test_displaying_errors(self):
        driver = self.driver
        self.wait_for_element(By.NAME, "username").send_keys("некорректный_email")
        self.wait_for_element(By.NAME, "password").send_keys("некорректный_пароль")
        self.wait_for_element(By.XPATH,"//button[contains(text(), 'Войти')]").click()

        # Ожидание появления списка ошибок
        error_list = self.wait_for_element(By.XPATH,
                                        "//div[contains(@class, 'error-list')]")  # Предполагается, что ошибки отображаются в этом элементе
        error_items = error_list.find_elements(By.TAG_NAME,
                                        "li")  # Предполагается, что ошибки отображаются в виде списка <li>

        self.assertGreater(len(error_items), 0)  # Проверка, что ошибки отображаются

    def test_support_service_accessibility(self):
        driver = self.driver
        support_info = self.wait_for_element(By.XPATH,
                                        "//div[contains(text(), 'Служба поддержки')]")  # Предполагается наличие элемента с информацией о поддержке
        support_phone = support_info.find_element(By.XPATH,
                                            ".//span[contains(@class, 'support-phone')]").text  # Предполагается наличие элемента с номером телефона
        support_email = support_info.find_element(By.XPATH,
                                            ".//span[contains(@class, 'support-email')]").text  # Предполагается наличие элемента с email

        self.assertTrue(support_phone)  # Проверка наличия номера телефона
        self.assertTrue(support_email)  # Проверка наличия email

    def test_cookies_info_display(self):
        driver = self.driver
        cookies_info = self.wait_for_element(By.XPATH,
                                        "//div[contains(text(), 'Cookies')]")  # Предполагается наличие элемента с информацией о Cookies
        cookies_text = cookies_info.text

        self.assertIn("согласие", cookies_text)  # Проверка наличия текста о согласии с использованием Cookies

    def test_age_restriction_display(self):
        driver = self.driver
        age_restriction_info = self.wait_for_element(By.XPATH,
                                        "//div[contains(text(), '18+')]")  # Предполагается наличие элемента с информацией о возрастном ограничении

        self.assertTrue(age_restriction_info.is_displayed())  # Проверка отображения информации о возрасте

    def test_email_format_validation(self):
        driver = self.driver
        self.wait_for_element(By.NAME, "username").send_keys("некорректный_email")  # Ввод некорректного email
        self.wait_for_element(By.NAME, "password").send_keys("корректный_пароль")  # Можно оставить пароль корректным
        self.wait_for_element(By.XPATH, "//button[contains(text(), 'Войти')]").click()

        # Ожидание появления сообщения об ошибке
        error_message = self.wait_for_element(By.XPATH,
                                              "//div[contains(@class, 'alert') and contains(text(), 'Некорректный формат электронной почты')]").text
        self.assertEqual(error_message, "Некорректный формат электронной почты")  # Проверьте сообщение об ошибке


    def test_displaying_errors(self):
        driver = self.driver
        self.wait_for_element(By.NAME, "username").send_keys("некорректный_email")
        self.wait_for_element(By.NAME, "password").send_keys("некорректный_пароль")
        self.wait_for_element(By.XPATH,"//button[contains(text(), 'Войти')]").click()

        # Ожидание появления списка ошибок
        error_list = self.wait_for_element(By.XPATH,
                                        "//div[contains(@class, 'error-list')]")  # Предполагается, что ошибки отображаются в этом элементе
        error_items = error_list.find_elements(By.TAG_NAME,
                                            "li")  # Предполагается, что ошибки отображаются в виде списка <li>

        self.assertGreater(len(error_items), 0)  # Проверка, что ошибки отображаются


    def test_support_service_accessibility(self):
        driver = self.driver
        support_info = self.wait_for_element(By.XPATH,
                                             "//div[contains(text(), 'Служба поддержки')]")  # Предполагается наличие элемента с информацией о поддержке
        support_phone = support_info.find_element(By.XPATH,
                                                  ".//span[contains(@class, 'support-phone')]").text  # Предполагается наличие элемента с номером телефона
        support_email = support_info.find_element(By.XPATH,
                                                  ".//span[contains(@class, 'support-email')]").text  # Предполагается наличие элемента с email

        self.assertTrue(support_phone)  # Проверка наличия номера телефона
        self.assertTrue(support_email)  # Проверка наличия email


    def test_cookies_info_display(self):
        driver = self.driver
        cookies_info = self.wait_for_element(By.XPATH,
                                             "//div[contains(text(), 'Cookies')]")  # Предполагается наличие элемента с информацией о Cookies
        cookies_text = cookies_info.text

        self.assertIn("согласие", cookies_text)  # Проверка наличия текста о согласии с использованием Cookies


    def test_age_restriction_display(self):
        driver = self.driver
        age_restriction_info = self.wait_for_element(By.XPATH,
                                            "//div[contains(text(), '18+')]")  # Предполагается наличие элемента с информацией о возрастном ограничении

        self.assertTrue(age_restriction_info.is_displayed())  # Проверка отображения информации о возрасте

if __name__ == "__main__":
    unittest.main()