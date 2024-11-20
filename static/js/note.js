var thisIsAVariable = 'this is a string!';

// There are numbers and booleans too
thisIsAVariable = 1;
thisIsAVariable = 1.1;
thisIsAVariable = true;
thisIsAVariable = false;

// This is a simple function that adds two numbers
function add(x, y) {
  return x + y;
}

var sum = add(1, 2); // 3

// The + operator is how you do string concatenation as well,
// like in Python.
var unitCode = 'INFO' + '2222';
// I prefer single quotes for strings, but double quotes
// are also available

// Some string operations
unitCode.length; // 8
unitCode.slice(4); // '2222'
unitCode.toLowerCase(); // 'info2222'

// In case you didn't realise, these are comments.

// This is an array. It's like a list in Python.
var array = [0, 'foobar', true];

array[1]; // 'foobar'
array.length; // 3
array.indexOf('foobar'); // 1
array.push(-1); // -1 is now at the end of the array.
array.pop(); // Removes the last value from the array.

// There's like a billion different ways of looping over an array,
// but this is the easiest.
for (var value of array) {
  // This will log the value to your browser's console
  // in the developer tools (recommended).
  console.log(value);

  // This will bring up an alert box in the browser
  // (less recommended).
  alert(value);
}

// This is an 'object'. It's basically just like a dictionary
// in Python. The syntax is pretty similar, even.
// In JavaScript, objects have 'properties'.
var obj = {
  hello: 'world',
  foo: 'bar',
  nested: {
    value: 1
  }
}

obj.nested.value; // 1
obj.nested.value = 2;

// This is a conditional
if (obj.hello === 'world' && obj.nested.value <= 0) {
  // This condition is false, so this won't run.
}

// Note that the equality operator is written with three equals
// signs. The inequality operator is written !==, and is also
// three characters long. (This is important)


// convert strings to binary data
function encodeString(string) {
    var encoder = new TextEncoder();
    return encoder.encode(string);
}
  
function decodeString(encoded) {
    var decoder = new TextDecoder();
    return decoder.decode(encoded);
}

// generate a key (CryptoKey object)
crypto.subtle.generateKey(
    {
        name: 'algorithm-name'
        // Other options
    },
    true,
    ['encrypt', 'decrypt']
).then(function (keyOrKeyPair) {
    // Do something with your key(s)
});

// encrypt a string by key (binary)
function encryptString(string) {
    var encoded = encodeString(string);

    return crypto.subtle.encrypt(
        {
        name: 'algorithm-name'
        // Other options
        },
        key,
        encoded
    );
}

encryptString('Hello World!').then(function(encrypted) {
// Do something with the encrypted data.
// Note that this is binary data (see more below).
})

// decrypt the string
function decryptString(encrypted) {
    var decrypted = crypto.subtle.decrypt(
        {
        name: 'algorithm-name'
        // Other options
        },
        key,
        encrypted
    );

    return decodeString(decrypted);
}
  
  // Imagine you have some encrypted string `encrypted`
  
decryptString(encrypted).then(function(string) {
// Do something with your decrypted string
});