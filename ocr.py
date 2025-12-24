from PIL import Image
import pytesseract
import pandas

IMAGE_PATH = "/Users/andy/Screenshots/Screenshot 2025-12-24 at 14.12.48.png"

# page segmentation methods https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html#page-segmentation-method
# don't load dictionary (expecting few words in input image)
custom_config = r"--psm 11 load_system_dawg 0"

image = Image.open(IMAGE_PATH)

data = pytesseract.image_to_data(image=image, config=custom_config, output_type=pytesseract.Output.DATAFRAME)

filtered = data.loc[data["conf"] >= 90, "text"]

amounts = (
    filtered
        .str.extract(r"(\d+\.\d+|\d+)", expand=False)
        .astype(float)
)

print(amounts)
print(amounts.sum())
