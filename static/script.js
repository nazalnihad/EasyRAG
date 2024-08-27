const togglePDFButton = document.getElementById('toggle-pdf');
const toggleChatButton = document.getElementById('toggle-chat');
const pdfContainer = document.querySelector('.pdf-container');
const chatContainer = document.querySelector('.chat-container');
const processingElement = document.getElementById('processing');
let isProcessing = false;

function displayPDF(file,page_num=1) {
    fetch(`/display_pdf/${encodeURIComponent(file)}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        return response.blob();
    })
    .then(blob => {
        const pdfUrl = URL.createObjectURL(blob);
        const pdfViewer = document.getElementById('pdf-content');
        pdfViewer.innerHTML = `<iframe src="${pdfUrl}#page=${page_num}" width="100%" height="100%"></iframe>`;
    })
    .catch(error => {
        console.error('There was a problem displaying the PDF:', error);
        alert('Error displaying PDF.');
    });
}
// Process document function
function processDocument(file) {
    if (isProcessing) return; // Prevent multiple clicks
    isProcessing = true;
    processingElement.classList.add('active');

    fetch('/process_document', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ file: file }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        updateNewFilesList();
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        alert('Error processing document.');
    })
    .finally(() => {
        isProcessing = false;
        processingElement.classList.remove('active');
    });
}

// Refresh file list
document.getElementById('refresh-files').addEventListener('click', updateNewFilesList);

// Update new files list
function updateNewFilesList() {
    fetch('/get_new_files')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        return response.json();
    })
    .then(data => {
        const newFileList = document.getElementById('new-file-list');
        newFileList.innerHTML = '';
        data.forEach(file => {
            const li = document.createElement('li');
            li.innerHTML = `${file} <button onclick="processDocument('${file}')">Process</button>`;
            newFileList.appendChild(li);
        });
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

// Handle query input
// document.getElementById('query-input').addEventListener('keypress', function (e) {
//     if (e.key === 'Enter') {
//         const query = this.value;
//         this.value = '';
        
//         const messagesDiv = document.getElementById('chat-messages');
//         messagesDiv.innerHTML += `<div class="user-message">${query}</div>`;

//         fetch('/query', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ query: query }),
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok.');
//             }
//             return response.json();
//         })
//         .then(data => {
//             let botResponse = '';
//             if (!data.response || data.response.trim() === '') {
//                 botResponse = "I can't find info on that.";
//             } else {
//                 // Use a Markdown parser to convert the response to HTML
//                 botResponse = marked.parse(data.response);
//             }
//             if (botResponse.startsWith('source')){
                
//             }

//             messagesDiv.innerHTML += `<div class="bot-message">${botResponse}</div>`;
//             messagesDiv.scrollTop = messagesDiv.scrollHeight;
//         })
//         .catch(error => {
//             console.error('There was a problem with the fetch operation:', error);
//         });
//     }
// });

document.getElementById('query-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        const query = this.value;
        this.value = '';
        
        const messagesDiv = document.getElementById('chat-messages');
        messagesDiv.innerHTML += `<div class="user-message">${query}</div>`;

        fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query }),
        })
        .then(response => response.json())
        .then(data => {
            let botResponse = '';
            if (!data.response || data.response.trim() === '') {
                botResponse = "I can't find info on that.";
            } else {
                // Replace custom markdown format with clickable links
                botResponse = data.response.replace(/\(source:\s*([^,]+)\s*,\s*page:\s*(\d+)\)/g, 
                    (match, filename, page) => {
                        return `\n\nsource : <a href="#" onclick="displayPDF('${filename}', ${page})">${filename}, page: ${page}</a>`;
                    }
                );
            }
            // Use `marked.parse` to convert markdown to HTML after replacing the links
            const finalResponse = marked.parse(botResponse);
            messagesDiv.innerHTML += `<div class="bot-message">${finalResponse}</div>`;
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    }
});



// Toggle PDF visibility
togglePDFButton.addEventListener('click', function() {
    pdfContainer.classList.toggle('hidden');
    this.textContent = pdfContainer.classList.contains('hidden') ? 'Show PDF' : 'Hide PDF';
    updateLayout();
});

// Toggle Chat visibility
toggleChatButton.addEventListener('click', function() {
    chatContainer.classList.toggle('hidden');
    this.textContent = chatContainer.classList.contains('hidden') ? 'Show Chat' : 'Hide Chat';
    updateLayout();
});

// Update layout
function updateLayout() {
    const visibleContainers = document.querySelectorAll('.main-content > div:not(.hidden)');
    
    if (visibleContainers.length > 0) {
        if (visibleContainers.length === 1) {
            visibleContainers[0].style.maxWidth = '100%';
            visibleContainers[0].style.flex = '1 0 100%';
        } else {
            const totalWidth = 100 / visibleContainers.length;
            visibleContainers.forEach(container => {
                container.style.maxWidth = '40vw'; // Default max width
                container.style.flex = `1 0 ${totalWidth}%`;
            });
        }
    }
}

// Initial layout update
updateLayout();
