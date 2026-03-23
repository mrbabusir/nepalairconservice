function setLang(lang){
    const flag = document.getElementById("currentFlag");
    const langText = document.getElementById("currentLang");

    if(lang==="en"){
        flag.src="https://flagcdn.com/w20/gb.png";
        langText.textContent="EN";
    } else {
        flag.src="https://flagcdn.com/w20/np.png";
        langText.textContent="ने";
    }

    document.querySelectorAll("[data-lang]").forEach(el=>{
        el.style.display = el.getAttribute("data-lang") === lang ? "block" : "none";
    });

    // ✅ THIS WAS MISSING
    localStorage.setItem("siteLanguage", lang);

    document.getElementById("langMenu").classList.remove("show");
}