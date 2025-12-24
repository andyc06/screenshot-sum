# import sys
import time
import pytesseract
import pandas
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image

SCREENSHOTS_PATH = "/Users/andy/Screenshots"

# returns a pandas Series of high confidence numbers from the input image path
def get_image_numbers(image_path):
    # page segmentation methods https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html#page-segmentation-method
    # toggle load_system_dawg to 0 if not generally expecting words in input image
    custom_config = r"--psm 11 load_system_dawg 1"

    image = Image.open(image_path)

    data = pytesseract.image_to_data(image=image, config=custom_config, output_type=pytesseract.Output.DATAFRAME)
    
    # high confidence OCR results only
    filtered = data.loc[data["conf"] >= 90, "text"]
    
    # extract the numbers and get rid of NaN rows
    amounts = (
        filtered
            .astype(str)
            .str.extract(r"(\d+\.\d+|\d+)", expand=False)
            .astype(float)
    ).dropna()

    return amounts


# subclassing watchdog event class
# https://stackoverflow.com/questions/32923451/how-to-run-an-function-when-anything-changes-in-a-dir-with-python-watchdog
class Event(FileSystemEventHandler):
    def on_moved(self, event):
        new_screenshot = event.dest_path
        numbers_series = get_image_numbers(new_screenshot)
        numbers_series_string = numbers_series.to_string(index=False)
        total_sum = numbers_series.sum()
        combined_message = """
        New screenshot found: {new_screenshot}
        Numbers detected:
        {numbers_series_string}
        Sum: {total_sum}
        """.format(new_screenshot=new_screenshot, numbers_series_string=numbers_series_string, total_sum=total_sum)
        print("New screenshot created: ", new_screenshot)
        print("Numbers detected:")
        print(numbers_series_string)
        print("Sum: ", numbers_series.sum())

        os.system(
            'osascript -e \'tell application "System Events" to display dialog "{}" with title "Message"\''.format(
                combined_message.replace('"', '\\"')
            )
        )



# watch the screenshot directory
if __name__ == "__main__":
    path = SCREENSHOTS_PATH
    event_handler = Event()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
