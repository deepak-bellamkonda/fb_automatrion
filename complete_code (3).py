import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException
import openai
import facebook
from selenium.webdriver.chrome.options import Options
import requests
from openai import OpenAI
from monsterapi import client
import schedule
import threading
from datetime import datetime, timedelta
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import pytz 
from datetime import datetime, timezone
import os
import tempfile
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
import chromedriver_autoinstaller


import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def install_chrome():
    os.system('sbase install chromebrowser')
    os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/browsers/chromebrowser /home/appuser/venv/bin/chromebrowser')

# Install Chrome browser
_ = install_chrome()

# Set up Chrome options
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-notifications')

# Create a Chrome webdriver instance
browser = webdriver.Chrome(options=chrome_options)

#def installff():
#  os.system('sbase install geckobrowser')
#
# os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/browsers/geckobrowser /home/appuser/venv/bin/geckobrowser')

#_ = installff()
#from selenium import webdriver
#from selenium.webdriver import FirefoxOptions
#opts = FirefoxOptions()
#opts = ChromeOptions()


#opts.add_argument("--headless")
#opts.add_argument('--disable-notifications')
#browser = webdriver.Firefox(options=opts)
#browser= webdriver.Chrome(options=opts)


OPENAI_API_KEY = "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"

# Global variable to store the browser instance

@st.cache_resource
def get_browser():
    global browser
    return browser

@st.cache_data
def validate_user_credentials(username, password):
    # Replace this with your validation logic
    return username == "Skepitglobal" and password == "Skepitglobal"


@st.cache_data
def content_generator(restuarant_name, location, nature_of_cuisine, occasion, offer):
    prompt = f"You are a prompt engineering assistant. Create a Facebook post for resturant {restuarant_name} at location {location} and my nature of cuisine is {nature_of_cuisine} for the {occasion} occasion and we are giving flat {offer} discount  and add relevant tags. Generate content without user involvement and limit to 50 words"
    #Generate content for the Facebook post using GPT-3.5 Turbo
    clientopenai = OpenAI(api_key=OPENAI_API_KEY)
    response = clientopenai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a prompt engineering assistant."},
                {"role": "user", "content": prompt},
            ]
        )
            #content=response['choices'][0]['message']['content']
    content= response.choices[0].message.content
    return content
    #modified_content=st.text_area("Generated Facebook Post Content", content)
    
@st.cache_data
def image_generator(other_keywords):
    api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjBhOTBhZWVhZWRjYjk5ZGVjNWE4YzgyOGNiNDZjZDQwIiwiY3JlYXRlZF9hdCI6IjIwMjMtMTItMjVUMTY6MTg6MDQuNTczNDMyIn0.8Ku0_-xJ0a7Ug79HvzsecIG_iakmH2VXdZzC7c0SE8o'  # Your API key here
    monster_client = client(api_key)
    model = 'sdxl-base'
    #prompt = input_text
    input_data = {
        'prompt': other_keywords,
        'negprompt': 'unreal, fake, meme, joke, disfigured, poor quality, bad, ugly, text, letters, numbers, humans',
        'samples': 2,
        'steps': 50,
        'aspect_ratio': 'square',
        'guidance_scale': 7.5,
        'seed': 2414,
        }
    result = monster_client.generate(model, input_data)

    image_urls = result['output']
    #image_urls = ["https://www.simplilearn.com/ice9/free_resources_article_thumb/Coca_Cola_Marketing_Strategy_2022.jpg"]
    return image_urls

