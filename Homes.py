import math
import pandas as pd
from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# ---------------------------------------------------------------------------
# 1. Nairobi Short-Stay Raw Dataset (Pandas DataFrame Source)
# ---------------------------------------------------------------------------
RAW_LISTINGS = [
    {"id": 1, "name": "Westlands Cozy Studio Suite", "desc": "Close to malls, secure parking & balcony", "neighborhood": "Westlands", "price": 3800, "lat": -1.2676, "lng": 36.8108, "img": "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=600&q=80"},
    {"id": 2, "name": "Kilimani Executive 2BR Airbnb", "desc": "High-speed WiFi, Pool, & Skyline View", "neighborhood": "Kilimani", "price": 5500, "lat": -1.2902, "lng": 36.7821, "img": "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=600&q=80"},
    {"id": 3, "name": "Karen Luxury Garden Villa", "desc": "Serene environment, lush garden, and private security", "neighborhood": "Karen", "price": 12500, "lat": -1.3200, "lng": 36.7050, "img": "https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=600&q=80"},
    {"id": 4, "name": "Kileleshwa Terrace 1BR Suite", "desc": "Quiet residential street, modern kitchen & Gym", "neighborhood": "Kileleshwa", "price": 4800, "lat": -1.2815, "lng": 36.7912, "img": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=600&q=80"},
    {"id": 5, "name": "Lavington Heights Duplex", "desc": "Spacious balcony, backup generator & rooftop lounge", "neighborhood": "Lavington", "price": 9500, "lat": -1.2789, "lng": 36.7678, "img": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=600&q=80"},
    {"id": 6, "name": "CBD City Center Penthouse", "desc": "Walking distance to office hubs, high security", "neighborhood": "CBD", "price": 4200, "lat": -1.2840, "lng": 36.8230, "img": "https://images.unsplash.com/photo-1536376072261-38c75010e6c9?auto=format&fit=crop&w=600&q=80"},
    {"id": 7, "name": "Gigiri Diplomatic Residence", "desc": "Near UN HQ, diplomatic security & private garden", "neighborhood": "Gigiri", "price": 16000, "lat": -1.2330, "lng": 36.8150, "img": "https://images.unsplash.com/photo-1505691938895-1758d7feb511?auto=format&fit=crop&w=600&q=80"},
    {"id": 8, "name": "Kilimani Poolside Studio", "desc": "Heated rooftop pool, gym, fast WiFi", "neighborhood": "Kilimani", "price": 4500, "lat": -1.2940, "lng": 36.7880, "img": "https://images.unsplash.com/photo-1554995207-c18c203602cb?auto=format&fit=crop&w=600&q=80"},
    {"id": 9, "name": "Westlands Skyline View 2BR", "desc": "Panic room, high floor, panoramic city views", "neighborhood": "Westlands", "price": 8200, "lat": -1.2630, "lng": 36.8020, "img": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=600&q=80"}
]

# Convert dataset into Pandas DataFrame
df = pd.DataFrame(RAW_LISTINGS)

# Uber Fare Calculation Algorithm
def calculate_uber_fare(lat, lng):
    cbd_lat, cbd_lng = -1.286389, 36.817223
    dlat = (lat - cbd_lat) * math.pi / 180
    dlng = (lng - cbd_lng) * math.pi / 180
    a = math.sin(dlat / 2) ** 2 + math.cos(cbd_lat * math.pi / 180) * math.cos(lat * math.pi / 180) * math.sin(dlng / 2) ** 2
    dist = 6371 * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))
    fare = round(250 + (dist * 70))
    uber_link = f"https://m.uber.com/ul/?action=setPickup&dropoff[latitude]={lat}&dropoff[longitude]={lng}"
    return {"dist": round(dist, 1), "fare": fare, "link": uber_link}

# ---------------------------------------------------------------------------
# 2. HTML Frontend Template Embedded inside Python
# ---------------------------------------------------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nairobi Star Homes | Python Flask Directory</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Leaflet Maps -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

    <style>
        body {
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E72 100%);
            min-height: 100vh;
            color: #1A0D12;
            font-family: system-ui, -apple-system, sans-serif;
        }
        .glass-card {
            background: rgba(26, 13, 18, 0.92);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 180, 162, 0.3);
            color: #FFF0ED;
        }
        .glass-pill {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.25);
        }
        .glass-pill.active {
            background: #FFF0ED;
            color: #9E2A2B;
            font-weight: 700;
        }
        #bottom-map {
            height: 320px;
            width: 100%;
            border-radius: 16px;
        }
    </style>
