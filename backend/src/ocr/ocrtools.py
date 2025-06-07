import pytesseract 
from PIL import Image,PdfParser,ImageOps
import requests 
from io import BytesIO
from pathlib import Path
import json
async def extract_resume_test(image_url: str):
    image = Image.open(BytesIO(requests.get(image_url).content))
    image = ImageOps.grayscale(image)
    image = ImageOps.autocontrast(image)
    text = pytesseract.image_to_string(image)
    return text

async def conversion_of_text_to_json(image_url: str):
    result : str = await extract_resume_test(image_url)
    json_result = json.dumps({"extracted text from resume":result},indent=-2)
    return json_result

# result = conversion_of_text_to_json(r"https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.etsystatic.com%2F38349274%2Fr%2Fil%2Fd2e6ee%2F4263663700%2Fil_794xN.4263663700_fj2u.jpg&f=1&nofb=1&ipt=d3a8dea717c85e3d436b97557dc96f997a57b1b6f643035f4007532a9a23b056")
# print(json.loads(result))