@st.cache_data
def save_uploaded_file(uploaded_file):
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    return file_path


    
def login_to_facebook(App_name,restuarant_name,location,nature_of_cuisine,occasion,offer,other_keywords):
    global browser

    #facebook content generation
    st.subheader("Facebook Post Content Generation")
    content=content_generator(restuarant_name,location,nature_of_cuisine,occasion,offer)
    modified_content=st.text_area("Generated Facebook Post Content",content)


    #image generation
    image_urls= image_generator(other_keywords)


    # Display all images with buttons
    for i, image_url in enumerate(image_urls):
        st.image(image_url, caption=f'Image {i + 1}', use_column_width=True, width=200)
    selected_image_index = st.text_input("Enter the image you want to choose (e.g., 1)",key="selected image")
    #upload image
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    selected_profile = None  # Assign a default value

    if st.toggle("Post to Facebook"):
        if selected_image_index:
            st.write("Posting images")
            if 1 <= int(selected_image_index) <= len(image_urls):
                st.session_state.selected_image_index = int(selected_image_index) - 1
                st.session_state.selected_image_url = image_urls[int(selected_image_index) - 1]
                image_path= image_urls[int(selected_image_index) - 1]
                st.text(f"Selected Image {selected_image_index}")  
                
                
                facebook_username = st.text_input("Enter your Facebook username")
                facebook_password = st.text_input("Enter your Facebook password", type="password")
                if st.checkbox("Login to facebook"):
                    username=facebook_username
                    password=facebook_password
                    if facebook_username and facebook_password:
                        st.info("Logging in to Facebook...")
                        #login_to_facebook(App_name,restuarant_name,location,nature_of_cuisine,occasion,offer,other_keywords)
                        page_id,permanant_access_token = app_creation(username, password, App_name)
                                #image_path = 'image.jpeg'
                        access_token = permanant_access_token  # Your Facebook access token here
                                #page_id = '179897971873271'  # Your Facebook page ID here
                        message = str(modified_content)

                        if st.checkbox("Schedule Post" ):
                            image_url = image_path
                            image_response = requests.get(image_url)
                           # graph = facebook.GraphAPI(access_token)
                            print(page_id)

                            # Check if the request was successful (status code 200)
                            if image_response.status_code == 200:
                            # Open the image file in binary mode
                                with open('local_image.png', 'wb') as file:
                                    # Write the content of the response to the file
                                    file.write(image_response.content)
                            #image_path = 'local_image.png'
                            image_path = image_response.content
                            
                            caption = modified_content
                        
                            
                            

                            # Replace with your User Access Token, Page ID, and desired API version
                            user_access_token = permanant_access_token
                            

                            api_version = "v13.0"

                            # Make a request to get the Page Access Token
                            url = f"https://graph.facebook.com/{api_version}/{page_id}?fields=access_token&access_token={user_access_token}"
                            response = requests.get(url)
                            data = response.json()

                            # Extract the Page Access Token
                            page_access_token = data.get("access_token")

                            print(f"Page Access Token: {page_access_token}")
                            

                            # Step 2: Display heading as Scheduling posts
                            st.header("Scheduling posts on Facebook")

                            # Step 3: Ask for Access token and Page ID
                            #access_token = st.text_input("Enter Facebook Access Token:")
                            #page_id = st.text_input("Enter Facebook Page ID:")

                            # Step 4: Ask for image (file uploader)
                            #uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

                            # Step 5: Ask for content
                            message = modified_content

                            # Step 6 & 7: Ask for date and time to schedule
                            scheduled_date = st.date_input("Select date:")
                            scheduled_time = st.time_input("Select time:")

                            # Combine date and time to create a datetime object
                            scheduled_datetime = datetime.combine(scheduled_date, scheduled_time)

                            # Step 8: Display all timezones in a dropdown
                            timezones = pytz.all_timezones
                            selected_timezone = st.selectbox("Select timezone:", timezones)

                            # Step 9: Store the selected timezone
                            st.write(f"Selected Timezone: {selected_timezone}")

                            # Step 9 & 10: Post the Facebook post according to the date, time, and timezone
                            if st.button("Schedule Post"):
                                if  message and scheduled_datetime:
                                    try:
                                        # Save the uploaded file and get the file path
                                        #image_path = save_uploaded_file(uploaded_file)
                                        post_to_facebook_demo_schedule_imageurl(access_token, page_id, message, image_path, scheduled_datetime, selected_timezone)
                                        st.success("Post scheduled successfully!")
                                    except Exception as e:
                                        st.error(f"Error scheduling post: {e}")
                                else:
                                    st.warning("Please fill in all the required fields.")


                        
                                # Set default values for scheduled date and time
                                
                                #st.success("Post scheduled. You can close this window, and the post will be posted at the scheduled time.")

                        if st.checkbox("Post Now"):
                            post_to_facebook_demo(access_token, page_id, message, image_path)
                            st.success("Post published successfully.")
                        # Button to close the browser
                            if st.button("Close Browser"):
                                close_browser()
                    else:
                        st.warning("Please enter both Facebook username and password.")
            else:
                st.warning(f"Invalid image index. Please enter a number between 1 and {len(image_urls)}.")
        if uploaded_file:
            facebook_username = st.text_input("Enter your Facebook username")
            facebook_password = st.text_input("Enter your Facebook password", type="password")
            image_path = save_uploaded_file(uploaded_file)
            if st.checkbox("Login to facebook"):
                username=facebook_username
                password=facebook_password
                if facebook_username and facebook_password:
                    st.info("Logging in to Facebook...")
                    #login_to_facebook(App_name,restuarant_name,location,nature_of_cuisine,occasion,offer,other_keywords)
                    page_id,permanant_access_token = app_creation(username, password, App_name)
                            #image_path = 'image.jpeg'
                    access_token = permanant_access_token  # Your Facebook access token here
                                #page_id = '179897971873271'  # Your Facebook page ID here
                    message = str(modified_content)

                    if st.checkbox("Schedule Post" ):
                        #image_url = image_path
                        #image_response = requests.get(image_url)
                        graph = facebook.GraphAPI(access_token)
                        print(page_id)

                        # Check if the request was successful (status code 200)
                        #if image_response.status_code == 200:
                        # Open the image file in binary mode
                        #    with open('local_image.png', 'wb') as file:
                        #        # Write the content of the response to the file
                        #        file.write(image_response.content)
                        #image_path = 'local_image.png'
                        caption = modified_content
                        
                            
                            

                            # Replace with your User Access Token, Page ID, and desired API version
                        user_access_token = permanant_access_token
                            

                        api_version = "v13.0"

                            # Make a request to get the Page Access Token
                        url = f"https://graph.facebook.com/{api_version}/{page_id}?fields=access_token&access_token={user_access_token}"
                        response = requests.get(url)
                        data = response.json()

                            # Extract the Page Access Token
                        page_access_token = data.get("access_token")

                        print(f"Page Access Token: {page_access_token}")
                        

                        st.header("Scheduling posts on Facebook")
                        #uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

                        message = modified_content

                        scheduled_date = st.date_input("Select date:")
                        scheduled_time = st.time_input("Select time:")

                            # Combine date and time to create a datetime object
                        scheduled_datetime = datetime.combine(scheduled_date, scheduled_time)

                            # Step 8: Display all timezones in a dropdown
                        timezones = pytz.all_timezones
                        selected_timezone = st.selectbox("Select timezone:", timezones)

                            # Step 9: Store the selected timezone
                        st.write(f"Selected Timezone: {selected_timezone}")

                            # Step 9 & 10: Post the Facebook post according to the date, time, and timezone
                        if st.button("Schedule Post"):
                            if uploaded_file and message and scheduled_datetime:
                                try:
                                    # Save the uploaded file and get the file path
                                    image_path = save_uploaded_file(uploaded_file)
                                    post_to_facebook_demo_schedule_file_upload(access_token, page_id, message, image_path, scheduled_datetime, selected_timezone)
                                    st.success("Post scheduled successfully!")
                                except Exception as e:
                                    st.error(f"Error scheduling post: {e}")
                            else:
                                st.warning("Please fill in all the required fields.")


                        
                                # Set default values for scheduled date and time
                                
                                #st.success("Post scheduled. You can close this window, and the post will be posted at the scheduled time.")

                    if st.checkbox("Post Now"):
                        post_to_facebook_demo_file_upload(access_token, page_id, message, image_path)
                        st.success("Post published successfully.")
                    # Button to close the browser
                        if st.button("Close Browser"):
                            close_browser()
                else:
                    st.warning("Please enter both Facebook username and password.")
                    
    return browser, selected_profile

