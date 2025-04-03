// const recordButton = document.getElementById('record');
// const stopButton = document.getElementById('stop');
// const audioElement = document.getElementById('audio');
// const uploadForm = document.getElementById('uploadForm');
// const audioDataInput = document.getElementById('audioData');
// const timerDisplay = document.getElementById('timer');

// let mediaRecorder;
// let audioChunks = [];
// let startTime;

// function formatTime(time) {
//   const minutes = Math.floor(time / 60);
//   const seconds = Math.floor(time % 60);
//   return `${minutes}:${seconds.toString().padStart(2, '0')}`;
// }

// recordButton.addEventListener('click', () => {
//   navigator.mediaDevices.getUserMedia({ audio: true })
//     .then(stream => {
//       mediaRecorder = new MediaRecorder(stream);
//       mediaRecorder.start();

//       startTime = Date.now();
//       let timerInterval = setInterval(() => {
//         const elapsedTime = Math.floor((Date.now() - startTime) / 1000);
//         timerDisplay.textContent = formatTime(elapsedTime);
//       }, 1000);

//       mediaRecorder.ondataavailable = e => {
//         audioChunks.push(e.data);
//       };

//       mediaRecorder.onstop = () => {
//         const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
//         const formData = new FormData();
//         formData.append('audio_data', audioBlob, 'recorded_audio.wav');

//         fetch('/upload', {
//             method: 'POST',
//             body: formData
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             location.reload(); // Force refresh

//             return response.text();
//         })
//         .then(data => {
//             console.log('Audio uploaded successfully:', data);
//             // Redirect to playback page or display success message
//         })
//         .catch(error => {
//             console.error('Error uploading audio:', error);
//         });
//       };
//     })
//     .catch(error => {
//       console.error('Error accessing microphone:', error);
//     });

//   recordButton.disabled = true;
//   stopButton.disabled = false;
// });

// stopButton.addEventListener('click', () => {
//   if (mediaRecorder) {
//     mediaRecorder.stop();
//   }

//   recordButton.disabled = false;
//   stopButton.disabled = true;
// });

// // Initially disable the stop button
// stopButton.disabled = true;
// script.js

//Working latest
// const recordButton = document.getElementById('record');
// const stopButton = document.getElementById('stop');
// const audioElement = document.getElementById('audio');
// const uploadForm = document.getElementById('uploadForm');
// const audioDataInput = document.getElementById('audioData');
// const timerDisplay = document.getElementById('timer');
// const ttsGenerateButton = document.getElementById('ttsGenerate');
// const ttsInput = document.getElementById('ttsInput');
// const ttsAudio = document.getElementById('ttsAudio');

// let mediaRecorder;
// let audioChunks = [];
// let startTime;

// function formatTime(time) {
//     const minutes = Math.floor(time / 60);
//     const seconds = Math.floor(time % 60);
//     return `${minutes}:${seconds.toString().padStart(2, '0')}`;
// }

// recordButton.addEventListener('click', () => {
//     navigator.mediaDevices.getUserMedia({ audio: true })
//         .then(stream => {
//             mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
//             mediaRecorder.start();

//             startTime = Date.now();
//             let timerInterval = setInterval(() => {
//                 const elapsedTime = Math.floor((Date.now() - startTime) / 1000);
//                 timerDisplay.textContent = formatTime(elapsedTime);
//             }, 1000);

//             mediaRecorder.ondataavailable = e => {
//                 audioChunks.push(e.data);
//             };

//             mediaRecorder.onstop = () => {
//                 clearInterval(timerInterval);
//                 const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
//                 const audioUrl = URL.createObjectURL(audioBlob);
//                 audioElement.src = audioUrl;
//                 audioElement.controls = true;

//                 const formData = new FormData();
//                 formData.append('audio_data', audioBlob, 'recorded_audio.webm');

//                 fetch('/upload', {
//                     method: 'POST',
//                     body: formData
//                 })
//                 .then(response => {
//                     if (!response.ok) {
//                         throw new Error('Network response was not ok');
//                     }
//                     location.reload(); // Force refresh
//                     return response.text();
//                 })
//                 .then(data => {
//                     console.log('Audio uploaded successfully:', data);
//                 })
//                 .catch(error => {
//                     console.error('Error uploading audio:', error);
//                 });
//             };
//         })
//         .catch(error => {
//             console.error('Error accessing microphone:', error);
//         });

//     recordButton.disabled = true;
//     stopButton.disabled = false;
// });

// stopButton.addEventListener('click', () => {
//     if (mediaRecorder) {
//         mediaRecorder.stop();
//     }
//     recordButton.disabled = false;
//     stopButton.disabled = true;
// });

// // Initially disable the stop button
// stopButton.disabled = true;

// ttsGenerateButton.addEventListener('click', () => {
//     const text = ttsInput.value.trim();
//     if (!text) {
//         alert('Please enter text to convert to speech');
//         return;
//     }

//     const formData = new FormData();
//     formData.append('text', text);

//     fetch('/upload_text', {
//         method: 'POST',
//         body: formData
//     })
//     .then(response => {
//         if (!response.ok) throw new Error('Network response was not ok');
//         location.reload();
//     })
//     .catch(error => console.error('Error generating audio:', error));
// });
const recordButton = document.getElementById('record');
const stopButton = document.getElementById('stop');
const audioElement = document.getElementById('audio');
const uploadForm = document.getElementById('uploadForm');
const audioDataInput = document.getElementById('audioData');
const timerDisplay = document.getElementById('timer');

let mediaRecorder;
let audioChunks = [];
let startTime;

function formatTime(time) {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
}

recordButton.addEventListener('click', () => {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
            audioChunks = [];
            mediaRecorder.start();

            startTime = Date.now();
            let timerInterval = setInterval(() => {
                const elapsedTime = Math.floor((Date.now() - startTime) / 1000);
                timerDisplay.textContent = formatTime(elapsedTime);
            }, 1000);

            mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
            mediaRecorder.onstop = () => {
                clearInterval(timerInterval);
                const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                const audioUrl = URL.createObjectURL(audioBlob);
                audioElement.src = audioUrl;
                audioElement.controls = true;

                const formData = new FormData();
                formData.append('audio_data', audioBlob, 'recorded_audio.webm');
                fetch('/upload', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    if (!response.ok) throw new Error('Network response was not ok');
                    location.reload();
                })
                .catch(error => console.error('Error uploading audio:', error));
            };
        })
        .catch(error => console.error('Error accessing microphone:', error));

    recordButton.disabled = true;
    stopButton.disabled = false;
});

stopButton.addEventListener('click', () => {
    if (mediaRecorder) mediaRecorder.stop();
    recordButton.disabled = false;
    stopButton.disabled = true;
});

stopButton.disabled = true;