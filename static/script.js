document.getElementById('uploadForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const questionInput = document.getElementById('questionInput');
    const responseDiv = document.getElementById('response');
    const uploadedImage = document.getElementById('uploadedImage');
    const imagePlaceholder = document.getElementById('imagePlaceholder');

    const file = fileInput.files[0];
    if (!file) {
        responseDiv.textContent = 'Error: Please select an image.';
        return;
    }

    // Display the uploaded image
    const reader = new FileReader();
    reader.onload = function (e) {
        uploadedImage.src = e.target.result;
        uploadedImage.style.display = 'block';
        imagePlaceholder.style.display = 'none';
    };
    reader.readAsDataURL(file);

    // Send the image and question to the server
    const formData = new FormData();
    formData.append('file', file);
    formData.append('question', questionInput.value);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            responseDiv.textContent = 'Error: ' + data.error;
        } else {
            responseDiv.textContent = 'Answer: ' + data.answer;
        }
    })
    .catch(error => {
        responseDiv.textContent = 'Error: ' + error.message;
    });
});