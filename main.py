import os
import time

from prepper import DataPrepper

if __name__ == '__main__':
    dir_path = 'Wellington'
    pet_names = ["Wellington", "Ton", "Tonny", "Tonnybear", "Beefer", "Wellington Beef"]

    prepper = DataPrepper(data_path=dir_path)
    prepper.setup_dir()

    dir_items = os.listdir(dir_path)

    for file in dir_items:

        name = os.path.splitext(file)[0]
        ext = os.path.splitext(file)[1]

        if ext == '.jpg' and f'{name}.txt' not in dir_items:

            description_list = prepper.describe_img(img_path=f'{dir_path}/{file}')
            prepper.write_file(file_name=os.path.splitext(file)[0],
                               text_list=description_list + pet_names)

            time.sleep(30)

        else:
            pass