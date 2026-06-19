const streamImg   = document.getElementById("backendStream");
const canvas      = document.getElementById("overlay");
const ctx         = canvas.getContext("2d");
const statusText  = document.getElementById("statusText");

let isDetecting      = false;
let detectionInterval = null;
let modelsLoaded     = false;

// ── 1. Load face-api models in the background ──────────────────────────
window.addEventListener('DOMContentLoaded', async () => {
    try {
        const MODEL_URL = 'https://cdn.jsdelivr.net/npm/@vladmandic/face-api/model/';
        await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL);
        modelsLoaded = true;
        statusText.innerText = "Status: Models Loaded. Stream is Live.";
    } catch (e) {
        console.error(e);
        statusText.innerText = "Status: Failed to load models. Check internet connection.";
    }
});

// ── 2. Snapshot — calls your existing Flask /save_photo route ──────────
document.getElementById("takeSnapshotBtn").addEventListener("click", function () {
    fetch('/save_photo', { method: 'POST' })
        .then(r => r.json())
        .then(data => alert(data.message))
        .catch(err => console.error('Snapshot error:', err));
});

// ── 3. Grayscale toggle ────────────────────────────────────────────────
function makeGrayscale() {
    streamImg.classList.toggle("gray-effect");
}

// ── 4. Face Detection on the backend stream ────────────────────────────
const offscreenCanvas = document.createElement('canvas');
const offscreenCtx    = offscreenCanvas.getContext('2d');

function toggleFaceDetection() {
    if (!modelsLoaded) {
        alert("Models are still loading. Please wait a moment.");
        return;
    }

    if (!isDetecting) {
        isDetecting = true;
        statusText.innerText = "Status: Scanning for Faces...";

        detectionInterval = setInterval(async () => {
            const w = streamImg.offsetWidth;
            const h = streamImg.offsetHeight;

            // Resize offscreen canvas to match display size
            offscreenCanvas.width  = w;
            offscreenCanvas.height = h;

            // Draw the current MJPEG frame into the offscreen canvas
            offscreenCtx.drawImage(streamImg, 0, 0, w, h);

            // Match the overlay canvas dimensions
            canvas.width  = w;
            canvas.height = h;

            // Run face detection on the offscreen canvas
            const detections = await faceapi.detectAllFaces(
                offscreenCanvas,
                new faceapi.TinyFaceDetectorOptions()
            );

            // Resize results to match display dimensions
            const resized = faceapi.resizeResults(detections, { width: w, height: h });

            // Clear previous frame's boxes
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (resized.length > 0) {
                resized.forEach(detection => {
                    const box = detection.box;

                    // Red bounding box
                    ctx.strokeStyle = 'red';
                    ctx.lineWidth = 3;
                    ctx.strokeRect(box.x, box.y, box.width, box.height);

                    // Label background
                    ctx.fillStyle = 'red';
                    ctx.fillRect(box.x, box.y - 20, 80, 20);

                    // Label text
                    ctx.fillStyle = 'white';
                    ctx.font = '14px Arial';
                    ctx.fillText('UNKNOWN', box.x + 5, box.y - 5);
                });
                statusText.innerText = "Status: ⚠️ UNKNOWN PERSON DETECTED!";
            } else {
                statusText.innerText = "Status: Scanning... No face found.";
            }
        }, 100);

    } else {
        stopDetection();
    }
}

function stopDetection() {
    isDetecting = false;
    clearInterval(detectionInterval);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    statusText.innerText = "Status: Detection Stopped. Stream is Live.";
}

// ── 5. Car movement ───────────────────────────────────────────────────
function move(action) {
    console.log("Action sent: " + action);
    // Hook up your Flask route here, e.g.:
    // fetch(`/move/${action}`, { method: 'POST' });
}
