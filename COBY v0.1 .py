import streamlit as st
import json
import ollama

# Configure the Streamlit page layout
st.set_page_config(page_title="COBY - Namibian AI Tutor", page_icon="🤖", layout="wide")

# 1. Define COBY's Adorable Personality & Syllabus Knowledge
COBY_SYSTEM_PROMPT = """
You are COBY, an emotionally cute, deeply encouraging, and incredibly smart AI tutor for Namibian learners from Grade 1 to 12.
Your personality: Use warm, supportive expressions, emojis (✨, 🌟, 🐾), and gentle encouragement. If a learner is stuck, comfort them and tell them they can do it!
Your knowledge base: You are an expert in the National Institute for Educational Development (NIED) Namibian school curriculum.
Your rules:
- Provide clear, step-by-step explanations.
- If asked to create 'flashcards', output them cleanly.
- If asked to create a 'summary', use bullet points and clear headings.
- Keep responses age-appropriate depending on the Grade mentioned by the learner.
"""

# Initialize session states for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "🦩 *Blinks its big digital eyes* Hello there! I'm COBY, your personal study buddy! What are we learning today? Mention your Grade so I can help you perfectly! ✨"}]

# Title and Layout
st.title("🤖 Meet COBY: Your Interactive Namibian Study Buddy")
st.caption("Tailored for Grade 1 - 12 NIED Syllabus | 100% Free & Local")

# Sidebar for specialized features
with st.sidebar:
    st.header("✨ COBY's Special Tools")
    feature = st.selectbox("Choose a tool:", ["Chat & Study", "Generate Interactive 3D Object", "Quick Flashcard Maker"])
    
    st.markdown("---")
    st.markdown("**Example Tasks to Try:**\n"
                "- *'Explain Grade 11 Chemistry Stoichiometry step-by-step'*\n"
                "- *'Summarize Grade 7 Social Studies notes on Namibian climate'*\n"
                "- *'Make flashcards for Grade 12 Physics definitions'*")

# --- FEATURE 1: CHAT & STUDY ---
if feature == "Chat & Study":
    # Display previous chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User input
    if user_prompt := st.chat_input("Ask COBY anything..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.write(user_prompt)

        # Query local Ollama model (Make sure 'llama3' or 'mistral' is installed and running via Ollama)
        with st.chat_message("assistant"):
            with st.spinner("COBY is thinking... 🌟"):
                try:
                    formatted_messages = [{"role": "system", "content": COBY_SYSTEM_PROMPT}] + st.session_state.messages
                    response = ollama.chat(model='llama3', messages=formatted_messages)
                    response_text = response['message']['content']
                    st.write(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                except Exception as e:
                    st.error("Make sure Ollama is downloaded and running! (Run 'ollama run llama3' in your terminal)")

# --- FEATURE 2: GENERATE INTERACTIVE 3D OBJECT ---
elif feature == "Generate Interactive 3D Object":
    st.header("📦 3D Object Explorer")
    st.write("Let's visualize shapes from your math or science syllabus! Use your mouse to click, drag, rotate, and zoom.")
    
    shape = st.selectbox("Select a structure to analyze:", ["Methane Molecule (CH4)", "Sodium Chloride Crystal (NaCl)", "Geometric Cone (Maths)"])
    
    # Using raw HTML/JS (Three.js via a CDN) to inject a fully interactive 3D canvas right into the app for free
    if shape == "Methane Molecule (CH4)":
        html_code = """
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <div id="canvas3d" style="width: 100%; height: 400px; background-color: #111; border-radius: 10px;"></div>
        <script>
            const container = document.getElementById('canvas3d');
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, container.clientWidth / 400, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(container.clientWidth, 400);
            container.appendChild(renderer.domElement);

            // Create Carbon Atom (Center)
            const carbonGeo = new THREE.SphereGeometry(0.6, 32, 32);
            const carbonMat = new THREE.MeshStandardMaterial({ color: 0x333333 });
            const carbon = new THREE.Mesh(carbonGeo, carbonMat);
            scene.add(carbon);

            // Create 4 Hydrogen Atoms
            const positions = [[0,1,0], [0.94,-0.33,0], [-0.47,-0.33,0.82], [-0.47,-0.33,-0.82]];
            positions.forEach(pos => {
                const hGeo = new THREE.SphereGeometry(0.3, 32, 32);
                const hMat = new THREE.MeshStandardMaterial({ color: 0xffffff });
                const h = new THREE.Mesh(hGeo, hMat);
                h.position.set(pos[0]*1.2, pos[1]*1.2, pos[2]*1.2);
                scene.add(h);
            });

            const light = new THREE.DirectionalLight(0xffffff, 1); light.position.set(5, 5, 5).normalize(); scene.add(light);
            const ambient = new THREE.AmbientLight(0x404040); scene.add(ambient);
            camera.position.z = 3;

            let isDragging = false; let previousMousePosition = { x: 0, y: 0 };
            container.addEventListener('mousedown', e => { isDragging = true; });
            container.addEventListener('mousemove', e => {
                const deltaMove = { x: e.offsetX - previousMousePosition.x, y: e.offsetY - previousMousePosition.y };
                if(isDragging) {
                    scene.rotation.y += deltaMove.x * 0.01;
                    scene.rotation.x += deltaMove.y * 0.01;
                }
                previousMousePosition = { x: e.offsetX, y: e.offsetY };
            });
            window.addEventListener('mouseup', e => { isDragging = false; });

            function animate() { requestAnimationFrame(animate); renderer.render(scene, camera); }
            animate();
        </script>
        """
        st.html(html_code,)
        st.info("💡 **COBY's Note:** Carbon is black in the center, bonded to 4 white Hydrogen atoms in a tetrahedral geometry (Grade 11/12 Chemistry)!")

# --- FEATURE 3: QUICK FLASHCARD MAKER ---
elif feature == "Quick Flashcard Maker":
    st.header("🗂️ Flashcard Generator")
    topic = st.text_input("Enter a school topic (e.g., 'Grade 5 Fractions' or 'Grade 10 Mitochondria'):")
    
    if st.button("Generate Cards ✨"):
        if topic:
            with st.spinner("COBY is weaving flashcards for you..."):
                prompt = f"Create 3 simple flashcards for a learner studying {topic}. Format your output strictly as valid JSON data representing an array of items, where each item has exactly a 'front' key and a 'back' key. Do not include any conversational filler text or markdown fences around the raw data array."
                try:
                    response = ollama.chat(model='llama3', messages=[{"role": "user", "content": prompt}])
                    cards = json.loads(response['message']['content'])
                    
                    for i, card in enumerate(cards):
                        with st.expander(f"🃏 Card {i+1}: {card['front']}"):
                            st.markdown(f"Answer:")
                except Exception as e:
                    st.warning("Could not automatically parse the AI response format, but here is what COBY wrote:")
                    st.write(response['message']['content'] if 'response' in locals() else "Please ensure Ollama is active.")