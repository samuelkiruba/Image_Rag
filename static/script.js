document.getElementById('uploadForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const questionInput = document.getElementById('questionInput');
    const responseDiv = document.getElementById('response');

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
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