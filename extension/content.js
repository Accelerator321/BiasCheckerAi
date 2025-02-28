chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "push_content") {
        
        
        // console.log(message.payload);
        document.body.innerHTML = message.payload;
        document.body.style.width = "80%";
        document.getElementById("sticky-button").style.display = "none";
        chrome.storage.local.set({ "progress": "", id:""});
        
        return true; 
    }
});




chrome.runtime.sendMessage({ action: "url-fetched", url: window.location.href});

