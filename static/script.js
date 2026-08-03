const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");
const clearBtn = document.getElementById("clearBtn");
const browseBtn = document.getElementById("browseBtn");
const dropArea = document.getElementById("dropArea");
const loading = document.getElementById("loading");
const form = document.getElementById("uploadForm");
const predictBtn = document.getElementById("predictBtn");


// Open file explorer
browseBtn.addEventListener("click", function () {
    imageInput.click();
});

// Preview selected image
imageInput.addEventListener("change", function () {

    const file = imageInput.files[0];

    if (!file) return;

    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";

});

// Drag over
dropArea.addEventListener("dragover", function (e) {

    e.preventDefault();

    dropArea.style.background = "#e0e7ff";

});

// Drag leave
dropArea.addEventListener("dragleave", function () {

    dropArea.style.background = "#f8f9ff";

});

// Drop Image
dropArea.addEventListener("drop", function (e) {

    e.preventDefault();

    dropArea.style.background = "#f8f9ff";

    const file = e.dataTransfer.files[0];

    if (!file) return;

    imageInput.files = e.dataTransfer.files;

    preview.src = URL.createObjectURL(file);

    preview.style.display = "block";

});

// Form Submit
form.addEventListener("submit", function (e) {

    if (imageInput.files.length === 0) {

        e.preventDefault();

        alert("⚠ Please upload an image first.");

        return;

    }

    loading.style.display = "block";

    predictBtn.disabled = true;

    predictBtn.innerHTML = "Analyzing...";

});

// Clear Button
clearBtn.addEventListener("click", function () {

    imageInput.value = "";

    preview.src = "";

    preview.style.display = "none";

    loading.style.display = "none";

    predictBtn.disabled = false;

    predictBtn.innerHTML = "Predict Image";

    stopCamera();

    video.srcObject = null;

    video.style.display = "none";

    captureBtn.style.display = "none";

    retakeBtn.style.display = "none";

    // Remove result card
    const result = document.querySelector(".result");

    if(result){

        result.remove();

    }

    const uploaded = document.querySelector(".uploaded-image");

    if (uploaded) {
    uploaded.remove();
    }

    // Remove warning
    const warning = document.querySelector(".warning");

    if(warning){

        warning.remove();

    }

});

window.addEventListener("load", function () {

    const canvas = document.getElementById("predictionChart");

    if (!canvas) return;

    const rows = document.querySelectorAll(".result table tr");

    const labels = [];
    const values = [];

    rows.forEach((row, index) => {

        if (index === 0) return;

        const cols = row.querySelectorAll("td");

        if (cols.length === 2) {

            labels.push(cols[0].innerText);

            values.push(parseFloat(cols[1].innerText.replace("%", "")));

        }

    });

    console.log(labels);
    console.log(values);

    new Chart(canvas, {

        type: "bar",

        data: {

            labels: labels,

            datasets: [{

                label: "Confidence",

                data: values,

                backgroundColor: [
                    "#4F46E5",
                    "#22C55E",
                    "#F59E0B",
                    "#EF4444",
                    "#06B6D4"
                ]

            }]

        },

        options: {

            responsive: true,

            scales: {

                y: {

                    beginAtZero: true,

                    max: 100

                }

            }

        }

    });

});

const themeBtn = document.getElementById("themeBtn");

if(localStorage.getItem("theme") === "dark"){

    document.body.classList.add("dark");

    themeBtn.innerHTML = "☀ Light Mode";

}

themeBtn.addEventListener("click",()=>{

    document.body.classList.toggle("dark");

    if(document.body.classList.contains("dark")){

        localStorage.setItem("theme","dark");

        themeBtn.innerHTML="☀ Light Mode";

    }else{

        localStorage.setItem("theme","light");

        themeBtn.innerHTML="🌙 Dark Mode";

    }

});

const startCameraBtn = document.getElementById("startCameraBtn");
const captureBtn = document.getElementById("captureBtn");
const retakeBtn = document.getElementById("retakeBtn");
const video = document.getElementById("camera");
const canvas = document.getElementById("cameraCanvas");

let cameraStream = null;

// ===============================
// Stop Camera Function
// ===============================

function stopCamera(){

    if(cameraStream){

        cameraStream.getTracks().forEach(track => {

            track.stop();

        });

        cameraStream = null;

    }

}


startCameraBtn.addEventListener("click", async () => {

    stopCamera();

    try{

        cameraStream = await navigator.mediaDevices.getUserMedia({
            video:true
        });

        video.srcObject = cameraStream;

        video.style.display="block";

        captureBtn.style.display="inline-block";

    }
    catch(err){

        alert("Unable to access camera.");

    }

});

captureBtn.addEventListener("click",()=>{

    canvas.width = video.videoWidth;

    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");

    ctx.drawImage(video,0,0);

    canvas.toBlob(function(blob){

        const file = new File([blob],"camera.jpg",{
            type:"image/jpeg"
        });

        const dt = new DataTransfer();

        dt.items.add(file);

        imageInput.files = dt.files;

        preview.src = URL.createObjectURL(file);

        preview.style.display="block";

    });

    cameraStream.getTracks().forEach(track=>track.stop());

    stopCamera();

    video.srcObject = null;

    video.style.display="none";

    captureBtn.style.display="none";

    retakeBtn.style.display = "inline-block";

});

retakeBtn.addEventListener("click", async () => {

    preview.src = "";

    preview.style.display = "none";

    imageInput.value = "";

    try{

        cameraStream = await navigator.mediaDevices.getUserMedia({

            video:true

        });

        video.srcObject = cameraStream;

        video.style.display = "block";

        captureBtn.style.display = "inline-block";

        retakeBtn.style.display = "none";

    }

    catch(err){

        alert("Unable to access camera.");

    }

});

// =============================
// Search Prediction History
// =============================

const historySearch =
document.getElementById("historySearch");

if(historySearch){

historySearch.addEventListener("keyup",function(){

let value =
this.value.toLowerCase();

let rows =
document.querySelectorAll("#historyTable tr");

rows.forEach(row=>{

let text =
row.innerText.toLowerCase();

if(text.indexOf(value)>-1){

row.style.display="";

}else{

row.style.display="none";

}

});

});

}