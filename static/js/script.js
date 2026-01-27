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

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // 사용자 메시지 표시
        appendMessage('user', message);
        userInput.value = '';
        userInput.disabled=true;

    try{ 
          const respone=await fetch('/'){
             method: 'POST',
             headers: { 'Content-Type': 'application/json' },
             body: JSON.stringify({ message: message })
        });
          if (!response.ok){
              const errorDetails =await response.text();
              throw new Error(`서버응답오류 : ${response.status}-${errorDetails}`);
          }
          const data=await response.json();
        appendMessage('bot',data.respone || '응답이 없습니다.');
      }catch(error) 
        console.error('Error',error);
        appendMessage('bot',`전송 중 오류가 발생 하였습니다. 잠시후 다시 시도해 주세요(${error.message})`);
    }
    finally{
        userInput.disable = false;
        userInput.focus();
   }
}       

    function appendMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', sender);
        msgDiv.innerHTML = `<p>${text}</p>`;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // 자동 스크롤
    }

});

