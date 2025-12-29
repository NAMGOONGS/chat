// DOM 요소
const chat = document.getElementById('chat');
const input = document.getElementById('input');

// send 함수 - 전역 스코프에 정의 (onclick 속성에서 접근 가능)
async function send() {
  const msg = input.value.trim();
  if (!msg) return;
  
  const btn = document.querySelector('button');
  btn.disabled = true;
  btn.textContent = '전송 중...';
  
  addMsg(msg, 'user');
  input.value = '';

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: msg})
    });
    
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }
    
    const data = await res.json();
    addMsg(data.reply, 'bot');
  } catch (error) {
    console.error('오류:', error);
    addMsg('❌ 오류: ' + error.message, 'bot');
  } finally {
    btn.disabled = false;
    btn.textContent = '전송';
  }
}

// 메시지 추가 함수
function addMsg(text, sender) {
  const div = document.createElement('div');
  div.className = `msg ${sender}`;
  div.textContent = (sender === 'user' ? 'You' : 'Bot') + ': ' + text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

// 엔터키 이벤트
document.addEventListener('DOMContentLoaded', function() {
  input.addEventListener('keypress', e => {
    if (e.key === 'Enter') send();
  });
});