@st.cache_data
def app_creation(username, password, App_name):
#facebook login
    selected_profile = None  # Assign a default value
 #facebook login
    

    # Working with the 'add_argument' Method to modify Driver Default Notification

    browser.get("http://www.facebook.com")

    username_elem = browser.find_element(By.ID, "email")
    password_elem = browser.find_element(By.ID, "pass")
    button = browser.find_element(By.CSS_SELECTOR, 'button[data-testid="royal_login_button"]')
    browser.maximize_window()
    username_elem.send_keys(username)
    password_elem.send_keys(password)
    button.click()
    time.sleep(4)  # Waiting for the page to load
 
 
 


# facebook login
    outer_profile_element = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".x14yjl9h.xudhj91.x18nykt9.xww2gxu.x10l6tqk.xhtitgo"))
    )
    outer_profile_element.click()
    time.sleep(4)
    inner_profile_element = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x1ypdohk.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1o1ewxj.x3x9cwd.x1e5q0jg.x13rtm0m.x87ps6o.x1lku1pv.x1a2a7pz.x9f619.x3nfvp2.xdt5ytf.xl56j7k.x1n2onr6.xh8yej3'))
    )
    inner_profile_element.click()
    time.sleep(4)
    profile_containers = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.x1i10hfl.x1qjc9v5.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x87ps6o.x1lku1pv.x1a2a7pz.x1lq5wgf.xgqcy7u.x30kzoy.x9jhf4c.x1lliihq[role="radio"]'))
    )
    st.write("Profiles and Business pages")
    profile_names = []
    for container in profile_containers:
        profile_name = container.find_element(By.CSS_SELECTOR, '.x1yc453h').text
        profile_names.append(profile_name)
    selected_profile = st.selectbox("Select a profile", profile_names)
    for container in profile_containers:
        profile_name = container.find_element(By.CSS_SELECTOR, '.x1yc453h').text
        if profile_name == selected_profile:
            container.click()
            time.sleep(3)
            time.sleep(4)
            business_page_name = selected_profile
            business_page_element = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, f'//span[text()="{business_page_name}"]'))
            )
            business_page_element.click()
            time.sleep(4)
        
        
            about_element = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//span[text()="About"]'))
                )
            about_element.click()
            page_transparency_element = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//span[text()="Page transparency"]'))
            )
            page_transparency_element.click()
            time.sleep(8)
            xpath = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/span'
            page_id_element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            page_id = page_id_element.text
            print("Page ID:", page_id)
            time.sleep(4)
            st.write(f"Retrieved Page ID: {page_id}")
            st.success(f"Clicked on {selected_profile}")
            time.sleep(4)
            browser.get("https://business.facebook.com/login/?next=https%3A%2F%2Fdevelopers.facebook.com%2F%3Fbiz_login_source%3Dbizweb_unified_login_fb_login_button")
            browser.maximize_window() 
            element_to_click = browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div[2]/div/div[2]/ul/li[5]/a/div[1]")

     
            element_to_click.click()
            #time.sleep(4)
            create_newapp = browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[2]/div/div/div/div/div/div[1]/div[3]/div[2]/div/div")
     
        # Click the element
            create_newapp.click()
            #time.sleep(4)
            usecase_button = browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[2]/div/div/div/div/div[3]/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[4]/div/div/div/div/div")
              # Click the element
            usecase_button.click()
            #time.sleep(4)
     
     
            #click next button
            next_button = browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[2]/div/div/div/div/div[3]/div/div[2]/div/div/div/div[2]/div/div/div")
            next_button.click()
            #time.sleep(4)
     
            #select app type
            apptype_button = browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[2]/div/div/div/div/div[3]/div/div[2]/div/div/div/div/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div")
            apptype_button.click()
            #time.sleep(4)
     
            #close notification
            notification_button = browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[3]/div/div/div/div/form/div/div/button")
            notification_button.click()
            time.sleep(4)
     
            #next button
            next_button = browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[2]/div/div/div/div/div[3]/div/div[2]/div/div/div/div/div[1]/div[2]/div/div[3]/div/div")
            next_button.click()
            time.sleep(4)
     
            #type app name
            appname=browser.find_element("xpath", "/html/body/div[1]/div[5]/div[2]/div/div/div/div/div[3]/div/div[2]/div/div/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div/div/div[1]/div[2]/div[1]/div/input")
            appname.send_keys(App_name)
     
            #create app button
            create_app_button = browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[2]/div/div/div/div/div[3]/div/div[2]/div/div/div/div/div[1]/div[2]/div/div[4]/div[2]/div[2]/div")
            create_app_button.click()
            time.sleep(10)
    
            #app_event = browser.find_element(By.CSS_SELECTOR, 'a._271k._271m._1qjd._1gwm[href*="/async/products/add/?product_route=analytics"]')
            #app_event.click()
            #time.sleep(6)
     
     
            #link_element = browser.find_element(By.CSS_SELECTOR, 'a.x1i10hfl')
     
            # Click the link
            #link_element.click()
            #time.sleep(4)
     
            #instagram
            #instagram_graph_api_button =  browser.find_element(By.CSS_SELECTOR, 'a._271k._271m._1qjd._1gwm[href*="/async/products/add/?product_route=instagram"]')
     
            #instagram_graph_api_button.click()
            #time.sleep(3)
            #back to product page
            #link_element = browser.find_element(By.CSS_SELECTOR, 'a.x1i10hfl')


            #link_element.click()

            #whatsapp button
            #button_whatsapp = browser.find_element(By.CSS_SELECTOR, 'a._271k._271m._1qjd._1gwm[href*="/async/products/add/?product_route=whatsapp-business"]')
            #button_whatsapp.click()
            #time.sleep(4)

            #back to product page
            #link_element = browser.find_element(By.CSS_SELECTOR, 'a.x1i10hfl')

            #link_element.click()
            #time.sleep(4)
            #business login
            #button_business_login = browser.find_element(By.CSS_SELECTOR, 'a._271k._271m._1qjd._1gwm[href*="/async/products/add/?product_route=business-login"]')
            #button_business_login.click()
            #time.sleep(4)

            #back to product page
            #link_element = browser.find_element(By.CSS_SELECTOR, 'a.x1i10hfl')
            #link_element.click()

            #tools
            tools_button= browser.find_element(By.XPATH, "/html/body/div[1]/div[5]/div[1]/div/div[1]/div/div/div/div/div/div[2]/a[2]")
            tools_button.click()
            time.sleep(4)

            #graph api explorer
            graph_api_button = browser.find_element(By.XPATH, '/html/body/div[1]/div[5]/div[2]/div/div/div[2]/div[1]/div[1]')
            graph_api_button.click()

 

            # Wait for the menu to be present
            button_xpath = '//*[@id="facebook"]/body/div[1]/div[5]/div[2]/div/div[2]/span/div/div[2]/div/div[5]/div[5]/div/div/div/div/div/div[5]/div/button'
            button_element = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
            )   
            button_element.click()
            time.sleep(6)



            item_xpath = f'//div[contains(., "{App_name}")]/span[@class="_5xzx"]'

            item_element = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, item_xpath))
            )
            time.sleep(2)
 
            item_element.click()
            time.sleep(6)


            #permissions button
            permissions = browser.find_element(By.XPATH, '/html/body/div[1]/div[5]/div[2]/div/div[2]/span/div/div[2]/div/div[5]/div[5]/div/div/div/div/div/div[9]/div[4]')
            permissions.click()


                    
 
 
            # Wait for the menu items to be present
            menu_items = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.uiContextualLayer ul[role="menu"] li a[role="menuitem"]')))
            time.sleep(6)

            # Click on each permissions ans sub permissions
            for item in menu_items:
                item.click()
            time.sleep(6)

            elements = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "_2wpb._3v8w"))
            )

            # Click on each element
            for element in elements:
                element.click()
            permissions.click()


            time.sleep(4)
            #scroll up teh window
            element = browser.find_element(By.XPATH,'/html/body/div[1]/div[5]/div[2]/div/div[2]/span/div/div[2]/div/div[5]/div[5]')
            # Scroll the element into view
            browser.execute_script("window.scrollTo(0, -document.body.scrollHeight);")


            original_window_handle = browser.current_window_handle



            #clicking the generate button
            generate_token_button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="facebook"]/body/div[1]/div[5]/div[2]/div/div[2]/span/div/div[2]/div/div[5]/div[5]/div/div/div/div/div/div[2]/div/button'))
            )

            # Click on the element
            generate_token_button.click() 

            #storing the state of teh original window


            #window_after = browser.window_handles[1]
            #browser.switch_to.window(window_after)


            new_window_handle = WebDriverWait(browser, 10).until(EC.number_of_windows_to_be(2))

            # Switch to the new window
            all_window_handles = browser.window_handles
            new_window_handle = [handle for handle in all_window_handles if handle != browser.current_window_handle][0]
            browser.switch_to.window(new_window_handle)

            button0 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/form/div/div[3]/div/div[1]")))
            button0.click()
            time.sleep(4)
         
            button1 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[2]")))
            button1.click()   
            time.sleep(4)

            button2 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[3]/div/label/div/div/div[1]/div")))
            button2.click()
            time.sleep(4)

            button3 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div[2]/div")))
            button3.click()
            time.sleep(4)

            button4 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[3]/div/label/div/div/div[1]/div")))
            button4.click()
            time.sleep(4)

            button5 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div[2]/div")))
            button5.click()
            time.sleep(4)

            button6 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[3]/div/div/div[2]/div[2]/div")))
            button6.click()
            time.sleep(4)

            button7 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[3]/div/label/div/div/div[1]/div")))
            button7.click()
            time.sleep(4)

            button8 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div[2]/div")))
            button8.click()
            time.sleep(4)
         
            button9 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div[2]/div")))
            button9.click()
            time.sleep(4)
         
            button10 = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/form/div/div/div/div/div/div[2]/div/div[2]/div/div/div[2]/div/div")))
            button10.click()
            time.sleep(4)

            browser.switch_to.window(original_window_handle)
            print("original window")


            access_token = browser.find_element(By.XPATH,"/html/body/div[1]/div[5]/div[2]/div/div[2]/span/div/div[2]/div/div[5]/div[5]/div/div/div/div/div/div[2]/div/div/div[1]/label/input")
            #access token
            value = access_token.get_attribute("value")
            #value="EAAMmI4VaensBOZBD2LUwZBMotBsjJdaXoX2ySW15NdU9jaReCR6yf7OXaaab4C2UlPhHWhc8kLbzZA1evA5wzuBWFNwpds3WZBdwRbUTCBfwfJyYOAv1ZBhVVPEMSZCUgYLZAMKvrsU8RqJg67xPfwCeCAylWSNVUiabJxbEZA5LHuI6vIJhKGOTvodZApZB2UYwVfhwO0tXTkliS73QBnaZBj39Om8ICTszsJQZBDkZD"
         
         
            #fetching app scoped id
            app_scoped_user_id=""
     

         
             # Construct the URL for the /me endpoint
            url = "https://graph.facebook.com/v12.0/me"

             # Prepare parameters
            params = {
                "access_token": str(value)
            }

            try:
             # Make the request using the requests library
                response = requests.get(url, params=params)
                response.raise_for_status()  # Raise an HTTPError for bad responses

                # Parse the JSON response
                data = response.json()

                 # Check for errors
                if "id" in data:
                    app_scoped_user_id = data["id"]
                #return app_scoped_user_id
                else:
                    print("Error: User ID not found in the response.")
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")

         
            # Replace this with a valid user access token

             # Get the App-Scoped User ID
            print(app_scoped_user_id)
            permanant_access_token =""
            url = f"https://graph.facebook.com/v12.0/{app_scoped_user_id}/accounts"

             # Prepare parameters
            params = {
                    "access_token": value
                }

            try:
                    # Make the GET request using the requests library
                response = requests.get(url, params=params)
                response.raise_for_status()  # Raise an HTTPError for bad responses

                 # Parse the JSON response
                data = response.json()

                    # Check for errors
                if "data" in data and data["data"]:
                    permanant_access_token = data["data"][0]["access_token"]
                    print(data["data"][0]["access_token"])
                else:
                    print("No accounts found for the given user.")
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")

  


            st.write(f"Retrieved Access token0 : {permanant_access_token}")
         
            pageid = page_id
            access_token = permanant_access_token
        
        
    

    
            return page_id, access_token
