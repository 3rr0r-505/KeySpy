document.addEventListener("DOMContentLoaded", async function () {
    try {
        // Fetch keystrokes and visited sites from the server
        const response = await fetch('/data');
        const { keystrokes, sites } = await response.json();

      // Display fetched data in the HTML
        const keystrokesList = document.getElementById('keystrokes');
        const sitesList = document.getElementById('sites');
    
        keystrokes.forEach(keystroke => {
            const li = document.createElement('li');
            li.textContent = `${keystroke.timestamp} > Keystroke: ${keystroke.keystroke}`;
            keystrokesList.appendChild(li);
        });

        sites.forEach(site => {
            const li = document.createElement('li');
            li.textContent = `${site.timestamp} > Site: ${site.site}`;
            sitesList.appendChild(li);
        });
    } catch (error) {
        console.error('Error fetching data:', error);
        // Handle error
    }
});