const chatInput = document.getElementById("chat-input");
const chatMessages = document.getElementById("chat-messages");
const chatToggle = document.getElementById("chat-toggle");
const chatbox = document.getElementById("chatbox");

// -------------------- Chat Toggle --------------------
if (chatToggle && chatbox) {
  const chatOpen = localStorage.getItem("chatOpen") === "true";
  chatbox.style.display = chatOpen ? "flex" : "none";

  chatToggle.addEventListener("click", () => {
    const isOpen = chatbox.style.display === "flex";
    chatbox.style.display = isOpen ? "none" : "flex";
    localStorage.setItem("chatOpen", !isOpen);
  });
}

// -------------------- Chatbot Logic --------------------
if (chatInput && chatMessages) {
  // Welcome message
  const welcomeDiv = document.createElement("div");
  welcomeDiv.className = "bot-msg animate-msg";
  welcomeDiv.textContent =
    "Hi! I'm INTEL bot. Ask me about delivery, customers, campaigns, or other metrics.";
  chatMessages.appendChild(welcomeDiv);

  chatInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter" && chatInput.value.trim() !== "") {
      const userMsg = chatInput.value;
      const userDiv = document.createElement("div");
      userDiv.className = "user-msg animate-msg";
      userDiv.textContent = userMsg;
      chatMessages.appendChild(userDiv);
      chatMessages.scrollTop = chatMessages.scrollHeight;

      // Bot typing indicator
      const typingDiv = document.createElement("div");
      typingDiv.className = "bot-msg typing";
      typingDiv.textContent = "INTEL is typing...";
      chatMessages.appendChild(typingDiv);
      chatMessages.scrollTop = chatMessages.scrollHeight;

      fetch("/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMsg }),
      })
        .then((res) => res.json())
        .then((data) => {
          // Remove typing indicator
          chatMessages.removeChild(typingDiv);

          // Highlight keywords in the bot's reply
          let reply = data.reply;

          // If bot doesn't understand, provide fallback message
          if (!reply || reply.toLowerCase().includes("sorry")) {
            reply =
              "I'm not sure about that. Please contact one of our employees for assistance.";
          } else {
            const keywords = [
              "delivery",
              "customers",
              "campaign",
              "recovery",
              "SLA",
            ];
            keywords.forEach((kw) => {
              const regex = new RegExp(`(${kw})`, "gi");
              reply = reply.replace(regex, "<strong>$1</strong>");
            });
          }

          const botDiv = document.createElement("div");
          botDiv.className = "bot-msg animate-msg";
          botDiv.innerHTML = reply;
          chatMessages.appendChild(botDiv);
          chatMessages.scrollTop = chatMessages.scrollHeight;
        });

      chatInput.value = "";
    }
  });
}

// -------------------- Scroll Animations --------------------
const scrollElements = document.querySelectorAll(".animate-on-scroll");

const elementInView = (el, offset = 0) => {
  const elementTop = el.getBoundingClientRect().top;
  return (
    elementTop <=
    (window.innerHeight || document.documentElement.clientHeight) - offset
  );
};

const displayScrollElement = (element) => {
  element.classList.add("visible");
};

const handleScrollAnimation = () => {
  scrollElements.forEach((el) => {
    if (elementInView(el, 100)) {
      displayScrollElement(el);
    }
  });
};

window.addEventListener("scroll", handleScrollAnimation);
window.addEventListener("load", handleScrollAnimation);
