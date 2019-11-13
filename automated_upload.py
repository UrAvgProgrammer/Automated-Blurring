#coding=utf-8
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image as pi
from PIL import ImageFilter

def test_fullpage_screenshot():
    chrome_path = r"D:\Work\Selenium Scraper\chromedriver\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.headless = True
    # options.add_argument('--start-maximized')
    driver = webdriver.Chrome(chrome_path, chrome_options=options)
    i = 0
    urls = ["https://so-compa.com/finding-your-new-appliances-in-the-market/", "https://stressaffect.com/smart-appliances-that-you-can-buy-to-make-your-life-easier/"]
    for url in urls:
        driver.get(url)
        time.sleep(2)
        #the element with longest height on page
        all_link = driver.find_elements_by_xpath("//a[@href]")
        for sub_link in all_link:
            if '5best.com' in sub_link.get_attribute("href"):
                original_size = driver.get_window_size()
                required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
                required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
                driver.set_window_size(required_width, required_height)

                location = sub_link.location
                size = sub_link.size

                #print(location['x'])
                #print(size['height'])
                print('starting..')

                # driver.save_screenshot(path)  # has scrollbar
                driver.find_element_by_tag_name('body').screenshot('test{}.png'.format(i))  # avoids scrollbar
                driver.set_window_size(original_size['width'], original_size['height'])

                img = pi.open('test{}.png'.format(i))
                temp = img.copy()
                temp = temp.crop((location['x'], location['y'], (location['x'] + size['width']), (location['y'] + size['height'])))
                new_size = img.size
                img = img.filter(ImageFilter.BLUR)
                img = img.filter(ImageFilter.BLUR)
                img.paste(temp, (location['x'], location['y']))
                img.save("image" + str(i) + ".png", "PNG", quality=80, optimize=True, progressive=True)
                print('saving extracted image')
        i += 1        
    driver.quit()
if __name__ == "__main__":
    test_fullpage_screenshot()