def post_to_facebook_demo_schedule_file_upload(access_token, page_id, message, image_path, scheduled_datetime, selected_timezone):
    graph = facebook.GraphAPI(access_token)

    # Convert scheduled_datetime to the selected timezone
    scheduled_datetime = pytz.timezone(selected_timezone).localize(scheduled_datetime)

    # Convert scheduled_datetime to Unix timestamp (number)
    scheduled_timestamp = int(scheduled_datetime.timestamp())

    # Schedule the post
    
    graph.put_photo(parent_object=page_id, image=open(image_path, 'rb'), message=message, published=False, scheduled_publish_time=scheduled_timestamp)
    
    
    
                                    
@st.cache_data
def post_to_facebook_demo_schedule_image_url(access_token, page_id, message, image_path, scheduled_datetime, selected_timezone):
    graph = facebook.GraphAPI(access_token)

    # Convert scheduled_datetime to the selected timezone
    scheduled_datetime = pytz.timezone(selected_timezone).localize(scheduled_datetime)

    # Convert scheduled_datetime to Unix timestamp (number)
    scheduled_timestamp = int(scheduled_datetime.timestamp())

    # Schedule the post
    
    graph.put_photo(parent_object=page_id, image=image_path, message=message, published=False, scheduled_publish_time=scheduled_timestamp)
    
    
    #open(image_path, 'rb')

