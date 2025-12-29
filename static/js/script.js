document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    // 요소가 제대로 있는지 확인 (디버깅용)
    if (!sendBtn) {
        console.error("send-btn 버튼을 찾을 수 없습니다! ID 확인하세요.");
        return;
    }

    // 전송 버튼 클릭 이벤트
    sendBtn.addEventListener('click', sendMessage);

    // 엔터키로도 전송
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // 사용자 메시지 표시
        appendMessage('user', message);
        userInput.value = '';

        // 서버로 보내기 (fetch 예시)
        fetch('/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage('bot', data.response || '응답이 없습니다.');
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage('bot', '오류가 발생했습니다.');
        });
    }

    function appendMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', sender);
        msgDiv.innerHTML = `<p>${text}</p>`;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // 자동 스크롤
    }
});