function fetchPrices() {
    fetch('http://127.0.0.1:5000/prices')
      .then(response => response.json())
      .then(data => {
        document.getElementById('min-price').textContent = data.min_price;
        document.getElementById('max-price').textContent = data.max_price;
      })
      .catch(error => console.error('Erro ao buscar preços:', error));
  }
  
  // Buscar preços quando a página carrega
  window.onload = fetchPrices;
  