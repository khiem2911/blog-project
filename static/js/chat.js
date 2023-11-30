const id = JSON.parse(document.getElementById('json-username').textContent);
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);
const receiver = JSON.parse(document.getElementById('json-username-receiver').textContent);

const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + id
    + '/'
);
socket.onopen = function(e){
    console.log("CONNECTION ESTABLISHED");
}

socket.onclose = function(e){
    console.log("CONNECTION LOST");
}

socket.onerror = function(e){
    console.log("ERROR OCCURED");
}

console.log(socket)


const scrollToBottom = () =>{
    const table = document.querySelector('.message-table-scroll');
    table.scrollTop = table.scrollHeight;

}

socket.onmessage = function(e){
    const data = JSON.parse(e.data);
    const chatBody = document.querySelector('#chat-body');
    if(data.username == message_username){
        chatBody.innerHTML += `<tr>
                                                                <td>
                                                                <p class="bg-success p-2 mt-2 mr-5 shadow-sm text-white float-right rounded">${data.message}</p>
                                                                </td>
                                                            </tr>`
    }else{
        chatBody.innerHTML += `<tr>
                                                                <td>
                                                                <p class="bg-primary p-2 mt-2 mr-5 shadow-sm text-white float-left rounded">${data.message}</p>
                                                                </td>
                                                            </tr>`
    }
    scrollToBottom()
}

window.addEventListener('load', function() {
    scrollToBottom()
});


document.querySelector('#chat-message-submit').onclick = function(e){
    const message_input = document.querySelector('#message_input');
    const message = message_input.value;
    
    socket.send(JSON.stringify({
        'message':message,
        'username':message_username,
        'receiver':receiver,
        
    }));

    message_input.value = '';
}

const messageInput = document.getElementById('message_input');


messageInput.addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        
        event.preventDefault();
        
       const message = messageInput.value.trim();

       if(message !== ''){
            socket.send(JSON.stringify({
                'message' : message,
                'username' : message_username,
                'receiver':receiver
            }))

            messageInput.value = '';
       }
    }
});