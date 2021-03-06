import requests
from PIL import Image
import numpy as np
from os.path import abspath


def lrp_demo(picture, question):
    # http://sequel-demo.lille.inria.fr/
    url = "https://lrpserver.hhi.fraunhofer.de/visual-question-answering/api/upload_image"

    with open(picture, 'rb') as f:
        files = {'file': (picture, f.read(), 'image/jpeg')}
    r = requests.post(url, files=files).json()
    img_id = r["img_id"]

    url = "https://lrpserver.hhi.fraunhofer.de/visual-question-answering/api/upload_question"
    data = {"img_id": img_id, "question": question}
    r = requests.post(url, data=data).json()
    r["viz0"][0] = "https://lrpserver.hhi.fraunhofer.de/visual-question-answering" + r["viz0"][0][1:]
    r["viz1"][0] = "https://lrpserver.hhi.fraunhofer.de/visual-question-answering" + r["viz1"][0][1:]
    return r


def sequel_demo(picture, question):
    # http://sequel-demo.lille.inria.fr/
    url = "http://sequel-demo.lille.inria.fr/api/upload_image"

    with open(picture, 'rb') as f:
        files = {'file': (picture, f.read(), 'image/jpeg')}
    r = requests.post(url, files=files).json()
    img_id = r["img_id"]

    url = "http://sequel-demo.lille.inria.fr/api/upload_question"
    data = {"img_id": img_id, "question": question}
    r = requests.post(url, data=data).json()
    return r


def scene_parsing(picture):
    # TODO https://github.com/CSAILVision/unifiedparsing
    pass


def scene_segmentation(picture):
    # TODO use the sauce https://github.com/CSAILVision/places365
    # NOTE half broken, timeout a lot, unusable
    url = "http://scenesegmentation.csail.mit.edu/cgi-bin/image_segnet.py"
    with open(picture, 'rb') as f:
        files = {'data': (picture, f.read(), 'image/jpeg')}
    r = requests.post(url, files=files)
    print(r.text)
    return r.json()


def scene_recognition(picture, engine="MAX-Scene-Classifier"):
    if engine == "placescnn_demo":
        # NOTE half broken, timeout a lot, unusable
        url = "http://places2.csail.mit.edu/cgi-bin/image.py"
        with open(picture, 'rb') as f:
            files = {'data': (picture, f.read(), 'image/jpeg')}
    else:
        # source https://github.com/IBM/MAX-Scene-Classifier
        url = "http://207.154.234.38:5100/model/predict"
        with open(picture, 'rb') as f:
            files = {'image': f.read()}
    r = requests.post(url, files=files)
    return r.json()


def object_recognition(picture, engine="MAX-Object-Detector"):
    # source https://github.com/IBM/MAX-Object-Detector
    url = "http://207.154.234.38:5001/model/predict"
    with open(picture, 'rb') as f:
        files = {'image': f.read()}
    r = requests.post(url, files=files)
    return r.json()


def image_captioning(picture, engine="MAX-Image-Caption-Generator"):
    # source https://github.com/IBM/MAX-Image-Caption-Generator
    url = "http://207.154.234.38:5002/model/predict"
    with open(picture, 'rb') as f:
        files = {'image': (picture, f.read(), 'image/jpeg')}
    r = requests.post(url, files=files)
    return r.json()


def image_label(picture, engine="MAX-ResNet-50"):
    # source https://github.com/IBM/MAX-Inception-ResNet-v2
    if engine == "MAX-Inception-ResNet-v2":
        url = "http://207.154.234.38:5003/model/predict"
    else: # "MAX-ResNet-50"
        url = "http://207.154.234.38:5004/model/predict"
    with open(picture, 'rb') as f:
        files = {'image': f.read()}
    r = requests.post(url, files=files)
    return r.json()


def image_segmentation(picture, engine="MAX-Image-Segmenter"):
    # source  https://github.com/IBM/MAX-Image-Segmenter
    url = "http://207.154.234.38:5006/model/predict"
    with open(picture, 'rb') as f:
        files = {'image': f.read()}
    r = requests.post(url, files=files)
    return r.json()


def image_colorize(picture, engine="MAX-Image-Colorizer"):
    # source  https://github.com/IBM/MAX-Image-Colorizer
    url = "http://207.154.234.38:5007/model/predict"

    # ensure grayscale
    # NOTE not needed, use if you want to keep a copy
    #img = Image.open(picture).convert('L')
    #img.save('output_file.jpg')

    with open(picture, 'rb') as f:
        files = {'image': f.read()}
    r = requests.post(url, files=files)
    return r.content


