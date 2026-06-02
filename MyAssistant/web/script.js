// লিসেনিং স্টেট ট্র্যাক করার জন্য ভ্যারিয়েবল
let isListeningNow = false;

// মাইক্রোফোন আইকনে ক্লিক করলে চালু হবে
document.getElementById("assistant-circle").addEventListener("click", function() {
    if (!isListeningNow) {
        startListening();
    }
});

function startListening() {
    isListeningNow = true;
    document.getElementById("status").innerText = "Listening... 🎙️";
    
    eel.listen()(function(text) {
        isListeningNow = false; // লিসেনিং প্রসেস শেষ
        
        // যদি সফলভাবে কোনো কথা শুনতে পায় এবং তাতে কোনো এরর মেসেজ না থাকে
        if (text && !text.includes("sorry") && !text.includes("couldn't hear")) {
            document.getElementById("status").innerText = "You said: " + text;
            eel.process_command(text);
        } else {
            document.getElementById("status").innerText = "Listening again...";
            // গ্যাপ সামান্য বাড়িয়ে ১.৫ সেকেন্ড করা হয়েছে যাতে ব্যাকগ্রাউন্ড জ্যাম না হয়
            setTimeout(startListening, 1500); 
        }
    });
}

// Python থেকে রেসপন্স দেখানো
eel.expose(show_response);
function show_response(text) {
    document.getElementById("response").innerHTML = `<strong>Alexa:</strong><br>${text}`;
    
    // অ্যাসিস্ট্যান্টের উত্তর দেওয়া বা কথা বলা শেষ হলে ২.৫ সেকেন্ড পর আবার অটোমেটিক শুনবে
    setTimeout(startListening, 2500); 
}

// লিসেনিং অ্যানিমেশন
eel.expose(show_listening);
function show_listening(isListening) {
    const circle = document.getElementById("assistant-circle");
    if (isListening) {
        circle.style.transform = "scale(1.1)";
        circle.style.boxShadow = "0 0 50px #00c3ff";
    } else {
        circle.style.transform = "scale(1)";
        circle.style.boxShadow = "none";
    }
}