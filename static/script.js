// Function to fetch stock data based on symbol and display it
async function getStockData() {
    const symbol = document.getElementById("symbol").value.trim().toUpperCase();

    if (!symbol) {
        alert("Please enter a stock symbol.");
        return;
    }

    try {
        const response = await fetch(`/fetch-single-stock?symbol=${symbol}`);

        if (!response.ok) {
            throw new Error('Failed to fetch stock data');
        }

        const data = await response.json();
        console.log("Fetched Stock Data: ", data);

        if (data.error) {
            throw new Error(data.error);
        }

        const stock = data.data;
        const stockHtml = `
            <div class="stock animate-text">
                <h2>${symbol} - Stock Data</h2>
                <p><strong>Price:</strong> $${stock.price}</p>
                <p><strong>PE Ratio:</strong> ${stock.pe_ratio}</p>
            </div>
        `;

        document.getElementById("stockData").innerHTML = stockHtml;
    } catch (error) {
        console.error("Error fetching stock data:", error);

        const dummyData = {
            symbol: "DUMMY",
            price: 100.00,
            pe_ratio: 15.5
        };

        const stockHtml = `
            <div class="stock animate-text">
                <h2>${dummyData.symbol} - Stock Data (Dummy Data)</h2>
                <p><strong>Price:</strong> $${dummyData.price}</p>
                <p><strong>PE Ratio:</strong> ${dummyData.pe_ratio}</p>
            </div>
        `;

        document.getElementById("stockData").innerHTML = stockHtml;
    }
}

// Fetch suggested stock data from the backend
async function fetchSuggestedStockData() {
    try {
        const response = await fetch("/fetch-suggested-stocks");

        if (!response.ok) {
            throw new Error('Failed to fetch suggested stocks');
        }

        const data = await response.json();
        console.log("Suggested Stock Data: ", data);

        if (data.error) {
            throw new Error(data.error);
        }

        const stockDataList = document.getElementById("stockDataList");
        stockDataList.innerHTML = "";

        data.data.forEach(stock => {
            const stockCard = document.createElement("div");
            stockCard.classList.add("stock-card", "animate-text");

            const stockSymbol = document.createElement("h4");
            stockSymbol.textContent = stock.symbol;

            const stockPrice = document.createElement("p");
            stockPrice.textContent = `Price: $${stock.price}`;

            const peRatio = document.createElement("p");
            peRatio.textContent = `PE Ratio: ${stock.pe_ratio}`;

            stockCard.appendChild(stockSymbol);
            stockCard.appendChild(stockPrice);
            stockCard.appendChild(peRatio);

            stockDataList.appendChild(stockCard);
        });
    } catch (error) {
        console.error("Error fetching suggested stock data:", error);

        const dummySuggestedData = [
            { symbol: "DUMMY1", price: 100.00, pe_ratio: 12.5 },
            { symbol: "DUMMY2", price: 150.00, pe_ratio: 10.0 },
        ];

        const stockDataList = document.getElementById("stockDataList");
        stockDataList.innerHTML = "";

        dummySuggestedData.forEach(stock => {
            const stockCard = document.createElement("div");
            stockCard.classList.add("stock-card", "animate-text");

            const stockSymbol = document.createElement("h4");
            stockSymbol.textContent = stock.symbol;

            const stockPrice = document.createElement("p");
            stockPrice.textContent = `Price: $${stock.price}`;

            const peRatio = document.createElement("p");
            peRatio.textContent = `PE Ratio: ${stock.pe_ratio}`;

            stockCard.appendChild(stockSymbol);
            stockCard.appendChild(stockPrice);
            stockCard.appendChild(peRatio);

            stockDataList.appendChild(stockCard);
        });
    }
}

window.onload = function () {
    fetchSuggestedStockData();
};