def nudity_detection(picture, engine="deepai_demo"):
    url = "https://api.deepai.org/api/nsfw-detector"
    with open(picture, 'rb') as f:
        files = {'image': (picture, f.read(), 'image/jpeg')}
    headers = {"origin": "https://deepai.org",
                "referer": "https://deepai.org/ai-image-processing",
                "user-agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"}
    r = requests.post(url, files=files, data={"new_try_it": "1"}, headers=headers)
    job = r.json()["result_data"]["output_url"]
    r = requests.get("https://api.deepai.org" + job)
    return r.json()


def deepmask(picture, save_path=None, engine="deepai_demo"):
    save_path = save_path or picture + "_mask.jpg"
    url = "https://api.deepai.org/api/deepmask"
    with open(picture, 'rb') as f:
        files = {'content': (picture, f.read(), 'image/jpeg')}
    headers = {"origin": "https://deepai.org",
                "referer": "https://deepai.org/ai-image-processing",
                "user-agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"}
    r = requests.post(url, files=files, data={"new_try_it": "1"}, headers=headers)
    job = r.json()["result_data"]["output_url"]
    r = requests.get("https://api.deepai.org" + job).content
    with open(save_path, "wb") as f:
        f.write(r)
    return save_path


def densecap(picture, engine="deepai_demo"):
    url = "https://api.deepai.org/api/densecap"
    with open(picture, 'rb') as f:
        files = {'image': (picture, f.read(), 'image/jpeg')}
    headers = {"origin": "https://deepai.org",
                "referer": "https://deepai.org/ai-image-processing",
                "user-agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"}
    r = requests.post(url, files=files, data={"new_try_it": "1"}, headers=headers)
    job = r.json()["result_data"]["output_url"]
    return requests.get("https://api.deepai.org" + job).json()


def image_similarity(picture1, picture2, engine="deepai_demo"):
    url = "https://api.deepai.org/api/image-similarity"
    with open(picture1, 'rb') as f:
        files = {'image1': (picture1, f.read(), 'image/jpeg')}
    with open(picture2, 'rb') as f:
        files['image2'] = (picture2, f.read(), 'image/jpeg')
    headers = {"origin": "https://deepai.org",
                "referer": "https://deepai.org/ai-image-processing",
                "user-agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"}
    r = requests.post(url, files=files, data={"new_try_it": "1"}, headers=headers)
    job = r.json()["result_data"]["output_url"]
    return requests.get("https://api.deepai.org" + job).json()


def neuraltalk(picture, engine="deepai_demo"):
    url = "https://api.deepai.org/api/neuraltalk"
    with open(picture, 'rb') as f:
        files = {'image': (picture, f.read(), 'image/jpeg')}
    headers = {"origin": "https://deepai.org",
                "referer": "https://deepai.org/ai-image-processing",
                "user-agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"}
    r = requests.post(url, files=files, data={"new_try_it": "1"}, headers=headers)
    job = r.json()["result_data"]["output_url"]
    return requests.get("https://api.deepai.org" + job).text