def post_to_facebook_demo_schedule(access_token, page_id, message, image_path, scheduled_datetime, selected_timezone):
    graph = facebook.GraphAPI(access_token)

    # Convert scheduled_datetime to the selected timezone
    scheduled_datetime = pytz.timezone(selected_timezone).localize(scheduled_datetime)

    # Convert scheduled_datetime to Unix timestamp (number)
    scheduled_timestamp = int(scheduled_datetime.timestamp())

    # Schedule the post
    
    graph.put_photo(parent_object=page_id, image=open(image_path, 'rb'), message=message, published=False, scheduled_publish_time=scheduled_timestamp)
    
            
            
@st.cache_data
def login_to_facebook_existing_user(App_name,restuarant_name,location,nature_of_cuisine,occasion,offer,other_keywords):
    global browser

    #facebook content generation
    st.subheader("Facebook Post Content Generation")
    content=content_generator(restuarant_name,location,nature_of_cuisine,occasion,offer)
    modified_content=st.text_area("Generated Facebook Post Content",content)


    #image generation
    image_urls= image_generator(other_keywords)


    # Display all images with buttons
    for i, image_url in enumerate(image_urls):
        st.image(image_url, caption=f'Image {i + 1}', use_column_width=True, width=200)
    selected_image_index = st.text_input("Enter the image you want to choose (e.g., 1)",key="selected image")
    
    selected_profile = None  # Assign a default value

    if st.toggle("Post to Facebook"):
        if selected_image_index:
            st.write("Posting images")
            if 1 <= int(selected_image_index) <= len(image_urls):
                st.session_state.selected_image_index = int(selected_image_index) - 1
                st.session_state.selected_image_url = image_urls[int(selected_image_index) - 1]
                image_path= image_urls[int(selected_image_index) - 1]
                st.text(f"Selected Image {selected_image_index}")                
                facebook_username = st.text_input("Enter your Facebook username")
                facebook_password = st.text_input("Enter your Facebook password", type="password")
                if st.checkbox("Login to facebook"):
                    username=facebook_username
                    password=facebook_password
                    if facebook_username and facebook_password:
                        st.info("Logging in to Facebook...")
                        #login_to_facebook(App_name,restuarant_name,location,nature_of_cuisine,occasion,offer,other_keywords)
                        #page_id,permanant_access_token = app_creation(username, password, App_name)
                                #image_path = 'image.jpeg'
                        access_token = permanant_access_token  # Your Facebook access token here
                                #page_id = '179897971873271'  # Your Facebook page ID here
                        message = str(modified_content)

                        if st.checkbox("Schedule Post" ):
                            image_url = image_path
                            image_response = requests.get(image_url)
                            graph = facebook.GraphAPI(access_token)
                            print(page_id)

                            # Check if the request was successful (status code 200)
                            if image_response.status_code == 200:
                            # Open the image file in binary mode
                                with open('local_image.png', 'wb') as file:
                                    # Write the content of the response to the file
                                    file.write(image_response.content)
                            image_path = 'local_image.png'
                            caption = modified_content

                            # Set default values for scheduled date and time
                            
                            all_timezones = [tz for tz in pytz.all_timezones]

