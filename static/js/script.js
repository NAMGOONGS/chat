// DOM 요소 (나중에 초기화)
let chat;
let input;

// 초기화 함수
function initializeChat() {
  chat = document.getElementById('chat');
  input = document.getElementById('input');
  
  if (!chat || !input) {
    console.error('필수 DOM 요소를 찾을 수 없습니다');
    return;
  }
  
  // 엔터키 이벤트 등록
  input.addEventListener('keypress', e => {
    if (e.key === 'Enter') send();
  });
  
  console.log('채팅봇 초기화 완료');
}

// send 함수 - 전역 스코프에 정의 (onclick 속성에서 접근 가능)
async function send() {
  const msg = input.value.trim();
  if (!msg) {
    console.warn('빈 메시지는 전송할 수 없습니다');
    return;
  }
  
  console.log('메시지 전송:', msg);
  
  const btn = document.querySelector('button');
  btn.disabled = true;
  btn.textContent = '전송 중...';
  
  addMsg(msg, 'user');
  input.value = '';

  try {
    console.log('/chat로 요청 전송 중...');
    const res = await fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: msg})
    });
    
    console.log('응답 상태:', res.status);
    
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }
    
    const data = await res.json();
    console.log('서버 응답:', data);
    addMsg(data.reply, 'bot');
  } catch (error) {
    console.error('오류 발생:', error);
    addMsg('❌ 오류: ' + error.message, 'bot');
  } finally {
    btn.disabled = false;
    btn.textContent = '전송';
  }
}

// 메시지 추가 함수
function addMsg(text, sender) {
  if (!chat) {
    console.error('chat 요소가 초기화되지 않았습니다');
    return;
  }
  
  const div = document.createElement('div');
  div.className = `msg ${sender}`;
  div.textContent = (sender === 'user' ? 'You' : 'Bot') + ': ' + text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  console.log('메시지 추가:', sender, text);
}

// 페이지 로드 완료 후 초기화
document.addEventListener('DOMContentLoaded', initializeChat);