class LILACSVisualReasoner(object):
    def __init__(self, bus=None):
        self.bus = bus or None

    def image_similarity(self, picture1, picture2, engine="deepai_demo"):
        return image_similarity(picture1, picture2, engine)["distance"]

    def nudity_detection(self, picture, engine="deepai_demo"):
        return nudity_detection(picture, engine)

    def label_image(self, picture, engine="MAX-ResNet-50"):
        return image_label(picture, engine)

    def recognize_scene(self, picture, engine="MAX-Scene-Classifier"):
        return scene_recognition(picture, engine)

    def recognize_objects(self, picture, engine="MAX-Object-Detector"):
        return object_recognition(picture, engine)

    def image_segmentation(self, picture, engine="MAX-Image-Segmenter", format="raw"):
        # format raw, picture, mask
        response = image_segmentation(picture, engine)

        LABEL_NAMES = [
            'background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
            'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike',
            'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tv'
        ]

        # add labels to raw data
        labels = []
        for n in response['seg_map']:
            for l in n:
                if l > 0 and l not in labels:
                    labels.append(l)
        labels = [LABEL_NAMES[l] for l in labels]
        response["labels"] = labels
        response["label_map"] = LABEL_NAMES

        def create_pascal_label_colormap():
            """Creates a label colormap used in PASCAL VOC segmentation benchmark.
            Returns:
              A Colormap for visualizing segmentation results.
            """
            colormap = np.zeros((256, 3), dtype=int)
            ind = np.arange(256, dtype=int)

            for shift in reversed(range(8)):
                for channel in range(3):
                    colormap[:, channel] |= ((ind >> channel) & 1) << shift
                ind >>= 3

            return colormap

        def label_to_color_image(label):
            """Adds color defined by the dataset colormap to the label.
            Args:
              label: A 2D array with integer type, storing the segmentation label.
            Returns:
              result: A 2D array with floating type. The element of the array
                is the color indexed by the corresponding element in the input label
                to the PASCAL color map.
            Raises:
              ValueError: If label is not of rank 2 or its value is larger than color
                map maximum entry.
            """
            if label.ndim != 2:
                raise ValueError('Expect 2-D input label')

            colormap = create_pascal_label_colormap()

            if np.max(label) >= len(colormap):
                raise ValueError('label value too large.')

            return colormap[label]

        image = Image.open(picture)
        image = image.resize(response['image_size'])
        seg_map = np.asarray(response['seg_map'])
        seg_image = label_to_color_image(seg_map).astype(np.uint8)

        image = Image.blend(image, Image.fromarray(seg_image), alpha=0.6)
        image.save(picture + ".seg.jpg")
        if format == "raw":
            response["annotated_image"] = abspath(picture + ".seg.jpg")
            return response
        elif format == "mask":
            return seg_image
        return image

    def colorize_image(self, picture, save_path=None, engine="MAX-Image-Colorizer"):
        if save_path is None:
            save_path = picture+"_colorize.png"
        data = image_colorize(picture, engine)
        with open(save_path, 'wb') as f:
            f.write(data)
        return abspath(save_path)

    def caption_image(self, picture, engine="MAX-Image-Caption-Generator"):
        if engine == "neuraltalk":
            return neuraltalk(picture)
        return image_captioning(picture, engine)

    def dense_captions(self, picture, engine="deepai_demo"):
        return densecap(picture, engine)["captions"]

    def answer_question(self, question, picture_path, engine="sequel_demo"):
        # check if pic is url or file
        if engine == "sequel_demo":
            return sequel_demo(picture_path, question)
        # lrp demo default
        return lrp_demo(picture_path, question)


if __name__ == "__main__":

    LILACS = LILACSVisualReasoner()

    picture = "me.jpg"

    question = "how many humans?"
    data = LILACS.answer_question(question, picture)
    result = data["answer"]
    print(result)
    # 1

    question = "are there any plants?"
    data = LILACS.answer_question(question, picture)
    result = data["answer"]
    print(result)
    # female

    data = LILACS.label_image(picture)
    result = data["predictions"][0]
    print(result)
    # {'label_id': 'n03770439', 'label': 'miniskirt', 'probability': 0.2659367024898529}

    data = LILACS.caption_image(picture)
    result = data["predictions"][0]
    print(result)
    # {'caption': 'a woman in a white shirt and a red tie', 'index': '0', 'probability': 2.5158757668475684e-05}

    data = LILACS.recognize_objects(picture)
    result = data["predictions"][0]
    print(result)
    # {'detection_box': [0.028039246797561646, 0.16406074166297913, 1.0, 0.993462085723877], 'label': 'person', 'label_id': '1', 'probability': 0.9459671974182129}

    data = LILACS.recognize_scene(picture)
    result = data["predictions"][0]
    print(result)
    # {'label': 'beauty_salon', 'label_id': '50', 'probability': 0.5930100679397583}

    data = LILACS.image_segmentation(picture)
    result = data
    print(result)
    # {'seg_map': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ...   15, 15, 15, 15, 0]], 'label_map': ['background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tv'], 'annotated_image': '/home/user/PycharmProjects/LILACS_github/lilacs/processing/vision/sasha.jpg.seg.jpg', 'image_size': [513, 513], 'status': 'ok', 'labels': ['person']}

    colorized_pic_path = LILACS.colorize_image(picture)
    print(colorized_pic_path)
    # /home/user/PycharmProjects/LILACS_github/lilacs/processing/vision/sasha.jpg_colorize.png