# Add UTC to the beginning of the list
                            all_timezones.insert(0, "UTC")

                            # Get current datetime
                            current_datetime = datetime.now()

                            # Set default values
                            default_date = current_datetime.date()
                            default_time = current_datetime.time()

                            # Input fields for date, time, and time zone
                            schedule_date = st.date_input("Enter Scheduled Date:", value=default_date, key="schedule_date")
                            schedule_time = st.time_input("Enter Scheduled Time:", key="schedule_time")
                            selected_timezone = st.selectbox("Select Time Zone:", all_timezones, index=all_timezones.index('UTC'), key="selected_timezone")

                            # Button to trigger scheduling
                            if st.checkbox("Schedule the Post") and image_path is not None and caption and schedule_date and schedule_time and selected_timezone:
                                # Combine date and time to create the scheduled_time string
                                scheduled_datetime_str = f"{schedule_date} {schedule_time}"
                                scheduled_datetime = datetime.strptime(scheduled_datetime_str, "%Y-%m-%d %H:%M:%S")
                                # Convert to UTC
                                #scheduled_datetime_utc = scheduled_datetime.replace(tzinfo=pytz.timezone("UTC"))
                                scheduled_datetime_utc = scheduled_datetime_tz.astimezone(pytz.utc)

                                
                                selected_timezone_object = pytz.timezone(selected_timezone)
                                scheduled_datetime_tz = selected_timezone_object.localize(scheduled_datetime, is_dst=None)


                                # Convert to the selected timezone
                                #scheduled_datetime_tz = scheduled_datetime_utc.astimezone(timezone(selected_timezone))
                                #scheduled_datetime_tz = scheduled_datetime_utc.astimezone(pytz.timezone(selected_timezone))
                                scheduled_datetime_tz = pytz.timezone(selected_timezone).localize(scheduled_datetime_utc)


                                scheduled_time = scheduled_datetime_tz.strftime("%Y-%m-%dT%H:%M:%S%z")

                                # Schedule the post using the provided inputs
                                print("schedule")
                                print(access_token)
                                print(page_id)
                                schedule.every().second.do(
                                    post_to_facebook_demo_schedule,
                                    page_id=page_id,
                                    access_token=access_token,
                                    image_path=image_path,
                                    message=modified_content,
                                    scheduled_time=scheduled_time,
                                    timezone=selected_timezone
                                ) 
                                                                
                                #st.success("Post scheduled. You can close this window, and the post will be posted at the scheduled time.")
                                st.success(f"Post scheduled for {scheduled_time}.")

                        if st.checkbox("Post Now"):
                            post_to_facebook_demo(access_token, page_id, message, image_path)
                            st.success("Post published successfully.")
                        # Button to close the browser
                            if st.button("Close Browser"):
                                close_browser()
                    else:
                        st.warning("Please enter both Facebook username and password.")
            else:
                st.warning(f"Invalid image index. Please enter a number between 1 and {len(image_urls)}.")
                
