import streamlit as st
import requests

KERALA_DISTRICTS = {
    "Palakkad": (10.7867, 76.6548),
    "Thrissur": (10.5276, 76.2144),
    "Ernakulam": (9.9816, 76.2999),
    "Kozhikode": (11.2588, 75.7804),
    "Wayanad": (11.6854, 76.1310),
    "Alappuzha": (9.4981, 76.3388),
    "Kottayam": (9.5916, 76.5222),
    "Idukki": (9.8494, 76.9806),
    "Malappuram": (11.0732, 76.0740),
    "Kannur": (11.8745, 75.3704),
    "Kasaragod": (12.5102, 74.9852),
    "Kollam": (8.8932, 76.6141),
    "Pathanamthitta": (9.2648, 76.7870),
    "Thiruvananthapuram": (8.5241, 76.9366)
}

def geocode_location(location_name: str):
    """Geocode any Kerala village, town, or panchayat via Open-Meteo Geocoding."""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={requests.utils.quote(location_name)}&count=1&language=en&format=json"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results")
            if results and len(results) > 0:
                item = results[0]
                return {
                    "name": item.get("name"),
                    "admin1": item.get("admin1", "Kerala"),
                    "lat": item.get("latitude"),
                    "lon": item.get("longitude")
                }
    except Exception:
        pass
    return None

def auto_detect_ip_location():
    """Detect approximate live location from IP."""
    try:
        resp = requests.get("https://ipapi.co/json/", timeout=4)
        if resp.status_code == 200:
            d = resp.json()
            return {
                "name": f"{d.get('city', 'Kerala')}, {d.get('region', '')}",
                "lat": float(d.get('latitude', 10.7867)),
                "lon": float(d.get('longitude', 76.6548))
            }
    except Exception:
        pass
    return None

def fetch_weather(lat: float, lon: float):
    """Fetch high-resolution hourly and current weather metrics."""
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,cloud_cover,wind_speed_10m,wind_direction_10m"
        "&hourly=precipitation_probability,precipitation,temperature_2m"
        "&daily=precipitation_sum,precipitation_probability_max,temperature_2m_max,temperature_2m_min"
        "&timezone=auto"
    )
    try:
        resp = requests.get(url, timeout=6)
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return None