</head>
<body class="p-3 md:p-6 pb-20">
    <!-- Header -->
    <header class="max-w-xl mx-auto mb-4 flex justify-between items-center glass-card p-4 rounded-2xl shadow-xl">
        <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-400 to-rose-500 flex items-center justify-center text-white shadow-lg">
                <i class="fa-solid fa-house-flag text-lg"></i>
            </div>
            <div>
                <h1 class="text-lg font-bold text-white tracking-wide">Nairobi Star Homes</h1>
                <p class="text-[11px] text-rose-200">Pandas-Powered Short-Stay Directory</p>
            </div>
        </div>
        <span class="px-3 py-1 bg-emerald-500/20 border border-emerald-400 text-emerald-400 rounded-full text-[10px] font-bold flex items-center gap-1.5">
            <i class="fa-brands fa-python"></i> Flask Engine Active
        </span>
    </header>

    <!-- Main Section -->
    <main class="max-w-xl mx-auto space-y-4">
        <div class="glass-card p-4 rounded-2xl space-y-3">
            <div class="flex justify-between items-center text-xs">
                <span class="text-rose-200 flex items-center gap-1.5">
                    <i class="fa-solid fa-location-crosshairs text-amber-400"></i> Location Filter: Nairobi
                </span>
                <span id="engine-status" class="px-2.5 py-1 bg-emerald-500/30 text-emerald-300 font-extrabold rounded-lg text-[10px] flex items-center gap-1">
                    <i class="fa-solid fa-check text-emerald-400"></i> Python API Connected
                </span>
            </div>
            
            <!-- Neighborhood Filters -->
            <div class="flex gap-2 overflow-x-auto text-xs no-scrollbar pt-1" id="hub-pills">
                <button onclick="filterHub('All', this)" class="glass-pill active px-4 py-1.5 rounded-full whitespace-nowrap">All Stays</button>
                <button onclick="filterHub('Kilimani', this)" class="glass-pill px-4 py-1.5 rounded-full text-white whitespace-nowrap">Kilimani</button>
                <button onclick="filterHub('Westlands', this)" class="glass-pill px-4 py-1.5 rounded-full text-white whitespace-nowrap">Westlands</button>
                <button onclick="filterHub('Kileleshwa', this)" class="glass-pill px-4 py-1.5 rounded-full text-white whitespace-nowrap">Kileleshwa</button>
                <button onclick="filterHub('Lavington', this)" class="glass-pill px-4 py-1.5 rounded-full text-white whitespace-nowrap">Lavington</button>
                <button onclick="filterHub('Karen', this)" class="glass-pill px-4 py-1.5 rounded-full text-white whitespace-nowrap">Karen</button>
                <button onclick="filterHub('CBD', this)" class="glass-pill px-4 py-1.5 rounded-full text-white whitespace-nowrap">CBD</button>
            </div>
        </div>

        <!-- Listings Grid -->
        <div id="listings-grid" class="space-y-4"></div>

        <!-- Map -->
        <div class="glass-card p-4 rounded-2xl space-y-3 mt-6">
            <div class="flex justify-between items-center text-xs">
                <h3 class="font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-map-location-dot text-amber-400"></i>
                    Nairobi Interactive Neighborhood Map
                </h3>
                <span class="text-[10px] text-rose-200">Live Pins</span>
            </div>
            <div id="bottom-map"></div>
        </div>
    </main>

    <!-- M-Pesa Checkout Modal -->
    <div id="mpesa-modal" class="fixed inset-0 bg-black/80 backdrop-blur-md hidden z-50 flex items-center justify-center p-4">
        <div class="glass-card w-full max-w-sm p-5 rounded-2xl border border-emerald-400/40 space-y-4">
            <div class="flex justify-between items-center border-b border-rose-400/20 pb-3">
                <h3 class="text-sm font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-mobile-screen text-emerald-400"></i>
                    M-Pesa Direct Checkout
                </h3>
                <button onclick="closeMpesaModal()" class="text-rose-300 text-xs"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div class="space-y-1.5 text-xs text-rose-200">
                <p id="mpesa-prop-name" class="font-bold text-white text-sm"></p>
                <div class="flex justify-between pt-1">
                    <span>Nightly Rate:</span>
                    <span id="mpesa-rate" class="font-bold text-emerald-400">Ksh 0</span>
                </div>
            </div>
            <div class="space-y-2 pt-2">
                <label class="block text-[11px] text-rose-200">Safaricom Phone Number</label>
                <input type="tel" id="mpesa-phone" placeholder="2547XXXXXXXX" value="254795353042" class="w-full bg-black/60 border border-rose-400/30 rounded-xl px-3 py-2 text-xs text-white">
                <button onclick="simulateSTKPush()" class="w-full py-2.5 bg-emerald-500 hover:bg-emerald-600 text-white font-bold rounded-xl text-xs transition">
                    Trigger STK Push Prompt
                </button>
            </div>
        </div>
    </div>

    <script>
        const WA_NUMBER = "254795353042";
        let bottomMap = null;

        async function fetchListings(hub = "All") {
            const res = await fetch(`/api/filter?hub=${encodeURIComponent(hub)}`);
            const listings = await res.json();
            
            let html = "";
            listings.forEach((row, idx) => {
                html += `
                <div class="glass-card rounded-2xl overflow-hidden shadow-lg border border-rose-400/20 p-4 space-y-3">
                    <div class="relative">
                        <img src="${row.img}" class="w-full h-44 object-cover rounded-xl">
                        <span class="absolute top-2 left-2 bg-amber-500 text-black text-[10px] font-extrabold px-2.5 py-1 rounded-md">
                            Listing #${idx + 1}
                        </span>
                        <span class="absolute top-2 right-2 bg-emerald-500 text-white text-[11px] font-bold px-2.5 py-1 rounded-md shadow">
                            Ksh ${row.price.toLocaleString()} / night
                        </span>
                    </div>
                    <div>
                        <h3 class="font-bold text-base text-white">${row.name}</h3>
                        <p class="text-xs text-rose-200">${row.desc}</p>
                        <p class="text-[11px] text-rose-300 mt-1"><i class="fa-solid fa-location-dot text-rose-400 mr-1"></i>${row.neighborhood}, Nairobi</p>
                    </div>
                    <div class="grid grid-cols-2 gap-2 pt-1">
                        <button onclick="openMpesaModalForListing('${row.name}', ${row.price})" class="py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs font-bold flex items-center justify-center gap-1.5 transition">
                            <i class="fa-solid fa-mobile-screen"></i> M-Pesa
                        </button>
                        <button onclick="triggerWA('${row.name}', ${row.price}, '${row.neighborhood}')" class="py-2.5 bg-emerald-500 hover:bg-emerald-600 text-white rounded-xl text-xs font-bold flex items-center justify-center gap-1.5 transition">
                            <i class="fa-brands fa-whatsapp"></i> Chat Host
                        </button>
                    </div>
                </div>
                `;
            });
            document.getElementById("listings-grid").innerHTML = html;
        }

        function filterHub(hub, btn) {
            document.querySelectorAll('#hub-pills button').forEach(b => {
                b.classList.remove('active', 'text-white');
                b.classList.add('text-white');
            });
            btn.classList.add('active');
            btn.classList.remove('text-white');
            fetchListings(hub);
        }

        function triggerWA(name, price, loc) {
            let text = `Hello Nairobi Star Homes! I'm interested in booking ${name} in ${loc} at Ksh ${price}/night.`;
            window.top.location.href = `https://api.whatsapp.com/send?phone=${WA_NUMBER}&text=${encodeURIComponent(text)}`;
        }

        function openMpesaModalForListing(name, price) {
            document.getElementById('mpesa-prop-name').innerText = name;
            document.getElementById('mpesa-rate').innerText = `Ksh ${price.toLocaleString()} / night`;
            document.getElementById('mpesa-modal').classList.remove('hidden');
        }

        function simulateSTKPush() {
            const phone = document.getElementById('mpesa-phone').value;
            alert(`M-Pesa STK Push prompt sent to ${phone}! Check your phone to complete booking.`);
            closeMpesaModal();
        }

        function closeMpesaModal() {
            document.getElementById('mpesa-modal').classList.add('hidden');
        }

        window.onload = function() {
            fetchListings('All');

            setTimeout(() => {
                bottomMap = L.map('bottom-map').setView([-1.286389, 36.817223], 12);
                L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png').addTo(bottomMap);
                
                const hubs = [
                    { name: "Kilimani Hub", lat: -1.2902, lng: 36.7821 },
                    { name: "Westlands Hub", lat: -1.2676, lng: 36.8108 },
                    { name: "Karen Hub", lat: -1.3200, lng: 36.7050 },
                    { name: "Kileleshwa Hub", lat: -1.2815, lng: 36.7912 },
                    { name: "Lavington Hub", lat: -1.2789, lng: 36.7678 }
                ];
                
                hubs.forEach(h => {
                    L.marker([h.lat, h.lng]).addTo(bottomMap).bindPopup(`<b>${h.name}</b>`);
                });
            }, 300);
        };
    </script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# 3. Flask API Routes
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/filter", methods=["GET"])
def api_filter():
    hub = request.args.get("hub", "All")
    if hub != "All":
        filtered_df = df[df["neighborhood"] == hub]
    else:
        filtered_df = df.copy()
    
    return jsonify(filtered_df.to_dict(orient="records"))

# ---------------------------------------------------------------------------
# 4. Main Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
