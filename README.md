## Cytosmart Scanning
This repository is a saved files necessary to continue creating a Python-based solution to interface with Cytosmart hardware using the **AxionVueOpenAPI** library (link: https://pypi.org/project/AxionVueOpenAPI/). 
The solution should automate the process of capturing and combining images from the Cytosmart scanner device into a larger composite image. This is useful for experiments where large field-of-view imaging is required.


### Overview of the system
- A computer (laptop) connects to AxionVue hardware
- Through the computer, the user controls camera settings, customizes parameters and capture images in a grid pattern.
- Captured images are combined into one large image.

#### Project Structure
```
.
├── run.py                # Main script to run the entire process
├── main.py               # AxionVueOpenAPI library file: Main logic for interacting with AxionVue device
├── listener.py           # AxionVueOpenAPI library file: Listens for hardware events and actions
└── README.md             # This file
```

The `run.py` file is used to establish a connection with the AxionVue hardware, capture images, and combine them into a single image. Here's how the main flow works:

- The script first establishes a connection with the AxionVue device.
- It sets the **focus** and **live view** of the camera.
- The device's stage is moved to capture images at different positions (a grid pattern is used for capturing multiple images).
- After collecting the images, the script combines them into a large image.

#### Code Walkthrough for `run.py`

This script orchestrates the entire process. Here’s how the flow works:

1. **Initialize the connector**: Connect to the device using `AxionVueOpenAPI`.
2. **Capture images**: The `save_image` function moves the stage and captures an image at each specified position in the grid.
3. **Create a combined image**: The `create_combined_image` function combines the images into one, placing them according to their positions on the grid.
4. **Save the final image**: Once all images are captured and combined, the final result is saved as `image_result.png`.

The basic idea is to capture images from different coordinates and combine them into a larger image for analysis or presentation.

##### Code Example:

```python
from AxionVueOpenAPI import AxionVueOpenAPI
import time
from PIL import Image

def save_image(x, y):
    connector.move_stage_fast(serial_numbers[0], x, y)
    img = connector.get_image_fast(serial_numbers[0])
    return img, (x, y)

def create_combined_image(images, grid_size, x_offset=0):
    img_width, img_height = images[0][0].size
    combined_img = Image.new('RGB', (img_width * grid_size[0], img_height * grid_size[1]))
    
    for img, (x, y) in images:
        adjusted_x = (x-6) * img_width
        combined_img.paste(img, (adjusted_x, (y-14) * img_height))

    print("Saving...")
    combined_img.save('image_result.png')

connector = AxionVueOpenAPI(number_of_devices=1, warranty=False)
serial_numbers = connector.get_all_serial_numbers()
print('connected', serial_numbers)

time.sleep(0.5)
connector.set_focus(serial_numbers[0], 0.500)
connector.set_liveview(serial_numbers[0], True)
time.sleep(0.5)

images = []
for i in range(7, 20, 1):
    for j in range(0, 20, 1):
        img, position = save_image(i, j)
        images.append((img, position))

grid_size = (25-6, 35-14)
create_combined_image(images, grid_size)
print("THe End!")
```
---
### System setup

#### Prerequisites
- have Python 3.x and pip installed
- have the Cytosmart drivers installed (they are installed with the official Cytosmart/AxionVue app)
- have the official app closed.

#### Install the library
```bash
pip install AxionVueOpenAPI
```


#### Modify the AxionVue library
##### Find the location of the files
```bash
pip show AxionVueOpenAPI
```
This will display the installation location of the library.

##### Change the files
Make sure to back up those files (just in case).
Take my `main.py` and `listener.py`, and put them instead of those in the library.


#### Customization
You can customize the following in the `run.py` script:

- **Grid Size**: Modify the range in the nested loops to adjust the grid size for capturing images.
  ```python
  for i in range(start, end, step):   # Customize the start, end, step values
  ```
- **Image saving path**: Change the path or filename where the combined image is saved in the `create_combined_image()` function.
- **Focus**: Adjust the camera focus by modifying the value passed to connector.set_focus().
```python
    connector.set_focus(serial_numbers[0], 0.500)  # Adjust this value based on your needs
```
- **Delays between actions**: The script includes time.sleep() calls to introduce delays between certain actions, such as waiting for the camera to adjust focus or for the stage to move. You can customize these delays by modifying the time.sleep() values For example:
```python
time.sleep(0.5)  # Adjust the delay time (in seconds) as needed between actions
```

#### Run the System

To run the script, simply execute the following command in your terminal:

```bash
python run.py
```
The script will connect to the hardware, capture the images in a grid pattern, and save the combined image as `image_result.png`.


---
### System's unsolved problems
- **Cannot connect to the device on the main Cytosmart laptop**: The issue might be that the laptop does not start the liveview properly. This prevents the laptop from connecting to the cytosmart device and further communication.
- **Slow image capture time**: Capturing a single image takes about 3 seconds. With a large grid scan, this could result in the entire process taking up to 1 hour or more. 


