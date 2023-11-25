from PIL import Image
# from rembg import remove
import os

folder_dir = "/home/bapary/Videos/Coala/Cartoon"
count = 0
for images in os.listdir(folder_dir):

    if (images.endswith(".png") or images.endswith(".jpg")
        or images.endswith(".jpeg") or images.endswith(".PNG")
        or images.endswith(".JPEG") or images.endswith(".JPG")):
        print(images)

        path = os.path.join(folder_dir,images)
        image = Image.open(path)

        #output = remove(image)
        count = count + 1
        # image.convert('RGB').save('/home/bapary/Downloads/PetImages/cat/'+'cat'+images)
        # for i in range(1,11):
        image.resize((200,200)).save(f'/home/bapary/Videos/Coala/img'+'_'+str(count)+'.png')

