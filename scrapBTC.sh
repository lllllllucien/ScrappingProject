# Récupérer les données de l'API
response=$(curl -s "https://api.bitget.com/api/v2/spot/market/tickers?symbol=BTCUSDT")

# Extraire les valeurs
open=$(echo "$response" | grep -o '"open":"[^"]*"' | cut -d':' -f2 | tr -d '"')
symbol=$(echo "$response" | grep -o '"symbol":"[^"]*"' | cut -d':' -f2 | tr -d '"')
high24h=$(echo "$response" | grep -o '"high24h":"[^"]*"' | cut -d':' -f2 | tr -d '"')
low24h=$(echo "$response" | grep -o '"low24h":"[^"]*"' | cut -d':' -f2 | tr -d '"')
lastPr=$(echo "$response" | grep -o '"lastPr":"[^"]*"' | cut -d':' -f2 | tr -d '"')
quoteVolume=$(echo "$response" | grep -o '"quoteVolume":"[^"]*"' | cut -d':' -f2 | tr -d '"')
time=$(echo "$response" | grep -o '"ts":"[^"]*"' | cut -d':' -f2 | tr -d '"')

# Afficher les valeurs en format JSON
echo "{\"timestamp\": \"$time\", \"open\": \"$open\", \"symbol\": \"$symbol\", \"high24h\": \"$high24h\", \"low24h\": \"$low24h\", \"lastPr\": \"$lastPr\", \"quoteVolume\": \"$quoteVolume\"}"
