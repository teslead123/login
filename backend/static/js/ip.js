fetch('https://api.ipify.org?format=json')
  .then(response => response.json())
  .then(data => {
    console.log('Public IP:', data.ip);
    sendIPToServer(data.ip);  // send IP only once
  });

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function sendIPToServer(ip) {
  fetch('/receive-ip/', {   // Use your Django URL here
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ public_ip: ip }),
  })
  .then(response => response.json())
  .then(data => console.log('Server response:', data))
  .catch(err => console.error('Error:', err));
}