def initialize_user_data():
    try:
        user_data = pd.read_excel("user_data.xlsx")
    except FileNotFoundError:
        columns = ['Username', 'Password', 'PageID', 'AccessToken']
        user_data = pd.DataFrame(columns=columns)
        user_data.to_excel("user_data.xlsx", index=False)
    return user_data

@st.cache_data
#posting to facebook page
def post_to_facebook_demo(access_token, page_id, message, image_path):
    image_url = image_path
    image_response = requests.get(image_url)
    graph = facebook.GraphAPI(access_token)
    print(page_id)

    # Check if the request was successful (status code 200)
    if image_response.status_code == 200:
    # Open the image file in binary mode
        with open('local_image.png', 'wb') as file:
            # Write the content of the response to the file
            file.write(image_response.content)

            # Now you can use 'local_image.png' as the image path in your code
        graph.put_photo(parent_object='me', image=image_response.content, message=message)
        # image=open(image_path, 'rb'),
        st.text ("Posted")

    else:
        print(f"Failed to download image. Status code: {image_response.status_code}")
def post_to_facebook_demo_file_upload(access_token, page_id, message, image_path):
    #image_url = image_path
    #image_response = requests.get(image_url)
    graph = facebook.GraphAPI(access_token)
    print(page_id)

    # Check if the request was successful (status code 200)
    #if image_response.status_code == 200:
    # Open the image file in binary mode
    #    with open('local_image.png', 'wb') as file:
            # Write the content of the response to the file
    #        file.write(image_response.content)

            # Now you can use 'local_image.png' as the image path in your code
    graph.put_photo(parent_object='me', image=open(image_path, 'rb'), message=message)
    st.text ("Posted")






