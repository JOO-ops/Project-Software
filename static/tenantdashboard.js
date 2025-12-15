document.addEventListener("DOMContentLoaded", () => {
    
    const rows = document.querySelectorAll("tbody tr");

    let total = rows.length;
    let pending = 0;
    let completed = 0;

    rows.forEach(row => {
        let status = row.querySelector("span").textContent.trim().toLowerCase();
        
        if (status === "pending") pending++;
        if (status === "completed") completed++;
    });

    document.querySelectorAll(".card p")[0].textContent = total;
    document.querySelectorAll(".card p")[1].textContent = pending;
    document.querySelectorAll(".card p")[2].textContent = completed;

});

