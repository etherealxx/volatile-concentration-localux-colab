let startTime;
let timeout;
let myHeaders = new Headers();
myHeaders.append("Bypass-Tunnel-Reminder", "Thanks for checking my code lol")
myHeaders.append("ngrok-skip-browser-warning", "Seriously tho, thank you so much!")
// hello nocrypt, etherealxx here. mind if i... ummm, borrow your code for a bit? 😋

function updateTimer(el) {
  const a = (i) => (i < 10 ? "0" + i : i);
  const b = (x) => Math.floor(x);
  let c = b(Date.now() / 1000) - startTime;
  h = a(b(c / 3600));
  m = a(b((c / 60) % 60));
  s = a(b(c % 60));
  // console.log(h,m,s)

  // show different text betwen 4:58 and 5:15
  if (c > 298 && c < 315) {
    el.innerText =
      "Usually there's captcha at this time, please check your colab (" +
      h +
      ":" +
      m +
      ":" +
      s +
      ")";
  } else {
    el.innerText = h + ":" + m + ":" + s;
  }

  //refresh timer every 30 seconds
  if (c % 30 == 0) {
    refreshTimer(el, true);
    return;
  }

  timeout = setTimeout(() => updateTimer(el), 1000);
}

refreshTimer = (timerEl, notext = false) => {
  if (timeout) {
    clearTimeout(timeout);
    timeout = null;
  }
  if (!notext) timerEl.innerText = "Connecting...";
  fetch("file=static/colabTimer.txt", { cache: "no-store", headers: myHeaders })
    .then((response) => {
      if (response.status == 404) {
        timerEl.innerText = "Error. Colab disconnected!";
        return;
      }
      response.text().then((text) => {
        startTime = parseInt(text);
        if (isNaN(startTime))
          timerEl.innerText = "Error. NaN stuff... Maybe network error";
        else updateTimer(timerEl);
      });
    })
    .catch((err) => {
      console.log(err);
      timerEl.innerText = "Error. "+err;
    });
};

toggleNotification = (imgEl, audioEl, divEl) => {
  audioEl.muted = !audioEl.muted
  audioEl.currentTime = 0;
  audioEl.play();
  divEl.title = !audioEl.muted ? "Currently not-muted. Click to mute" : "Currently muted. Click to unmute";
  divEl.style.borderColor =
    !audioEl.muted
      ? "#00ff00"
      : "#ff0000";
  imgEl.src = audioEl.muted ? "https://api.iconify.design/ion:md-notifications-off.svg?color=%23ff0000" : "https://api.iconify.design/ion:md-notifications.svg?color=%2300ff00";
}

onUiLoaded(function () {
  const quickSettings = gradioApp().querySelector("#quicksettings");
  const audioEl = gradioApp().querySelector("#audio_notification > audio")

  if (gradioApp().querySelector("#nocrypt-timer") != null) return;

  let mainDiv = document.createElement("div");
  mainDiv.id = "nocrypt-timer";
  mainDiv.className = "flex justify-start";
  mainDiv.style = "gap: 10px; user-select: none; margin-block: -10px; transform-origin: left center; scale: 0.8;";

  let div2 = document.createElement("div");
  div2.className = "flex gap-2 items-center border-solid border gr-box";
  div2.style =
    "cursor: pointer; padding-block: 3px; width: fit-content; padding-inline: 5px; border-color: hsl(300, 65%, 61%); z-index: 999; background-color: transparent !important;";
  div2.title = "Colab Timer Integration by NoCrypt. Click to refresh.";

  let img = document.createElement("img");
  img.src =
    "https://ssl.gstatic.com/colaboratory-static/common/de56aa663d279b80074b6c21f69dc872/img/favicon.ico";
  img.width = 24;
  img.style.filter = "hue-rotate(270deg)";

  let timerEl = document.createElement("div");
  timerEl.style = "font-family: monospace;color: hsl(300, 65%, 61%);";
  timerEl.innerText = "Connecting...";
  div2.appendChild(img);
  div2.appendChild(timerEl);
  mainDiv.appendChild(div2);
  div2.onclick = () => refreshTimer(timerEl);

  // notification mute
  audioEl.volume = 0.6; // Request from RileyX: "its a bit too loud"
  let div3 = document.createElement("div");
  div3.className = "flex gap-2 items-center border-solid border gr-box";
  div3.style =
    "cursor: pointer; padding-block: 3px; width: fit-content;  padding-inline: 5px; border-color: lime; z-index: 999; background-color: transparent !important;";
  div3.title = "Currently not-muted. Click to mute";

  let img2 = document.createElement("img");
  img2.src =
    "https://api.iconify.design/ion:md-notifications.svg?color=%2300ff00";
  img2.width = 20;
  div3.appendChild(img2);
  div3.onclick = () => toggleNotification(img2, audioEl, div3);
  mainDiv.appendChild(div3);

  quickSettings.parentNode.insertBefore(mainDiv, quickSettings.nextSibling);
  refreshTimer(timerEl);
});
