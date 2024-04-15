document.addEventListener('DOMContentLoaded', () => {
    const spaceList = document.getElementById('space-list');
    const chatContainer = document.getElementById('chat-container');
    const createSpaceForm = document.getElementById('create-space-form');
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');

    let currentSpace = null;

  
    function renderSpaces(spaces) {
        spaceList.innerHTML = '';
        spaces.forEach(space => {
            const li = document.createElement('li');
            li.textContent = space.name;
            li.classList.add('space-item');
            li.addEventListener('click', () => {
                currentSpace = space;
                updateChat();
            });
            spaceList.appendChild(li);
        });
    }

  
    function renderChat(messages) {
        chatContainer.innerHTML = '';
        messages.forEach(message => {
            const div = document.createElement('div');
            div.classList.add('message');
            div.textContent = `${message.sender}: ${message.text}`;
            chatContainer.appendChild(div);
        });
    }

    function updateChat() {
        if (currentSpace) {
            axios.get(`/get_messages/${currentSpace.id}`)
                .then(response => {
                    renderChat(response.data.messages);
                })
                .catch(error => {
                    console.error('Error fetching messages:', error);
                });
        }
    }

    createSpaceForm.addEventListener('submit', event => {
        event.preventDefault();
        const spaceName = document.getElementById('space-name').value;
        axios.post('/create_space', { name: spaceName })
            .then(response => {
                renderSpaces(response.data.spaces);
            })
            .catch(error => {
                console.error('Error creating space:', error);
            });
    });

   
    messageForm.addEventListener('submit', event => {
        event.preventDefault();
        const messageText = messageInput.value;
        if (currentSpace && messageText.trim() !== '') {
            axios.post('/send_message', { spaceId: currentSpace.id, text: messageText })
                .then(response => {
                    updateChat();
                    messageInput.value = '';
                })
                .catch(error => {
                    console.error('Error sending message:', error);
                });
        }
    });

 
    axios.get('/get_spaces')
        .then(response => {
            renderSpaces(response.data.spaces);
        })
        .catch(error => {
            console.error('Error fetching spaces:', error);
        });

    setInterval(updateChat, 3000); 
});
