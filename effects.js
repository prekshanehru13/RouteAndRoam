function createSnowflake() {
    const snowflake = document.createElement("div");
    snowflake.innerHTML = "❄";
    snowflake.className = "snowflake";
    snowflake.style.left = Math.random() * window.innerWidth + "px";
    snowflake.style.animationDuration = (Math.random() * 3 + 2) + "s";
    document.body.appendChild(snowflake);

    setTimeout(() => {
        snowflake.remove();
    }, 5000);
}

setInterval(createSnowflake, 200);
