// for the first dummy user
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

        var user1 = document.getElementById("user1").textContent;

        document.getElementById("pk1").innerHTML = 
        "You have a public key now: " + user1; //+ ": " + pk_string;  

        var data = {
            username: user1,
            pub_key: pk_string // wow this is a bad password
        };

        // send the public key by a new post to the server
        fetch('/getkey', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
    });

    crypto.subtle.exportKey('jwk', PKE.privateKey).then(function(jwk) {
        var sk_string = JSON.stringify(jwk);

        var user1 = document.getElementById("user1").textContent;

        document.getElementById("sk1").innerHTML = 
        "You have a private key now: "+ user1;// + ": "+ sk_string;

        // store sk in client side
        localStorage.setItem(user1, sk_string);
    });
    
});


// for the second dummy user
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

        var user2 = document.getElementById("user2").textContent;

        document.getElementById("pk2").innerHTML = 
        "You have a public key now: " + user2; //+ ": " + pk_string;  

        var data = {
            username: user2,
            pub_key: pk_string // wow this is a bad password
        };

        // send the public key by a new post to the server
        fetch('/getkey', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
    });

    crypto.subtle.exportKey('jwk', PKE.privateKey).then(function(jwk) {
        var sk_string = JSON.stringify(jwk);

        var user2 = document.getElementById("user2").textContent;

        document.getElementById("sk2").innerHTML = 
        "You have a private key now: "+ user2;// + ": " + sk_string;

        // store sk in client side
        localStorage.setItem(user2, sk_string);
    });
});