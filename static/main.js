const params = new Proxy(new URLSearchParams(window.location.search), {
    get: (searchParams, prop) => searchParams.get(prop)
});
let chat_id = params.chat_id
let username = params.username

Telegram.WebApp.ready();
Telegram.WebApp.MainButton.setText('CHECKOUT').show().onClick(function () {
    const data = JSON.stringify({chat_id: chat_id, username: username});
    Telegram.WebApp.sendData(data);
    Telegram.WebApp.close();
});

Telegram.WebApp.expand();