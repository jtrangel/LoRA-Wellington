import os

from prepper import DataPrepper

if __name__ == '__main__':
    dir_path = 'Wellington'
    pet_names = ["Wellington", "Ton", "Tonny", "Tonnybear", "Beefer", "Wellington Beef"]

    prepper = DataPrepper(data_path=dir_path)
    prepper.setup_dir()

    for file in os.listdir(dir_path):

        if os.path.splitext(file)[1] == '.jpg':

            description_list = prepper.describe_img(img_path=f'{dir_path}/{file}')
            prepper.write_file(file_name=os.path.splitext(file)[0],
                               text_list=description_list + pet_names)
        else:
            pass