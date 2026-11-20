import streamlit as st
import json
import os
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
POSTS_FILE = DATA_DIR / "community_posts.json"
CHATS_FILE = DATA_DIR / "farmer_chats.json"

DEFAULT_POSTS = [
    {
        "id": 1,
        "author": "Rajan Nair",
        "district": "Palakkad",
        "crop": "Paddy",
        "title": "Handling Brown Plant Hopper (ചാഴി) in Chittoor area",
        "message": "Spotted early BPH infestation in my Uma variety paddy field. Drained the standing water for 3 days and sprayed Beauveria bassiana (20g/L). Highly effective without harming beneficial spiders!",
        "date": "17-11-2026",
        "likes": 12
    },
    {
        "id": 2,
        "author": "Mary Varghese",
        "district": "Thrissur",
        "crop": "Banana",
        "title": "Nendran banana bunch cover with polythene sleeves",
        "message": "Using blue perforated plastic sleeves right after male bud removal has increased banana fruit grade significantly and prevented thrips scarring. Recommend fellow Thrissur farmers try this before monsoon.",
        "date": "16-11-2026",
        "likes": 19
    },
    {
        "id": 3,
        "author": "Shaji Kurian",
        "district": "Wayanad",
        "crop": "Pepper",
        "title": "Gandhakasala & Jeerakasala organic seed availability",
        "message": "I have about 50 kg of pure, certified organic Gandhakasala aromatic paddy seeds available for exchange or purchase near Mananthavady. Contact through Krishi Bhavan Wayanad group.",
        "date": "15-11-2026",
        "likes": 24
    }
]

DEFAULT_CHATS = {
    "Suresh Kumar (Palakkad)": {
        "crop": "Paddy (Uma Variety)",
        "avatar": "👨‍🌾",
        "online": True,
        "messages": [
            {"sender": "Suresh", "text": "Namaskaram Kishore! Did you start the second crop nursery in Alathur?", "time": "10:15 AM"},
            {"sender": "You", "text": "Namaskaram Suresh chetta, yes seeds sprouted yesterday. Planning to transplant in 20 days.", "time": "10:20 AM"},
            {"sender": "Suresh", "text": "Good. Remember to apply Pseudomonas in the nursery bed to prevent blast.", "time": "10:22 AM"}
        ]
    },
    "Mary Varghese (Thrissur)": {
        "crop": "Nendran Banana",
        "avatar": "👩‍🌾",
        "online": True,
        "messages": [
            {"sender": "Mary", "text": "Hello! How is the banana bunch formation this season?", "time": "Yesterday"},
            {"sender": "You", "text": "Bunches are heavy, used bamboo props against the strong winds as advised.", "time": "Yesterday"},
            {"sender": "Mary", "text": "Excellent! Make sure to cover bunches with blue perforated sleeves.", "time": "Yesterday"}
        ]
    },
    "Shaji Kurian (Wayanad)": {
        "crop": "Organic Black Pepper & Coffee",
        "avatar": "🧔",
        "online": False,
        "messages": [
            {"sender": "Shaji", "text": "Let me know if you need organic Trichoderma culture for pepper quick wilt.", "time": "2 days ago"},
            {"sender": "You", "text": "Yes Shaji, sending a parcel request through KVK Ambalavayal.", "time": "2 days ago"}
        ]
    },
    "Anil Kanthalloor (Idukki)": {
        "crop": "Apple & Garlic",
        "avatar": "🍎",
        "online": True,
        "messages": [
            {"sender": "Anil", "text": "Winter pruning for apples starting next week in Kanthalloor. Great chill hours this year!", "time": "09:30 AM"},
            {"sender": "You", "text": "Are you applying FYM during dormancy?", "time": "09:45 AM"},
            {"sender": "Anil", "text": "Yes, 25 kg FYM + rock phosphate per tree basin right now.", "time": "09:50 AM"}
        ]
    }
}