# Function to run the scheduling thread
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

def close_browser():
    global browser
    if browser:
        browser.quit()
        st.success("Browser closed successfully.")
        


def main():
    st.title("Welcome to Facebook Post Automation App")

    # Sidebar dropdown for login options
    login_option = st.sidebar.selectbox("Choose login option:", ("Select", "Admin login", "User login"))

    if login_option == "Select":
        st.warning("Please select a login option.")

    elif login_option == "Admin login":
        st.warning("Admin login feature is not implemented yet.")
        # You can add admin login functionality here if needed.

    elif login_option == "User login":
        # User credentials step
        st.subheader("User Credentials")
        user_username = st.text_input("Enter your username")
        user_password = st.text_input("Enter your password", type="password")

        if st.checkbox("Validate User Credentials"):
            if validate_user_credentials(user_username, user_password):
                st.success("User credentials validated successfully!")

                # Facebook login and profile selection step
                st.subheader("Facebook Login and Profile Selection")
                #facebook_username = st.text_input("Enter your Facebook username")
                #facebook_password = st.text_input("Enter your Facebook password", type="password")
                App_name = st.text_input("Enter your Facebook App Name")
                restuarant_name=st.text_input("Enter Your Resturant name")
                nature_of_cuisine=st.text_input("Enter Nature of Cuisine")
                occasion=st.text_input("Enter the occasion")
                offer=st.text_input("Enter the offer or the discount")
                other_keywords=st.text_input("Enter any other for image genration")
                location=st.text_input("Enter your loaction")
                
                #options = ['Existing user', 'New User']

                # Display the radio button in the Streamlit app
                #selected_option = st.radio("Select an option:", options)
                if st.checkbox('Existing user'):
                    login_to_facebook_existing_user(App_name,restuarant_name,location,nature_of_cuisine,occasion,offer,other_keywords)
                    
                if st.checkbox('New User'): 
                    login_to_facebook(App_name,restuarant_name,location,nature_of_cuisine,occasion,offer,other_keywords)      
            else:
                st.error("Invalid user credentials. Please try again.")
                
schedule_thread = threading.Thread(target=run_schedule)
schedule_thread.start()


if __name__ == "__main__":
    main()