const server = "http://127.0.0.1:5000/analyse"

// chrome.storage.local.set({ "progress": "", id:""});

chrome.storage.local.get(["progress","id"], (result) => {
    if(!result) return;
    console.log(result.progress,"ds", " id ", result.id); 
    if(result.progress){
        document.body.innerHTML = result.progress;
        document.getElementById("sticky-button").addEventListener("click", (e) => {
            chrome.storage.local.get(["progress","id"], (result) => {

                if(result.progress && result.id){
                    console.log("res", result.id, result.progress)
                    chrome.storage.local.set({ "progress": "", id:""});
                    chrome.tabs.sendMessage(result.id, { action: "push_content", payload: result.progress });
                }

            });

        });

    }


});


document.addEventListener("DOMContentLoaded", function () {
    // Create a button element
    let closeButton = document.createElement("button");
    closeButton.innerText = "X";
    closeButton.style.position = "fixed";
    closeButton.style.top = "10px";
    closeButton.style.right = "10px";
    closeButton.style.width = "20px";

    closeButton.style.background = "red";
    closeButton.style.color = "white";
    closeButton.style.border = "none";
    closeButton.style.cursor = "pointer";


    closeButton.addEventListener("click", () => {
        chrome.storage.local.set({ progress: "", id: "" }, () => {
            window.close(); 
        });
    });


    document.body.appendChild(closeButton);
});





chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
    if (message.action === "fetched") {


        let res = await fetch(server, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "query": message.content
            })
        });

        res= await res.json();
        document.getElementsByClassName("loader-container")[0].style.display = "none";

        if(res.content) {
            document.body.innerHTML = res.content;
        // Create the Bias Analysis Section
            let biasSection = document.createElement("div");
            biasSection.id = "bias-analysis-section";
            biasSection.innerHTML =`<h2>Bias Analysis</h2><p>${res.bias}</p>`;
            document.body.prepend(biasSection);


            let stickButton = document.createElement("button");
            stickButton.id = "sticky-button";
            stickButton.innerText ="Insert into Tab";
            document.body.prepend(stickButton);

            chrome.storage.local.set({ "id":sender.tab.id,"progress": document.documentElement.outerHTML});

            stickButton.addEventListener("click", (e) => {

                chrome.storage.local.set({ "progress": "", id:""});
                chrome.tabs.sendMessage(sender.tab.id, { action: "push_content", payload: document.documentElement.outerHTML });


            });

        }
        else{
            alert("Something went wrong please try again.");
            document.getElementById("detectButton").style.display = 'initial';
        }


        return true
    }
});

document.getElementById("detectButton").addEventListener("click", (e) => {
    document.getElementsByClassName("loader-container")[0].style.display = "flex";
    e.target.style.display = 'none';

    chrome.runtime.sendMessage({ action: "startProcessing" });
});

