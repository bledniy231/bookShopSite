const usernameField = document.querySelector('#usernameField');
const feedBackArea = document.querySelector(".invalid_feedback");
const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const password1Field = document.querySelector("#password1Field");
const password1FeedBackArea = document.querySelector(".password1FeedBackArea");


password1Field.addEventListener("keyup", (e) => {
    const password1Val = e.target.value;
    password1Field.classList.remove("is-invalid");
    password1FeedBackArea.style.display = "none";
    if (password1Val.length > 0){
    fetch("/validate-password1/", {
        body: JSON.stringify({password1: password1Val}), method: "POST",
    })
        .then((res)=>res.json())
        .then((data) => {
            console.log("data", data);
            if (data.password1_error){
                password1Field.classList.add("is-invalid");
                password1FeedBackArea.style.display = "block";
                password1FeedBackArea.innerHTML = `<p>${data.password1_error}</p>`;
            }
        });
    }
})

emailField.addEventListener("keyup", (e) => {
    const emailVal = e.target.value;
    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";
    if (emailVal.length > 0){
    fetch("/validate-email/", {
        body: JSON.stringify({email: emailVal}), method: "POST",
    })
        .then((res)=>res.json())
        .then((data) => {
            console.log("data", data);
            if (data.email_error){
                emailField.classList.add("is-invalid");
                emailFeedBackArea.style.display = "block";
                emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
            }
        });
    }
});

usernameField.addEventListener("keyup", (e) => {
    const usernameVal = e.target.value;
    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display = "none";
    if (usernameVal.length > 0){
    fetch("/validate-username/", {
        body: JSON.stringify({username: usernameVal}), method: "POST",
    })
        .then((res)=>res.json())
        .then((data) => {
            console.log("data", data);
            if (data.username_error){
                usernameField.classList.add("is-invalid");
                feedBackArea.style.display = "block";
                feedBackArea.innerHTML = `<p>${data.username_error}</p>`;
            }
        });
    }
});