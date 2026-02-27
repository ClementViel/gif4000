import pycurl
from io import BytesIO
from urllib.parse import urlencode
import json
from bs4 import BeautifulSoup
import re
#Put your own stuff here
ID=""
SECRET=""
PIWIGO_URL=""

headers = [f'X-PIWIGO-API: {ID}:{SECRET}']

def get_pwg_token():
    curl = pycurl.Curl()
    buffer = BytesIO()
    params = {'format':'json', 'method':'pwg.session.getStatus'}
    curl.setopt(pycurl.HTTPHEADER, headers)
    curl.setopt(pycurl.WRITEDATA, buffer)
    curl.setopt(pycurl.URL, "https://dereference.net/piwigo/ws.php?"+urlencode(params))
    curl.perform()
    body = buffer.getvalue().decode('utf-8')

    body = buffer.getvalue()
    # Decode using the encoding we figured out.
    json_answer = json.loads(body.decode('utf-8'))['result']

    token = json_answer['pwg_token']
    return token


def send_picture(filepath):
    # Buffer to hold the response
    filevalue = filepath
    send = [("method", "pwg.images.addSimple"), ("image", (pycurl.FORM_FILE, filepath)), ("format", "json")]
    buffer = BytesIO()
    headers_dump = BytesIO()

    # Create a Curl object
    curl = pycurl.Curl()

    # Configure the request headers
    curl.setopt(pycurl.HTTPHEADER, headers)

    # Configure the request data (using -d "key=value" syntax)
    curl.setopt(pycurl.HTTPPOST, send)
    
    # Set the URL to which we are posting
    curl.setopt(pycurl.URL, "https://dereference.net/piwigo/ws.php" )

    # Configure Curl to write the output to our buffer (instead of printing it)
    curl.setopt(pycurl.WRITEDATA, buffer)
    curl.setopt(pycurl.HEADERFUNCTION, headers_dump.write)
    # Perform the request
    curl.perform()

    # Get the response data from the buffer
    body = buffer.getvalue().decode('utf-8')

    body = buffer.getvalue()
    # Decode using the encoding we figured out.
    body_data = str(BeautifulSoup(body, "xml").find('image_id'))
    matches = re.findall(r'[0-9]+', body_data)
    return int(matches[0])

def associate_picture(token, image_id, id_album):
    # Buffer to hold the response
    post_data = {"method": "pwg.images.setCategory","action":"associate", "category_id":id_album, "image_id":image_id, "pwg_token":token }
    buffer = BytesIO()

    # Create a Curl object
    curl = pycurl.Curl()

    # Configure the request headers
    curl.setopt(pycurl.HTTPHEADER, headers)

    # Configure the request data (using -d "key=value" syntax)
    curl.setopt(pycurl.POSTFIELDS, urlencode(post_data))
    
    # Set the URL to which we are posting
    curl.setopt(pycurl.URL, "https://dereference.net/piwigo/ws.php" )

    # Configure Curl to write the output to our buffer (instead of printing it)
    curl.setopt(pycurl.WRITEDATA, buffer)
    curl.perform()
 

def get_download_link(id_album):
    curl = pycurl.Curl()
    buffer = BytesIO()
    params = {'format':'json', 'method':'pwg.categories.getImages', 'cat_id':id_album}
    curl.setopt(pycurl.HTTPHEADER, headers)
    curl.setopt(pycurl.WRITEDATA, buffer)
    curl.setopt(pycurl.URL, "https://dereference.net/piwigo/ws.php?"+urlencode(params))
    curl.perform()
    body = buffer.getvalue().decode('utf-8')

    body = buffer.getvalue()
    # Decode using the encoding we figured out.
    json_answer = json.loads(body.decode('utf-8'))['result']
    images = json_answer['images']
    url = images[0]['download_url']
    return url

def delete_image(image_id, pwg_token):
    # Buffer to hold the response
    print(f"delete image {image_id}")
    post_data = {"method": "pwg.images.delete", "image_id":image_id, "pwg_token":pwg_token }
    buffer = BytesIO()

    # Create a Curl object
    curl = pycurl.Curl()

    # Configure the request headers
    curl.setopt(pycurl.HTTPHEADER, headers)

    # Configure the request data (using -d "key=value" syntax)
    curl.setopt(pycurl.POSTFIELDS, urlencode(post_data))
    
    # Set the URL to which we are posting
    curl.setopt(pycurl.URL, "https://dereference.net/piwigo/ws.php" )

    # Configure Curl to write the output to our buffer (instead of printing it)
    curl.setopt(pycurl.WRITEDATA, buffer)
    curl.perform()
    body = buffer.getvalue().decode('utf-8')
    print(body)

def delete_shared_gifs(image_id_list, pwg_token):
    for image_id in image_id_list:
        delete_image(image_id, pwg_token)

# Call the function to make the request
def send_to_slideshow(filepath):
    token=get_pwg_token()
    image_id=send_picture(filepath)
    associate_picture(token, image_id, 1)


def send_to_share(filepath):
    token=get_pwg_token()
    image_id=send_picture(filepath)
    associate_picture(token, image_id, 2)
    url = get_download_link(2)
    return image_id, url
