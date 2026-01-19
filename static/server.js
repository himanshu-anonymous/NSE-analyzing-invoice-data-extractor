document.addEventListener("DOMContentLoaded", function() {
  const sendButton = document.getElementById('send-btn');
  const inputField = document.getElementById('chat-input');
  const chatMessages = document.getElementById('chat-messages');

  async function fetchStockData() {
      const stockSymbols = document.getElementById("stockSymbols").value;
      const stockSymbolsArray = stockSymbols.split(",").map(symbol => symbol.trim());

      try {
          // Send request to FastAPI backend
          const response = await fetch("http://localhost:8000/fetch-stocks", {
              method: "POST",
              headers: {
                  "Content-Type": "application/json"
              },
              body: JSON.stringify({ stocks: stockSymbolsArray })
          });

          const data = await response.json();

          if (data.data) {
              // Clear any previous data
              const stockDataList = document.getElementById("stockDataList");
              stockDataList.innerHTML = "";

              // Display each stock data in the list
              data.data.forEach(stock => {
                  const stockItem = document.createElement("li");
                  stockItem.textContent = `${stock.symbol}: $${stock.price} | PE Ratio: ${stock.pe_ratio}`;
                  stockDataList.appendChild(stockItem);
              });
          } else {
              alert("No stock data found or there was an error.");
          }
      } catch (error) {
          console.error("Error fetching stock data:", error);
          alert("There was an error fetching the stock data.");
      }
  }

  sendButton.addEventListener('click', function() {
      const inputMessage = inputField.value.trim();

      if (inputMessage === '') {
          return;
      }
    const symbol = document.getElementById("symbol").value.trim().toUpperCase();
console.log(symbol);  // Add this to debug the symbol


      appendMessage('You: ' + inputMessage, 'user');
      inputField.value = '';
      const botResponse = getBotResponse(inputMessage);

      setTimeout(function() {
          appendMessage('AI: ' + botResponse, 'bot');
      }, 500);
  });

  function appendMessage(message, sender) {
      const messageDiv = document.createElement('div');
      messageDiv.classList.add('chat-message');
      messageDiv.classList.add(sender);
      messageDiv.textContent = message;
      chatMessages.appendChild(messageDiv);
      chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function getBotResponse(userInput) {
      userInput = userInput.toLowerCase();

      if (userInput.includes('hello') || userInput.includes('hi')) {
          return "Hello! How can I assist you today?";
      }

      if (userInput.includes('stock') || userInput.includes('investment')) {
          return "Sure! What stocks are you interested in?";
      }

      if (userInput.includes('help')) {
          return "I can help with stock data, setting goals, and answering investment queries.";
      }

      if (userInput.includes('bye')) {
          return "Goodbye! Feel free to reach out anytime.";
      }

      return "Sorry, I didn't understand that. Can you please rephrase?";
  }

  // Hook to fetch stock data when the button is clicked
  document.querySelector("button").addEventListener('click', fetchStockData);
});
