const text  = document.querySelector(".shop_name");
const strText = text.textContent;
const splitText = strText.split("");
text.textContent = " ";
for (let i = 0; i < splitText.length; i++){
    text.innerHTML += "<h6>" + splitText[i] + "</h6>";
}

let char = 0;
let timer = setInterval(onTick, 90);

function onTick() {
    const h6 = text.querySelectorAll("h6")[char];
    h6.classList.add("fade");
    char++;
    if (char === splitText.length) {
        complete();
        return;
    }
}

function complete() {
    clearInterval(timer);
    timer = null;
    text.textContent = strText;

}

const nav = document.querySelectorAll(".list-group-item");


