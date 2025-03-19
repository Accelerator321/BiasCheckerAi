chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "push_content") {


        // console.log(message.payload);
        const parser = new DOMParser();
        const parsedDoc = parser.parseFromString(message.payload, "text/html");

        
        const styles = parsedDoc.querySelectorAll("style");
        styles.forEach(style => document.head.appendChild(style.cloneNode(true)));

        
        document.body.innerHTML = parsedDoc.body.innerHTML;
        document.body.style.width ='90%'
        document.getElementById("sticky-button").style.display = "none";
        chrome.storage.local.set({ "progress": "", id: "" });

        return true;
    }
});




chrome.runtime.sendMessage({ action: "fetched", content: document.body.innerText });

