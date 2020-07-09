# QR Utility APIs

This is a flask project which implements a few QR code utility functions in API.
* Generate plain QR Code
* Generate QR Code with a logo image in the middle
* Generate QR code and add it to a image file

## Endpoints

### 1. Generate QR Code with GET
* Suitable for generating QR Code with simple single line of data, e.g. website, telephone, GPS, Text
* **Method and URL**:
    * `GET /qr_code/<string:data>`
* **URL Params (required)**: 
    * `data`: String to be embedded in QR Code
* **Success Response**:
    * Code: 200
    * Content: QR code image file
* **Sample Code (Curl)**:
    ```bash
    curl --request GET \
    --url http://localhost:3000/qr_code/tel:81234567
    ```

* **Sample Code (Python)**
    ```python
    import requests

    url = "http://localhost:3000/qr_code/tel:81234567"

    payload = ""
    response = requests.request("GET", url, data=payload)

    print(response.text)
    ```

### 2. Generate QR Code with POST
* Suitable for generating QR Code with multiple lines of data, e.g. vCard, vCalendar
* **Method and URL**:
    * `POST /qr_code`
* **Data Params (required)**: 
    * `data`: String to be embedded in QR Code
* **Success Response**:
    * Code: 200
    * Content: QR code image file
* **Sample Code (Curl)**:
    ```bash
    curl --request POST \
    --url http://localhost:3000/qr_code \
    --header 'content-type: application/json' \
    --data 'BEGIN:VCARD
    VERSION:3.0
    N:Gump;Forrest;;Mr.;
    FN:Forrest Gump
    ORG:Bubba Gump Shrimp Co.
    TITLE:Shrimp Man
    PHOTO;VALUE=URI;TYPE=GIF:http://www.example.com/dir_photos/my_photo.gif
    TEL;TYPE=WORK,VOICE:(111) 555-1212
    TEL;TYPE=HOME,VOICE:(404) 555-1212
    ADR;TYPE=WORK,PREF:;;100 Waters Edge;Baytown;LA;30314;United States of America
    LABEL;TYPE=WORK,PREF:100 Waters Edge\nBaytown\, LA 30314\nUnited States of America
    ADR;TYPE=HOME:;;42 Plantation St.;Baytown;LA;30314;United States of America
    LABEL;TYPE=HOME:42 Plantation St.\nBaytown\, LA 30314\nUnited States of America
    EMAIL:forrestgump@example.com
    REV:2008-04-24T19:52:43Z
    END:VCARD'
    ```

* **Sample Code (Python)**
    ```python
    import requests

    url = "http://localhost:3000/qr_code"

    payload = "BEGIN:VCARD\nVERSION:3.0\nN:Gump;Forrest;;Mr.;\nFN:Forrest Gump\nORG:Bubba Gump Shrimp Co.\nTITLE:Shrimp Man\nPHOTO;VALUE=URI;TYPE=GIF:http://www.example.com/dir_photos/my_photo.gif\nTEL;TYPE=WORK,VOICE:(111) 555-1212\nTEL;TYPE=HOME,VOICE:(404) 555-1212\nADR;TYPE=WORK,PREF:;;100 Waters Edge;Baytown;LA;30314;United States of America\nLABEL;TYPE=WORK,PREF:100 Waters Edge\\nBaytown\\, LA 30314\\nUnited States of America\nADR;TYPE=HOME:;;42 Plantation St.;Baytown;LA;30314;United States of America\nLABEL;TYPE=HOME:42 Plantation St.\\nBaytown\\, LA 30314\\nUnited States of America\nEMAIL:forrestgump@example.com\nREV:2008-04-24T19:52:43Z\nEND:VCARD"
    headers = {'content-type': 'application/json'}

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)
    ```

### 3. Generate QR Code with Logo in the Middle
* **Method and URL**:
    * `POST /qr_with_logo`
* **Data Params (required)**:
    * `logo`: Multi-part file of logo image 
    * `data`: String to be embedded in QR Code
* **Query String (optional)**:
    * `width`: Width of embedded logo in pixels. Default value 64. 
* **Success Response**:
    * Code: 200
    * Content: QR code image file with logo in the centre
* **Sample Code (Curl)**:
    ```bash
    curl --request POST \
    --url http://localhost:3000/qr_with_logo \
    --header 'content-type: multipart/form-data; boundary=---011000010111000001101001' \
    --form logo= \
    --form data=tel:81234567
    ```

* **Sample Code (Python)**
    ```python
    import requests

    url = "http://localhost:3000/qr_with_logo"

    payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"logo\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"data\"\r\n\r\ntel:81234567\r\n-----011000010111000001101001--\r\n"
    headers = {'content-type': 'multipart/form-data; boundary=---011000010111000001101001'}

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)
    ```

### 4. Generate QR Code and Add to an Image
* **Method and URL**:
    * `POST /qr_in_image`
* **Data Params (required)**:
    * `image`: Multi-part file of image where QR code to be embedded
    * `data`: String to be embedded in QR Code
* **Query String (optional)**:
    * `fraction`: Determine size of QR Code image in terms of fraction of the background image. Default value 0.2 
* **Success Response**:
    * Code: 200
    * Content: Image file with embedded QR code

* **Sample Code (Curl)**:
    ```bash
    curl --request POST \
        --url 'http://localhost:3000/qr_in_image?fraction=0.2' \
        --header 'content-type: multipart/form-data; boundary=---011000010111000001101001' \
        --form image= \
        --form data=tel:81234567
    ```

* **Sample Code (Python)**
    ```python
    import requests

    url = "http://localhost:3000/qr_with_logo"

    payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"logo\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"data\"\r\n\r\ntel:81234567\r\n-----011000010111000001101001--\r\n"
    headers = {'content-type': 'multipart/form-data; boundary=---011000010111000001101001'}

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)
    ```