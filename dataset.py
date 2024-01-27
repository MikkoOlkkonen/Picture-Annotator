from torch.utils.data import Dataset
from torchvision.transforms import ToTensor

class ImageDataset(Dataset):
    def __init__(self, images):
        super().__init__()
        self.images = images
        self.annotations = []
        for image in self.images:
            self.annotations.extend(image.get_annotations())

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, indeksi):
        annotation = self.annotations[indeksi]
        x, y, w, h = annotation.get_rectangle().getCoords()
        x, y, w, h = int(x), int(y), int(w), int(h)
        label = annotation.get_name()

        #Etsitään kuva, jolle annotaatio kuuluu
        i = 0
        while i < len(self.images) and annotation not in self.images[i].get_annotations():
            i += 1
        image = self.images[i]
        image_crop = image.crop((x, y, x+w, y+h))
        image_tensor = ToTensor()(image_crop)
        return image_tensor, label