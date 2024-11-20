// generate a key (CryptoKey object)

crypto.subtle.generateKey(  // CryptoKeyPair
    {
        name: 'RSA-OAEP',
        modulusLength: 4096,
        publicExponent: new Uint8Array([1, 0, 1]),
        hash: "SHA-256"
    },
    true,
    ['encrypt', 'decrypt']
).then(function(PKE) {

    // export pk and sk
    crypto.subtle.exportKey('jwk', PKE.publicKey).then(function(jwk) {
        var pk_string = JSON.stringify(jwk);
        // document.getElementById("public").innerHTML = 
        // "You have a public key now: " + pk_string;

        var user = document.getElementById("username").textContent;

        var data = {
            username: user,
            pub_key: pk_string 
        };

        // send the public key by a new post to the server
        fetch('/getkey', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }).then(() => {
            // Removing the progress bar and making the button appear.
            const to_login = document.querySelector("#to-login");
            const prog_bar = document.querySelector("#progress-bar");
            const generating = document.querySelector("#generating");
            const finish = document.querySelector("#finished");

            to_login.addEventListener('click', () => {
                window.location.replace("/login");
            })

            to_login.classList.remove("is-hidden");
            finish.classList.remove("is-hidden");
            prog_bar.classList.add("is-hidden");
            generating.classList.add("is-hidden");
            console.log("done");
        });
    });

    // store sk in client side

    crypto.subtle.exportKey('jwk', PKE.privateKey).then(function(jwk) {
        var sk_string = JSON.stringify(jwk);
        // document.getElementById("private").innerHTML = 
        // "You have a private key now: " + sk_string;
        var username = document.getElementById("username").textContent;

        localStorage.setItem(username, sk_string);
    });
});