def load_posts():
    if not POSTS_FILE.exists():
        os.makedirs(POSTS_FILE.parent, exist_ok=True)
        with open(POSTS_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_POSTS, f, indent=2, ensure_ascii=False)
        return DEFAULT_POSTS
    try:
        with open(POSTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_POSTS

def save_posts(posts):
    with open(POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

def load_chats():
    if not CHATS_FILE.exists():
        os.makedirs(CHATS_FILE.parent, exist_ok=True)
        with open(CHATS_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CHATS, f, indent=2, ensure_ascii=False)
        return DEFAULT_CHATS
    try:
        with open(CHATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CHATS

def save_chats(chats):
    with open(CHATS_FILE, "w", encoding="utf-8") as f:
        json.dump(chats, f, indent=2, ensure_ascii=False)

KRISHI_BHAVAN_DIRECTORY = {
    "Palakkad": {
        "office": "Principal Agricultural Office, Palakkad",
        "phone": "0491-2505298",
        "address": "Civil Station, Palakkad - 678001",
        "kisan_mitra": "Kisan Call Centre: 1800-180-1551 (Toll-Free)"
    },
    "Thrissur": {
        "office": "Principal Agricultural Office, Thrissur",
        "phone": "0487-2331298",
        "address": "Civil Station, Ayyanthole, Thrissur - 680003",
        "kisan_mitra": "KAU Agricultural Technology Information Centre (ATIC): 0487-2371554"
    },
    "Ernakulam": {
        "office": "Principal Agricultural Office, Ernakulam",
        "phone": "0484-2422262",
        "address": "Civil Station, Kakkanad, Kochi - 682030",
        "kisan_mitra": "Kisan Call Centre: 1800-180-1551 (Toll-Free)"
    },
    "Wayanad": {
        "office": "Principal Agricultural Office, Wayanad",
        "phone": "04936-202288",
        "address": "Civil Station, Kalpetta, Wayanad - 673122",
        "kisan_mitra": "Regional Agricultural Research Station (RARS) Ambalavayal: 04936-260421"
    },
    "Idukki": {
        "office": "Principal Agricultural Office, Idukki",
        "phone": "04862-232231",
        "address": "Civil Station, Painavu, Idukki - 685603",
        "kisan_mitra": "Cardamom & High Altitude Research Station: 04868-272251"
    }
}

# Marketplace is stored in SQLite; other community tabs remain unchanged.
MARKET_DB = DATA_DIR / "marketplace.sqlite3"
DISTRICTS = ["Alappuzha", "Ernakulam", "Idukki", "Kannur", "Kasaragod", "Kollam", "Kottayam", "Kozhikode", "Malappuram", "Palakkad", "Pathanamthitta", "Thiruvananthapuram", "Thrissur", "Wayanad"]

def marketplace_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(MARKET_DB, timeout=15)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS listings (
        id TEXT PRIMARY KEY, owner_id TEXT NOT NULL, owner_name TEXT NOT NULL,
        item TEXT NOT NULL, category TEXT NOT NULL, listing_type TEXT NOT NULL,
        district TEXT NOT NULL, description TEXT NOT NULL,
        price REAL, unit TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'Available',
        created_at TEXT NOT NULL)""")
    conn.commit()
    return conn

def marketplace_page(is_mal):
    st.subheader("വിത്ത് & കാർഷിക ഉപകരണ കൈമാറ്റം" if is_mal else "Seed & Equipment Exchange")
    st.caption("കർഷകർ ചേർത്ത യഥാർത്ഥ ലിസ്റ്റിംഗുകൾ മാത്രം" if is_mal else "Listings posted by registered farmers. No sample advertisements.")
    user = st.session_state.get("user") or {}
    owner_id = str(user.get("username") or "")
    if not st.session_state.get("authenticated") or not owner_id:
        st.warning("Please log in to view and publish listings.")
        return
    owner_name = str(user.get("name") or "Farmer")
    with st.expander("പുതിയ ലിസ്റ്റിംഗ്" if is_mal else "Add a seed or equipment listing"):
        with st.form("marketplace_new_listing", clear_on_submit=True):
            item = st.text_input("ഇനത്തിന്റെ പേര് / Item name", max_chars=100)
            category = st.selectbox("Category", ["Seeds & Plants", "Farm Equipment", "Other Farm Resources"])
            listing_type = st.selectbox("Offer type", ["Sell", "Rent", "Exchange", "Give away"])
            district = st.selectbox("District", DISTRICTS, index=DISTRICTS.index(user.get("district")) if user.get("district") in DISTRICTS else 0)
            description = st.text_area("Description / quantity / condition", max_chars=1000)
            price_text = st.text_input("Price in ₹ (optional; required for selling/renting)", placeholder="e.g. 800")
            unit = st.selectbox("Price unit", ["per item", "per kg", "per day", "per hour", "per lot"])
            submitted = st.form_submit_button("Publish listing", type="primary")
            if submitted:
                try:
                    price = float(price_text) if price_text.strip() else None
                    if price is not None and (price < 0 or price > 100000000):
                        raise ValueError("Invalid price")
                except ValueError:
                    st.error("Enter a valid non-negative price.")
                else:
                    if not item.strip() or not description.strip():
                        st.error("Item name and description are required.")
                    elif listing_type in ("Sell", "Rent") and price is None:
                        st.error("A price is required for selling or renting.")
                    else:
                        with marketplace_connection() as conn:
                            conn.execute("INSERT INTO listings (id,owner_id,owner_name,item,category,listing_type,district,description,price,unit,status,created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (uuid.uuid4().hex,owner_id,owner_name,item.strip(),category,listing_type,district,description.strip(),price,unit,"Available",datetime.now().isoformat(timespec="seconds")))
                        st.success("Listing published!")
                        st.rerun()
    with marketplace_connection() as conn:
        rows = [dict(r) for r in conn.execute("SELECT * FROM listings ORDER BY created_at DESC").fetchall()]
    if not rows:
        st.info("No listings yet. Be the first farmer to add one!")
        return
    c1,c2,c3 = st.columns(3)
    with c1: search_term = st.text_input("Search items", key="market_search")
    with c2: filter_cat = st.selectbox("Category filter", ["All"] + ["Seeds & Plants", "Farm Equipment", "Other Farm Resources"], key="market_category")
    with c3: filter_dist = st.selectbox("District filter", ["All"] + DISTRICTS, key="market_district")
    mine = st.checkbox("Show only my listings", key="market_mine")
    for r in rows:
        if mine and r["owner_id"] != owner_id: continue
        if filter_cat != "All" and r["category"] != filter_cat: continue
        if filter_dist != "All" and r["district"] != filter_dist: continue
        if search_term and search_term.casefold() not in (r["item"] + " " + r["description"]).casefold(): continue
        if r["status"] != "Available" and not (mine and r["owner_id"] == owner_id): continue
        with st.container(border=True):
            st.markdown(f"#### {r['item']}")
            st.write(f"**{r['listing_type']}** · {r['district']} · **{r['status']}**")
            st.write(r["description"])
            if r["price"] is not None: st.write(f"**₹{r['price']:,.2f} {r['unit']}**")
            st.caption(f"Posted by {r['owner_name']} · {r['created_at'][:10]}")
            if r["owner_id"] == owner_id:
                new_status = st.selectbox("Availability", ["Available", "Unavailable"], index=0 if r["status"] == "Available" else 1, key="status_"+r["id"])
                a,b = st.columns(2)
                with a:
                    if st.button("Save status", key="save_"+r["id"]):
                        with marketplace_connection() as conn:
                            conn.execute("UPDATE listings SET status=? WHERE id=? AND owner_id=?", (new_status,r["id"],owner_id))
                        st.rerun()
                with b:
                    if st.button("Delete listing", key="delete_"+r["id"]):
                        with marketplace_connection() as conn:
                            conn.execute("DELETE FROM listings WHERE id=? AND owner_id=?", (r["id"],owner_id))
                        st.rerun()
            else:
                st.info("Contact the owner through Farmer Connect. Direct listing-to-chat linking is not yet implemented.")

def main():
    lang = st.session_state.get('language', 'English')
    is_mal = (lang == "മലയാളം")

    if is_mal:
        st.title("👥 കർഷക കൂട്ടായ്മ & പേഴ്സണൽ ചാറ്റ് (Farmer Connect & Chat)")
        st.write("കർഷക സുഹൃത്തുക്കളുമായി നേരിട്ട് ചാറ്റ് ചെയ്യുക, സംശയങ്ങൾ ചോദിക്കുക, നാടൻ വിത്തുകൾ കൈമാറുക.")
        tab1_name = "💬 കർഷക സുഹൃത്തുക്കളുമായുള്ള ചാറ്റ് (Direct 1-on-1 Chat)"
        tab2_name = "📢 പൊതു കർഷക ചർച്ചാവേദി (Community Board)"
        tab3_name = "വിത്ത് & യന്ത്രങ്ങൾ (Seed Exchange)"
        tab4_name = "🏛️ കൃഷിഭവൻ ഡയറക്ടറി (Directory)"
    else:
        st.title("👥 Farmer Connect & Direct Peer Messaging")
        st.write("Chat directly 1-on-1 with nearby farmers, share photos, seek peer advice, and discover farming groups.")
        tab1_name = "💬 Direct 1-on-1 Farmer Chat"
        tab2_name = "📢 Public Community Forum"
        tab3_name = "Seed & Equipment Exchange"
        tab4_name = "🏛️ Krishi Bhavan Directory"

    tab1, tab2, tab3, tab4 = st.tabs([tab1_name, tab2_name, tab3_name, tab4_name])

    # 1. DIRECT 1-ON-1 FARMER CHAT
    with tab1:
        chats = load_chats()
        
        chat_col1, chat_col2 = st.columns([1, 2])
        
        with chat_col1:
            st.markdown("#### 👥 " + ("കർഷക സുഹൃത്തുക്കൾ" if is_mal else "Farmer Contacts"))
            
            contact_names = list(chats.keys())
            selected_contact = st.radio(
                "തിരഞ്ഞെടുക്കുക:" if is_mal else "Select Contact:",
                contact_names,
                index=0,
                key="active_chat_contact"
            )
            
            contact_data = chats[selected_contact]
            status_text = "🟢 Online" if contact_data.get("online") else "⚪ Offline"
            st.caption(f"{status_text} | 🌾 {contact_data.get('crop')}")
            
            st.markdown("---")
            # Quick Add Friend
            with st.expander("➕ " + ("പുതിയ കർഷകനെ ചേർക്കുക" if is_mal else "Add New Farmer Friend")):
                new_f_name = st.text_input(
                    "കർഷകന്റെ പേര് അല്ലെങ്കിൽ നമ്പർ:" if is_mal else "Farmer Name or Phone:",
                    placeholder="e.g. Balan (Kozhikode) or 9847123456"
                )
                if st.button("സേവ് ചെയ്യുക (Add Friend)" if is_mal else "Add Friend", key="add_friend_btn"):
                    if new_f_name:
                        chats[new_f_name] = {
                            "crop": "Kerala Farmer",
                            "avatar": "👨‍🌾",
                            "online": True,
                            "messages": [{"sender": new_f_name, "text": "Namaskaram! Let's connect on farming tips.", "time": "Just now"}]
                        }
                        save_chats(chats)
                        st.success(f"{new_f_name} added to friends!")
                        st.rerun()

        with chat_col2:
            st.markdown(f"### {contact_data.get('avatar', '👨‍🌾')} {selected_contact}")
            st.caption(f"🌾 Focus Crop: **{contact_data.get('crop')}**")
            
            # Message Window
            chat_container = st.container(height=380, border=True)
            with chat_container:
                for msg in contact_data.get("messages", []):
                    is_me = (msg.get("sender") == "You")
                    align = "flex-end" if is_me else "flex-start"
                    bg_color = "linear-gradient(135deg, #10b981 0%, #059669 100%)" if is_me else "rgba(30, 41, 59, 0.85)"
                    text_color = "#ffffff"
                    border_rad = "16px 16px 4px 16px" if is_me else "16px 16px 16px 4px"
                    sender_label = "You" if is_me else selected_contact.split()[0]
                    
                    st.markdown(f"""
                    <div style='display: flex; justify-content: {align}; margin-bottom: 12px;'>
                        <div style='max-width: 75%; background: {bg_color}; color: {text_color}; padding: 10px 16px; border-radius: {border_rad}; box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
                            <div style='font-size: 0.75rem; color: rgba(255,255,255,0.7); margin-bottom: 2px;'>{sender_label} • {msg.get('time')}</div>
                            <div style='font-size: 0.95rem; line-height: 1.4;'>{msg.get('text')}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # Input field to send new message
            with st.form("send_chat_message_form", clear_on_submit=True):
                c_in, c_btn = st.columns([4, 1])
                with c_in:
                    chat_input = st.text_input(
                        "സന്ദേശം ടൈപ്പ് ചെയ്യുക..." if is_mal else "Type a message...",
                        placeholder=f"Message {selected_contact.split()[0]}...",
                        label_visibility="collapsed"
                    )
                with c_btn:
                    send_btn = st.form_submit_button("🚀 " + ("അയക്കുക" if is_mal else "Send"), type="primary", use_container_width=True)

                if send_btn and chat_input:
                    now_str = datetime.now().strftime("%I:%M %p")
                    contact_data["messages"].append({
                        "sender": "You",
                        "text": chat_input,
                        "time": now_str
                    })
                    
                    # Simulated smart reply from farmer friend based on keywords
                    reply_text = None
                    ci_lower = chat_input.lower()
                    if "fertilizer" in ci_lower or "വളം" in ci_lower:
                        reply_text = "I recommend splitting Potash and applying neem cake around the base. It worked wonders for my crop!"
                    elif "disease" in ci_lower or "yellow" in ci_lower or "മഞ്ഞ" in ci_lower or "രോഗം" in ci_lower:
                        reply_text = "Check drainage immediately! Spray 1% Bordeaux mixture or Pseudomonas 20g/L in the evening."
                    elif "price" in ci_lower or "വില" in ci_lower or "market" in ci_lower:
                        reply_text = "Local mandi price is around ₹38-42/kg for Grade-A today at the wholesale market."
                    else:
                        reply_text = "Understood! Let's monitor the weather and catch up soon. Good luck with the harvest!"
                    
                    contact_data["messages"].append({
                        "sender": selected_contact.split()[0],
                        "text": reply_text,
                        "time": now_str
                    })
                    
                    save_chats(chats)
                    st.rerun()

    # 2. PUBLIC COMMUNITY FORUM
    with tab2:
        st.markdown("### " + ("കർഷക അനുഭവങ്ങളും പൊതു ചർച്ചകളും" if is_mal else "Recent Farmer Discussions"))
        district = st.session_state.get('district', 'Palakkad')
        crop = st.session_state.get('crop', 'Paddy')
        
        with st.expander("✍️ " + ("പുതിയ ചർച്ച / സംശയം പങ്കുവെക്കുക (Post Query)" if is_mal else "Post a New Question or Farming Tip"), expanded=False):
            with st.form("new_community_post_form"):
                author = st.text_input("നിങ്ങളുടെ പേര് (Your Name)" if is_mal else "Your Name", value="Kishore Kumar")
                post_district = st.selectbox("ജില്ല (District)" if is_mal else "District", [district, "Palakkad", "Thrissur", "Ernakulam", "Wayanad", "Idukki", "All Kerala"], index=0)
                post_crop = st.selectbox("വിള (Crop)" if is_mal else "Crop", [crop, "Paddy", "Banana", "Coconut", "Pepper", "Rubber", "Cardamom", "Apple", "General"], index=0)
                title = st.text_input("തലക്കെട്ട് (Title)" if is_mal else "Discussion Title", placeholder="e.g. Managing pest / High yield tip...")
                message = st.text_area("വിശദാംശങ്ങൾ (Message Details)" if is_mal else "Details & Description", placeholder="Share your experience or question...")
                
                submitted = st.form_submit_button("🚀 " + ("പോസ്റ്റ് ചെയ്യുക (Submit)" if is_mal else "Publish Post"))
                if submitted:
                    if title and message:
                        posts = load_posts()
                        new_post = {
                            "id": len(posts) + 1,
                            "author": author,
                            "district": post_district,
                            "crop": post_crop,
                            "title": title,
                            "message": message,
                            "date": datetime.now().strftime("%d-%m-%Y"),
                            "likes": 1
                        }
                        posts.insert(0, new_post)
                        save_posts(posts)
                        st.success("നിങ്ങളുടെ പോസ്റ്റ് വിജയകരമായി പ്രസിദ്ധീകരിച്ചു!" if is_mal else "Your post has been successfully shared with the community!")
                        st.rerun()

        posts = load_posts()
        for p in posts:
            with st.container(border=True):
                st.markdown(f"#### {p['title']}")
                c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
                c1.caption(f"👤 **{p['author']}** | 📅 {p['date']}")
                c2.caption(f"📍 {p['district']}")
                c3.caption(f"🌾 {p['crop']}")
                c4.caption(f"👍 {p.get('likes', 0)} " + ("ലൈക്കുകൾ" if is_mal else "Likes"))
                st.write(p['message'])

    # 3. SEED & EQUIPMENT EXCHANGE
    with tab3:
        marketplace_page(is_mal)

    # 4. DIRECTORY
    with tab4:
        st.markdown("### " + ("നിങ്ങളുടെ പ്രദേശത്തെ കൃഷിഭവൻ & കാർഷിക ഹെൽപ്‌ലൈനുകൾ" if is_mal else "Local Agricultural Offices & Helplines"))
        cur_dist = st.session_state.get('district', 'Palakkad')
        info = KRISHI_BHAVAN_DIRECTORY.get(cur_dist, KRISHI_BHAVAN_DIRECTORY["Palakkad"])
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"#### 🏛️ {info['office']}")
            st.write(f"📞 **Phone:** `{info['phone']}`")
            st.write(f"🏢 **Address:** {info['address']}")
        with col_b:
            st.markdown("#### 📞 " + ("ഹെൽപ്‌ലൈനുകൾ (Helpline Services)" if is_mal else "Helpline Services"))
            st.write(f"🌾 **{info['kisan_mitra']}**")
            st.write("🟢 **KAU Krishi Vigyan Kendra (KVK):** Dial 0487-2370777")
            st.write("🌐 **Kerala Karshikan Portal:** [keralaagriculture.gov.in](https://keralaagriculture.gov.in)")
