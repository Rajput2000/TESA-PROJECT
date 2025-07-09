const fileInput = document.getElementById("fileInput");
const fileStatus = document.getElementById("fileStatus");
const imagePreview = document.getElementById("imagePreview");
const resultText = document.getElementById("resultText");
const full_details = document.getElementById("full_details");
const bigTxt = document.getElementById("bigTxt");
const fruitDetails = document.getElementById("fruitDetails");
const show_perc = document.getElementById("show_perc");
const submitBtn = document.getElementById("submitBtn");
const startCameraBtn = document.getElementById("startCameraBtn");
const captureBtn = document.getElementById("captureBtn");
const cameraStream = document.getElementById("cameraStream");

const chatContainer = document.getElementById("chatContainer");
const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const chatMessages = document.getElementById("chatMessages");
let stream;

// Typewriter effect function
function typeWriter(textElement, text, i = 0, speed = 15) {
  if (i < text.length) {
    textElement.innerHTML += text.charAt(i);
    setTimeout(() => typeWriter(textElement, text, i + 1, speed), speed);
  }
}

// ========== FILE INPUT ========== //
fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (file) {
    fileStatus.textContent = "File selected: " + file.name;
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.src = e.target.result;
      imageShow.style.display = "block";
    };
    reader.readAsDataURL(file);
  } else {
    fileStatus.textContent = "No file selected";
    imagePreview.style.display = "none";
  }
});

// ========== FORM SUBMIT ========== //
document.getElementById("uploadForm").addEventListener("submit", async function (e) {
  e.preventDefault();
  const formData = new FormData();
  const file = fileInput.files[0];

    // Set to loading state
  submitBtn.disabled = true;
  submitBtn.innerHTML = 'Loading...';
  

  if (!file) {
    alert("Please upload or capture an image.");
      // submitBtn.disabled = false;
      // submitBtn.innerHTML = "Submit";
    return;
  }

  formData.append("file", file);

  const response = await fetch("/predict", {
    method: "POST",
    body: formData,
  });


  const data = await response.json();

  document.getElementById("formContainer").classList.add("slide-left");
  document.getElementById("resultContainer").classList.add("slide-in-right");
  
  // Clear chat container content
  chatMessages.innerHTML = "";
  chatInput.value = "";
  chatContainer.style.display = "block";


  // Optionally reveal the content inside resultContainer
  document.getElementById("resultText").style.display = "block";
  document.getElementById("fruitDetails").style.display = "block";




  // Handle responses
  if (data.name) {
    resultText.innerHTML = "";
    full_details.innerHTML = "";
    typeWriter(resultText, "✨ " + data.name + " ✨", 0, 200);
    typeWriter(full_details, data.full_details);
    document.getElementById("percent").textContent = data.accuracy + "%";

    document.getElementById("body").classList.add("the_margin_class");
  
    resultText.style.display = "block";
    show_perc.style.display = "block";

    submitBtn.innerHTML = "Submit";
    submitBtn.disabled = false;

    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: 'smooth'
    });
  }

  if (data.guess) {
    resultText.innerHTML = "";
    typeWriter(resultText, data.guess + " (Just guessing)😇", 0, 200);
    percent.innerHTML = data.accuracy + "%";
    resultText.style.display = "block";
    fruitDetails.style.display = "none";
    show_perc.style.display = "block";

    submitBtn.innerHTML = "Submit";
    submitBtn.disabled = false;
  }

  if (data.undetected) {
    resultText.innerHTML = "";
    typeWriter(resultText, data.undetected + " 😞", 0, 200);
    resultText.style.display = "block";
    fruitDetails.style.display = "none";
    show_perc.style.display = "none";
    submitBtn.innerHTML = "Submit";
    submitBtn.disabled = false;
  }

  cameraStream.style.display = "none";
  showCapture.style.display = "none";
  startCameraBtn.style.display = "block";
});

// ========== CAMERA CAPTURE ========== //
startCameraBtn.addEventListener("click", async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    cameraStream.srcObject = stream;
    cameraStream.style.display = "block";
    showCapture.style.display = "inline-block";
    fileStatus.textContent = "Camera activated.";
    fileInput.style.display = "none";
    startCameraBtn.style.display = "none";
    resultText.style.display = "none";
    fruitDetails.style.display = "none";
    show_perc.style.display = "none";
    bigTxt.style.display = "block";
    imageShow.style.display = "none";

    document.getElementById("formContainer").classList.remove("slide-left");
    document.getElementById("body").classList.remove("the_margin_class");
  } catch (err) {
    console.error("Error accessing camera:", err);
    fileStatus.textContent = "Camera access denied or unavailable.";
  }
});

captureBtn.addEventListener("click", () => {
  const canvas = document.createElement("canvas");
  canvas.width = cameraStream.videoWidth;
  canvas.height = cameraStream.videoHeight;
  const context = canvas.getContext("2d");
  context.drawImage(cameraStream, 0, 0);

  // Convert canvas to blob
  canvas.toBlob((blob) => {
    const file = new File([blob], "capture.jpg", { type: "image/jpeg" });
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    fileInput.files = dataTransfer.files;

    // Show image preview
    const reader = new FileReader();
    reader.onload = function (e) {
      imagePreview.src = e.target.result;
      imageShow.style.display = "block";
    };
    reader.readAsDataURL(file);

    fileStatus.textContent = "Photo captured from camera.";
  });

  // Stop camera
  stream.getTracks().forEach((track) => track.stop());
  cameraStream.style.display = "none";
  showCapture.style.display = "none";
});


// ========== CHATBOT SUBMIT ========== //
chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = chatInput.value.trim();

  chatMessages.style.display = "block"

  if (!message) return;
  const userMsg = document.createElement("div");
  userMsg.className = "user-msg";
  userMsg.textContent = "🧑 " + message;
  chatMessages.appendChild(userMsg);

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await res.json();
    const botMsg = document.createElement("div");
    botMsg.className = "bot-msg";
    botMsg.textContent = "🤖 " + data.response;
    chatMessages.appendChild(botMsg);
  } catch (err) {
    const errorMsg = document.createElement("div");
    errorMsg.className = "bot-msg";
    errorMsg.textContent = "🤖 Sorry, something went wrong.";
    chatMessages.appendChild(errorMsg);
    console.error("Chat error:", err);
  }

  chatInput.value = "";
  chatMessages.scrollTop = chatMessages.scrollHeight;
});
