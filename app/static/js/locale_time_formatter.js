document.addEventListener("DOMContentLoaded", () => {
    const tds = document.getElementsByClassName("datetime");

    for (const td of tds) {
        if (td.firstElementChild === null) {
            let datetime = new Date(td.innerText);
            datetime = datetime.toLocaleString();
            datetime = datetime.replace(", ", "&nbsp;&nbsp;&nbsp;&nbsp;");
            td.innerHTML = datetime;
        }
    }
})