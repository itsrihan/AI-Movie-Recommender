document.getElementById('prompt_button').addEventListener('click', async () => {
    const prompt_text = document.getElementById('prompt_text').value;
    
    try {
        const response = await fetch('http://127.0.0.1:5000/recommend', {  // Correct URL
            method: 'POST',  // Make sure it’s POST
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: prompt_text })
        });

        if (!response.ok) {
            document.getElementById('result').innerText = "Error: " + response.statusText;
            return;
        }

        const data = await response.json();
        document.getElementById('result').innerText = JSON.stringify(data);
    } catch (error) {
        document.getElementById('result').innerText = "Fetch error: " + error.message;
    }
});