def main():
    lang = st.session_state.get('language', 'English')
    is_mal = (lang == "മലയാളം")

    if is_mal:
        st.title("🌦️ തത്സമയ കാലാവസ്ഥ & കാർഷിക കർമ്മപദ്ധതി")
        st.write("നിങ്ങളുടെ കൃഷിയിടത്തിന്റെ കൃത്യമായ ലൊക്കേഷൻ കണ്ടെത്തി തത്സമയ കാലാവസ്ഥാ വിവരങ്ങളും കർഷകർക്കുള്ള അടിയന്തര നിർദ്ദേശങ്ങളും അറിയുക.")
    else:
        st.title("🌦️ Hyper-Local Weather & Farm Advisory")
        st.write("Get real-time weather at your exact farm location with actionable agronomic advisories for spraying, irrigation, and harvesting.")

    # Location Selector
    loc_col1, loc_col2 = st.columns([2, 1])
    
    with loc_col1:
        search_query = st.text_input(
            "🔍 " + ("നിങ്ങളുടെ ഗ്രാമം / പഞ്ചായത്ത് / നഗരം തിരയുക:" if is_mal else "Search Village / Panchayat / Town:"),
            placeholder="e.g. Pattambi, Chittur, Kuttanad, Sulthan Bathery, Aluva, Nedumangad..."
        )
    
    with loc_col2:
        st.write("")
        st.write("")
        detect_btn = st.button("📍 " + ("എന്റെ ലൊക്കേഷൻ കണ്ടെത്തുക (Auto-Detect)" if is_mal else "Detect My Live GPS/IP"), type="secondary")

    # Determine Coordinates
    target_lat, target_lon = None, None
    location_title = ""

    if search_query:
        geo = geocode_location(search_query)
        if geo:
            target_lat, target_lon = geo["lat"], geo["lon"]
            location_title = f"{geo['name']}, {geo.get('admin1', 'Kerala')}"
            st.success(f"📍 {'കണ്ടെത്തിയ സ്ഥലം:' if is_mal else 'Location Identified:'} **{location_title}** (Lat: {target_lat:.4f}, Lon: {target_lon:.4f})")
        else:
            st.warning("ഈ സ്ഥലം കണ്ടെത്താനായില്ല. താഴെയുള്ള ജില്ലാ പട്ടിക ഉപയോഗിക്കുക." if is_mal else "Could not resolve exact coordinates. Falling back to district location.")
            
    elif detect_btn:
        with st.spinner("ലൊക്കേഷൻ കണ്ടെത്തുന്നു..." if is_mal else "Detecting live location..."):
            auto_loc = auto_detect_ip_location()
            if auto_loc:
                target_lat, target_lon = auto_loc["lat"], auto_loc["lon"]
                location_title = auto_loc["name"]
                st.success(f"📍 {'തത്സമയ ലൊക്കേഷൻ:' if is_mal else 'Live Detected Location:'} **{location_title}**")
            else:
                st.info("ഓട്ടോ-ഡിറ്റക്ഷൻ പരാജയപ്പെട്ടു, സ്ഥിരം ജില്ല ലഭ്യമാക്കുന്നു." if is_mal else "Auto-detect timed out, using selected district.")

    # Fallback to selected district
    if target_lat is None or target_lon is None:
        sel_district = st.session_state.get('district', 'Palakkad')
        target_lat, target_lon = KERALA_DISTRICTS.get(sel_district, (10.7867, 76.6548))
        location_title = f"{sel_district} District, Kerala"

    # Fetch Weather Data
    weather_data = fetch_weather(target_lat, target_lon)

    if not weather_data:
        st.error("കാലാവസ്ഥാ വിവരങ്ങൾ ശേഖരിക്കാൻ സാധിച്ചില്ല. ദയവായി അല്പം കഴിഞ്ഞ് വീണ്ടും ശ്രമിക്കുക." if is_mal else "Failed to retrieve weather data from meteorological service.")
        return

    current = weather_data.get("current", {})
    daily = weather_data.get("daily", {})
    hourly = weather_data.get("hourly", {})

    temp = current.get("temperature_2m", 28.0)
    feels_like = current.get("apparent_temperature", temp)
    humidity = current.get("relative_humidity_2m", 75)
    precip_now = current.get("precipitation", 0.0)
    wind_speed = current.get("wind_speed_10m", 8.0)
    cloud_cover = current.get("cloud_cover", 40)

    # 24h forecast summary
    precip_prob_max = daily.get("precipitation_probability_max", [0])[0] if daily.get("precipitation_probability_max") else 10
    precip_sum_today = daily.get("precipitation_sum", [0.0])[0] if daily.get("precipitation_sum") else 0.0

    st.markdown("---")

    # Colorful Metrics Row
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("🌡️ " + ("താപനില" if is_mal else "Temperature"), f"{temp} °C", f"Feels {feels_like}°C")
    with m2:
        st.metric("💧 " + ("ഈർപ്പം" if is_mal else "Humidity"), f"{humidity} %", "Relative")
    with m3:
        st.metric("🌧️ " + ("മഴ സാധ്യത" if is_mal else "Rain Probability"), f"{precip_prob_max} %", f"{precip_sum_today} mm forecast")
    with m4:
        st.metric("💨 " + ("കാറ്റിന്റെ വേഗത" if is_mal else "Wind Speed"), f"{wind_speed} km/h", "At 10m height")
    with m5:
        st.metric("☁️ " + ("മേഘാവൃതത" if is_mal else "Cloud Cover"), f"{cloud_cover} %", "Overcast" if cloud_cover > 70 else "Partly Cloudy")

    st.markdown("---")

    # Agronomic Farmer Advisory Section
    st.subheader("🌾 " + ("കർഷകർക്കായുള്ള തത്സമയ കാലാവസ്ഥാ നിർദ്ദേശങ്ങൾ (Farm Advisory)" if is_mal else "Actionable Agronomic Advisories for Farmers"))

    col_adv1, col_adv2 = st.columns(2)

    with col_adv1:
        # 1. Spraying Advisory
        with st.container(border=True):
            st.markdown("#### 🧪 " + ("കീടനാശിനി / കുമിൾനാശിനി തളിക്കൽ (Spraying Window)" if is_mal else "Spraying Window Advisory"))
            if precip_prob_max > 40 or precip_sum_today > 1.0:
                st.error("❌ **" + ("ഇന്ന് മരുന്ന് തളിക്കുന്നത് ഒഴിവാക്കുക" if is_mal else "DO NOT SPRAY TODAY") + "**")
                st.write(
                    "ഇന്ന് മഴയ്ക്ക് ഉയർന്ന സാധ്യതയുള്ളതിനാൽ ഇലകളിൽ തളിക്കുന്ന മരുന്നുകൾ കഴുകിപ്പോകാനും പാഴാകാനും സാധ്യതയുണ്ട്." if is_mal else
                    "High rain probability (>40%). Foliar sprays will be washed off, reducing chemical efficacy and causing runoff."
                )
            elif wind_speed > 16.0:
                st.warning("⚠️ **" + ("ശക്തമായ കാറ്റ് - സൂക്ഷിക്കുക" if is_mal else "HIGH WIND DRIFT RISK") + "**")
                st.write(
                    "കാറ്റിന്റെ വേഗത 16 കി.മീ/മണിക്കൂറിൽ കൂടുതലായതിനാൽ സ്പ്രേ ചെയ്യുമ്പോൾ മരുന്ന് സമീപത്തെ പറമ്പുകളിലേക്ക് കാറ്റിൽ പാറിപ്പോകാൻ ഇടയുണ്ട്." if is_mal else
                    "Wind speed exceeds 16 km/h. High spray drift risk to non-target crops. Wait for calm early morning hours."
                )
            else:
                st.success("✅ **" + ("മരുന്ന് തളിക്കാൻ അനുകൂല സമയം" if is_mal else "OPTIMAL SPRAYING WINDOW") + "**")
                st.write(
                    "അനുകൂലമായ കാലാവസ്ഥ. രാവിലെയോ വൈകുന്നേരമോ ബോർഡോ മിശ്രിതമോ സ്യൂഡോമോണസോ തളിക്കാവുന്നതാണ്." if is_mal else
                    "Calm winds and low rain probability. Early morning or late afternoon is ideal for applying fungicides or bio-agents."
                )

        # 2. Irrigation Planning
        with st.container(border=True):
            st.markdown("#### 💧 " + ("നനയ്ക്കൽ നിർദ്ദേശം (Irrigation Advisory)" if is_mal else "Irrigation Planning"))
            if precip_sum_today > 5.0:
                st.info("🌧️ **" + ("നനയ്ക്കൽ ആവശ്യമില്ല (Skip Irrigation)" if is_mal else "SKIP IRRIGATION TODAY") + "**")
                st.write(
                    "ഇന്ന് പ്രതീക്ഷിക്കുന്ന മഴ മണ്ണിന് ആവശ്യമായ ഈർപ്പം നൽകും. പമ്പ് ചെയ്യേണ്ടതില്ല; വൈദ്യുതിയും വെള്ളവും ലാഭിക്കാം." if is_mal else
                    "Forecasted rainfall will replenish root zone soil moisture. Skip motorized pumping to conserve power and water."
                )
            elif temp > 33.0 and humidity < 60:
                st.warning("☀️ **" + ("നന വർദ്ധിപ്പിക്കുക (Intense Evaporation)" if is_mal else "INCREASE IRRIGATION") + "**")
                st.write(
                    "ഉയർന്ന ചൂടും കുറഞ്ഞ ഈർപ്പവും ഉള്ളതിനാൽ വാഴ, പച്ചക്കറികൾ എന്നിവയ്ക്ക് വൈകുന്നേരം കൂടുതൽ നന നൽകുക. ചുവട്ടിൽ കരിയില പുതയിടുക." if is_mal else
                    "High heat and low humidity trigger high evapotranspiration. Provide deep irrigation in the evening and maintain thick mulch."
                )
            else:
                st.success("✅ **" + ("സാധാരണ നന രീതി തുടരുക" if is_mal else "STANDARD IRRIGATION REGIME") + "**")
                st.write(
                    "മണ്ണിലെ ഈർപ്പത്തിനനുസരിച്ച് സാധാരണ നന നൽകുക." if is_mal else
                    "Normal soil moisture retention. Follow scheduled drip or basin irrigation for your crop."
                )

    with col_adv2:
        # 3. Fertilizer Broadcasting
        with st.container(border=True):
            st.markdown("#### 🌾 " + ("വളപ്രയോഗ സമയം (Fertilizer Broadcasting)" if is_mal else "Fertilizer Application Advisory"))
            if precip_prob_max > 50:
                st.warning("⚠️ **" + ("രാസവളം വിതറുന്നത് മാറ്റിവെക്കുക" if is_mal else "POSTPONE FERTILIZER BROADCASTING") + "**")
                st.write(
                    "കനത്ത മഴയിൽ യൂറിയയും പൊട്ടാഷും ഒലിച്ചുപോകാൻ (leaching) സാധ്യതയുണ്ട്. മഴ ശമിച്ച ശേഷം മാത്രം വളമിടുക." if is_mal else
                    "Heavy rain will cause surface runoff and leaching of soluble Urea and Potash. Postpone broadcasting until rain clears."
                )
            else:
                st.success("✅ **" + ("വളപ്രയോഗത്തിന് അനുയോജ്യം" if is_mal else "SAFE FOR FERTILIZER APPLICATION") + "**")
                st.write(
                    "മണ്ണിൽ നേരിയ ഈർപ്പമുള്ളപ്പോൾ അടിവളവും മേൽവളവും ചേർത്ത് മണ്ണിട്ട് മൂടുക." if is_mal else
                    "Soil moisture conditions are receptive for incorporating compost and split NPK doses."
                )

        # 4. Storm & Propping Warning for Banana / Rubber
        with st.container(border=True):
            st.markdown("#### 🌴 " + ("വാഴ / റബ്ബർ കാറ്റിൽ സംരക്ഷണം (Propping Alert)" if is_mal else "Crop Propping & Storm Alert"))
            if wind_speed > 20.0:
                st.error("🚨 **" + ("ശക്തമായ കാറ്റ് മുന്നറിയിപ്പ് - വാഴകൾക്ക് താങ്ങ് നൽകുക" if is_mal else "GALE WARNING: PROP BANANA PLANTS") + "**")
                st.write(
                    "കാറ്റിന്റെ വേഗത കൂടുതലായതിനാൽ കുലച്ച വാഴകൾ ഒടിഞ്ഞു വീഴാതിരിക്കാൻ മുളങ്കമ്പുകൾ കൊണ്ട് ഉടൻ താങ്ങ് നൽകുക." if is_mal else
                    "Gusty winds (>20 km/h) can cause pseudostem breakage in bunching banana plants. Anchor with double bamboo props immediately."
                )
            else:
                st.info("🍃 **" + ("കാറ്റ് ശാന്തമാണ്" if is_mal else "MILD BREEZE CONDITIONS") + "**")
                st.write(
                    "കാറ്റിന്റെ ആഘാതം സാധാരണ നിലയിലാണ്. എങ്കിലും കനത്ത കുലയുള്ള വാഴകൾക്ക് മുൻകരുതലായി താങ്ങ് കൊടുക്കുന്നത് നല്ലതാണ്." if is_mal else
                    "Normal wind velocity. Ensure routine staking for high-yield bunching plants as a preventive measure."
                )

    st.caption("Data Source: Open-Meteo High Resolution Weather API | Updated: Live Real-time")
