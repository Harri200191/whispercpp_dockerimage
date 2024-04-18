document.getElementById('uploadForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  
  const form = e.target;
  const formData = new FormData(form);
  
  try {
      const response = await fetch(form.action, {
          method: 'POST',
          body: formData
      });

      const data = await response.json();
      displayTranscription(data);
  } catch (error) {
      console.error('Error:', error);
  }
});

function displayTranscription(data) {
  const transcriptionResult = document.getElementById('transcriptionResult');
  transcriptionResult.innerHTML = ''; // Clear previous result
  
  if (data.error) {
      transcriptionResult.textContent = `Error: ${data.error}`;
  } else if (data.transcription) {
      const transcriptionList = document.createElement('ul');
      data.transcription.forEach(entry => {
          const listItem = document.createElement('li');
          listItem.textContent = `[${entry.start_time} - ${entry.end_time}]: ${entry.text}`;
          transcriptionList.appendChild(listItem);
      });
      transcriptionResult.appendChild(transcriptionList);
  }
}