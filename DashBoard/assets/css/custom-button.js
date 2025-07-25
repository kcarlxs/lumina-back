document.addEventListener("DOMContentLoaded", function() {
    if (!document.getElementById("btn-sair")) {
        var btn = document.createElement("a");
        btn.id = "btn-sair";
        btn.href = "http://localhost:8000/logout";
        btn.innerText = "Logout";
        btn.style.backgroundColor = "#1c1f31ff"; 
        btn.style.color = "#ffffffff";
        document.body.appendChild(btn);
    }
});

