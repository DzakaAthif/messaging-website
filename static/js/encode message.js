//convert strings to binary data
function encodeString(string) {
    var encoder = new TextEncoder();
    return encoder.encode(string);
}
  
function decodeString(encoded) {
    var decoder = new TextDecoder();
    return decoder.decode(encoded);
}

function convertArrayBufferToBase64(arrayBuffer) {
    return btoa(String.fromCharCode(...new Uint8Array(arrayBuffer)));
}

function convertBase64ToArrayBuffer(base64) {
    return (new Uint8Array(atob(base64).split('').map(char => char.charCodeAt()))).buffer;
  }

// For Encrypting ----------------------------------------------------------

// Fetching the friend's pk.
fetch('/retrieve_pks')
.then(response => response.json())  // json object
.then(function(data) {
    // Do something with the retrieved data.
    localStorage.setItem("pks", JSON.stringify(data));  // store JSON string
});

// Event listener for the send_form.
var form = document.getElementById("send_form");
form.addEventListener( "submit", function ( event ) {

    var data = localStorage.getItem("pks");  // JSON string
    data = JSON.parse(data);  // convert back to JSON object
    
    // Get the friend name, and the message and put it
    // to localstorage.
    var name = document.getElementById("send_person").value;
    var plain_txt = document.getElementById("send_message").value;

    var json_obj = {"friend" : name, "send_message" : plain_txt};

    localStorage.setItem("send_mssg", JSON.stringify(json_obj));

    var friend_pk = data[name];  // get pk-string with friend's name
    
    // Dont forget to press test page first.
    // so the pk is not "no"
    friend_pk = JSON.parse(friend_pk);  // jwk
    
    // import the pk as cryptoKey object
    crypto.subtle.importKey(
        "jwk",
        friend_pk,
        {
            name: "RSA-OAEP",
            hash: "SHA-256",
        },
        true,
        ["encrypt"]
    ).then(function(pk) {
        //Get the message from the localStorage.
        var json = JSON.parse(localStorage.getItem("send_mssg"))
        var plain_message = json["send_message"];
        
        var encoded = encodeString(plain_message);

        crypto.subtle.encrypt(
            {
                name: 'RSA-OAEP'
            },
            pk,
            encoded
        ).then(function(ciphertext) {
            // Get the friend name from the localStorage.
            var json = JSON.parse(localStorage.getItem("send_mssg"))
            var name = json["friend"];

            var text = convertArrayBufferToBase64(ciphertext);

            // Put the cipher text to the localStorage.
            var data = {
                friend: name,
                send_message: text  // array buffer object(binary)
            };
            
            localStorage.setItem("cipher_mssg", JSON.stringify(data));

        }); //encrypt
    
    }); //importkey.

    // Set the name and the message on the form to empty
    // so the program didnt put it to the message table.
    form.send_person.value = "";
    form.send_message.value = "";

}); //addEventListener.

// Send the message and the friend name through 
// different channel.
var data = localStorage.getItem("cipher_mssg");

if (data !== null) {
    fetch('/get_ciphertext', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: data
    }); //fetch

    localStorage.setItem("cipher_mssg", null);
}

// For decrypting -----------------------------------------------------

// get username-sk
fetch('/get_username')
.then(response => response.json()) 
.then(function(data) {
    
    var user_sk = localStorage.getItem(data["user"]);  // store JSON string
    localStorage.setItem("sk", user_sk);  // store current sk
    
    });

// Get the enctypted message.
var json = document.getElementById("rec_message").textContent;
json = json.replaceAll("'", '"');
if (json !== "") {
    console.log(json);
    localStorage.setItem("rec_cipher", "");
    localStorage.setItem("rec_mssg", null);
    localStorage.setItem("length", null);
}
localStorage.setItem("rec_cipher", json);

document.getElementById("rec_message").textContent = "";

console.log("here");
var rec_cipher = localStorage.getItem("rec_cipher");

if (rec_cipher !== "" && rec_cipher.length !== 0) {

    rec_cipher = JSON.parse(rec_cipher);

    var len = rec_cipher.length;
    localStorage.setItem("length", len.toString());
    
    // Get the sk.
    var user_sk = localStorage.getItem("sk");
    
    user_sk = JSON.parse(user_sk);
    console.log("here1");
    // Import sk.
    crypto.subtle.importKey(
        "jwk",
        user_sk,
        {
            name: "RSA-OAEP",
            hash: "SHA-256",
        },
        true,
        ["decrypt"]
    ).then(function(sk) {

        var len = parseInt(localStorage.getItem("length"));
        for (var i = 0; i < len; i++) {
            //Get the message from the localStorage.
            var rec_cipher = localStorage.getItem("rec_cipher");
            rec_cipher = JSON.parse(rec_cipher);

            // Get and remove the first cipher message.
            var cipher = rec_cipher.shift();
    
            // Turn the cipher to binary.
            cipher = convertBase64ToArrayBuffer(cipher);

            // Put the reduced ciphers back to localStorage.
            if (rec_cipher.length === 0) {
                localStorage.setItem("rec_cipher", "");
            } else {
                localStorage.setItem("rec_cipher", JSON.stringify(rec_cipher));
            }
            
            // decrypt arraybuffer first -> then decode binary data
            crypto.subtle.decrypt(
                {
                    name: 'RSA-OAEP'
                },
                sk,
                cipher
            ).then(function(encoded) {
                // Decode the decryption. 
                var plaintext = decodeString(encoded);
                
                // Get the mssgs if exist
                var rec_mssg = localStorage.getItem("rec_mssg");
                rec_mssg = JSON.parse(rec_mssg);

                if (rec_mssg === null) {
                    rec_mssg = [];
                }
                
                // Push the plain text to the array of plains.
                rec_mssg.push(plaintext);

                // Put the mssgs back to the local Storage.
                localStorage.setItem("rec_mssg", JSON.stringify(rec_mssg));

                var len = localStorage.getItem("length");
                len = parseInt(len);

                rec_mssg = localStorage.getItem("rec_mssg");
                rec_mssg = JSON.parse(rec_mssg);

                if (rec_mssg !== null && rec_mssg.length === len) {

                    var mssgs = "";

                    for (var i = 0; i < rec_mssg.length; i++) {
                        mssgs += rec_mssg[i] += "\n\n";
                    }
                    console.log(mssgs);
                    document.getElementById("test_message").value = mssgs;
                    localStorage.setItem("rec_mssg", null);
                    localStorage.setItem("length", null);

                }
            });
        }
        
        
    });
    
    
}