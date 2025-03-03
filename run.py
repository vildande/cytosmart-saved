from AxionVueOpenAPI import AxionVueOpenAPI
import time
from PIL import Image


def save_image(x, y):
    connector.move_stage_fast(serial_numbers[0], x, y)
    img = connector.get_image_fast(serial_numbers[0])
    # print(x, y)
    return img, (x, y)

def create_combined_image(images, grid_size, x_offset=0):
    # Calculate the size of the combined image
    img_width, img_height = images[0][0].size
    combined_img = Image.new('RGB', (img_width * grid_size[0], img_height * grid_size[1]))

    
    for img, (x, y) in images:
        # Adjust x position by the offset
        adjusted_x =  (x-6)* img_width
        combined_img.paste(img, (adjusted_x, (y-14) * img_height))

    print("Saving...")
    combined_img.save('image_result.png')


connector = AxionVueOpenAPI(number_of_devices=1, warranty=False)
serial_numbers = connector.get_all_serial_numbers()
print('connected', serial_numbers)

# connector.do_autofocus(serial_numbers[0], "CSslide")
# print('autofocused')

# connector.set_liveview(serial_numbers[0], True) 
time.sleep(0.5)

connector.set_focus(serial_numbers[0], 0.500)

connector.set_liveview(serial_numbers[0], True) # Led of device turns off till you take a picture

time.sleep(0.5)

connector.open_liveview(serial_numbers[0]) # Opens liveview in the default browser
connector.set_liveview(serial_numbers[0], True)

time.sleep(5)
connector.move_stage(serial_numbers[0], 0, 0)
time.sleep(10)
connector.set_liveview(serial_numbers[0], True)
time.sleep(1)

print("Current Position:", connector.get_position(serial_numbers[0]))


# Collect images and their positions
images = []

for i in range(7, 20, 1):
    for j in range(0, 20, 1):
        img, position = save_image(i, j)
        images.append((img, position))

# Create and save the combined image
grid_size = (25-6, 35 - 14)  # Size of the grid based on the loop ranges
create_combined_image(images, grid_size)





print("THe End!")


# # time.sleep(11.5)
# connector.move_stage(serial_numbers[0], 10, 10)
# print("moved")
# time.sleep(1.5)
# for i in range(5):
#     print(connector.get_position(serial_numbers[0]))
#     time.sleep(5)

