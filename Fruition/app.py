from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from PIL import Image
from fastapi.staticfiles import StaticFiles
from src.services import FruitMaster
from src.requestModel import ChatMessage

app = FastAPI()
fruit_master = FruitMaster()

# Serve HTML template
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Load the uploaded image
    contents = await file.read()
    
    # Open image and ensure it's RGB
    image = Image.open(file.file).convert("RGB")
    #Predict Image and get index
    predicted_name, y = fruit_master.predict(image=image)
    print(predicted_name, y)
    #get fruit details--r
    # category, description, fruit_benefits, smoothie_recipe, similar_fruits_list = fruit_master.get_details(predicted_name)
    gemini_details = fruit_master.get_details_from_gemini(predicted_name)

    if predicted_name and y > 0.5:
        return JSONResponse(content={
            "response_code": 200,
            "name": predicted_name,
            "accuracy": round(y * 100, 2),
            "full_details": gemini_details
            })
    
    elif predicted_name and y < 0.5:
        return JSONResponse(content={
            "response_code": 300,
            "accuracy": round(y * 100, 2),
            "guess": predicted_name})        

    else:
        # print(f'Unable to detect image')
        return JSONResponse(content={
            "response_code": 400,
            "undetected": "Unable to detect the Image"})


@app.post("/chat")
async def chat(message: ChatMessage):
    input = message.message
    if not input:
        response = fruit_master.get_details_from_gemini()
        return {"response": response}
    response = fruit_master.get_details_from_gemini(question=input)
    return {"response": response}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", reload=True)