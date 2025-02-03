document.getElementById('prompt_button').addEventListener('click', async () => {
const prompt_text = document.getElementById('prompt_text').value;
const response = await fetch('http://127.0.0.1:5000/recommend', {
    method: 'POST', 
    headers: {
        'content-type': 'application/json'
    },
    body: JSON.stringify({ prompt: prompt_text })
});
const data = await response.json();
document.getElementById('result').innerText = JSON.stringify(data);
});