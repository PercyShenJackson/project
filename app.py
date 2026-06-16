from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime, date

app = Flask(__name__)

# ============================================================
# DATA: All 7 CS branches with lessons, quizzes, prerequisites
# ============================================================

BRANCHES = {
    "web": {
        "name": "Web Development",
        "icon": "🌐",
        "description": "Full‑stack web development from HTML to deployment",
        "modules": [
            {
                "id": "web_html",
                "title": "HTML Fundamentals",
                "xp": 50,
                "prerequisites": [],
                "lesson": """
                <h3>HTML – The Skeleton of the Web</h3>
                <p>HTML (HyperText Markup Language) structures web content.</p>
                <pre><code>&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;&lt;title&gt;Page&lt;/title&gt;&lt;/head&gt;
&lt;body&gt;
  &lt;h1&gt;Hello World&lt;/h1&gt;
  &lt;p&gt;A paragraph.&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>
                <p><strong>Key elements:</strong> &lt;div&gt;, &lt;span&gt;, &lt;a&gt;, &lt;img&gt;, lists.</p>
                """,
                "quiz": [
                    {"q": "What does HTML stand for?", "options": ["HyperText Markup Language", "High Tech Modern Language", "HyperText Modern Layout", "Home Tool Markup Language"], "answer": 0},
                    {"q": "Which tag creates a hyperlink?", "options": ["&lt;link&gt;", "&lt;a&gt;", "&lt;href&gt;", "&lt;url&gt;"], "answer": 1},
                    {"q": "Where does visible content go?", "options": ["&lt;head&gt;", "&lt;meta&gt;", "&lt;body&gt;", "&lt;title&gt;"], "answer": 2}
                ]
            },
            {
                "id": "web_css",
                "title": "CSS Styling",
                "xp": 50,
                "prerequisites": ["web_html"],
                "lesson": """
                <h3>CSS – Making It Beautiful</h3>
                <p>CSS (Cascading Style Sheets) controls visual presentation.</p>
                <pre><code>/* Element */
p { color: blue; }

/* Class */
.highlight { background: yellow; }

/* ID */
#header { font-size: 24px; }</code></pre>
                <p><strong>Box Model:</strong> margin → border → padding → content</p>
                """,
                "quiz": [
                    {"q": "What does CSS stand for?", "options": ["Cascading Style Sheets", "Computer Style Sheets", "Creative Style System", "Colorful Style Sheets"], "answer": 0},
                    {"q": "Which selector targets a class?", "options": ["#class", ".class", "class", "@class"], "answer": 1},
                    {"q": "Which property changes text color?", "options": ["text-color", "font-color", "color", "text-style"], "answer": 2}
                ]
            },
            {
                "id": "web_js",
                "title": "JavaScript Basics",
                "xp": 75,
                "prerequisites": ["web_html"],
                "lesson": """
                <h3>JavaScript – Making It Interactive</h3>
                <p>JavaScript adds behaviour to web pages.</p>
                <pre><code>let name = "John";
const age = 25;

function greet(name) {
    return "Hello, " + name + "!";
}

document.querySelector(".btn").addEventListener("click", handleClick);</code></pre>
                """,
                "quiz": [
                    {"q": "Which keyword declares a constant?", "options": ["let", "var", "const", "static"], "answer": 2},
                    {"q": "What does DOM stand for?", "options": ["Document Object Model", "Data Object Method", "Digital Ordinance Model", "Document Orientation Module"], "answer": 0},
                    {"q": "How to write a function?", "options": ["func myFunc()", "function myFunc()", "def myFunc()", "fn myFunc()"], "answer": 1}
                ]
            }
        ]
    },
    "ai": {
        "name": "Artificial Intelligence",
        "icon": "🤖",
        "description": "Machine learning, deep learning, and AI systems",
        "modules": [
            {
                "id": "ai_ml_intro",
                "title": "Machine Learning Basics",
                "xp": 75,
                "prerequisites": [],
                "lesson": """
                <h3>What is Machine Learning?</h3>
                <p>ML enables systems to learn from data.</p>
                <ul>
                    <li><strong>Supervised</strong> – labelled data</li>
                    <li><strong>Unsupervised</strong> – no labels</li>
                    <li><strong>Reinforcement</strong> – rewards/penalties</li>
                </ul>
                <pre><code>from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)</code></pre>
                """,
                "quiz": [
                    {"q": "What type uses labelled data?", "options": ["Unsupervised", "Supervised", "Reinforcement", "All"], "answer": 1},
                    {"q": "Common Python ML library?", "options": ["NumPy", "scikit-learn", "Flask", "Requests"], "answer": 1},
                    {"q": "Regression predicts?", "options": ["Categories", "Continuous values", "Clusters", "Rules"], "answer": 1}
                ]
            },
            {
                "id": "ai_neural",
                "title": "Neural Networks",
                "xp": 100,
                "prerequisites": ["ai_ml_intro"],
                "lesson": """
                <h3>Neural Networks</h3>
                <p>Inspired by the brain. Layers: input, hidden, output.</p>
                <p><strong>Neuron:</strong> output = activation( Σ(weights × inputs) + bias )</p>
                """,
                "quiz": [
                    {"q": "Layers in a neural network?", "options": ["Input, Hidden, Output", "Start, Middle, End", "Front, Center, Back", "Top, Middle, Bottom"], "answer": 0},
                    {"q": "Activation function adds?", "options": ["Linearity", "Non‑linearity", "Speed", "Bias only"], "answer": 1},
                    {"q": "Backpropagation is?", "options": ["Forward pass", "Weight update with gradients", "Data preprocessing", "Model deployment"], "answer": 1}
                ]
            }
        ]
    },
    "security": {
        "name": "Cybersecurity",
        "icon": "🔒",
        "description": "Security, cryptography, and ethical hacking",
        "modules": [
            {
                "id": "sec_crypto",
                "title": "Cryptography",
                "xp": 75,
                "prerequisites": [],
                "lesson": """
                <h3>Cryptography</h3>
                <p>Secure communication in the presence of adversaries.</p>
                <ul>
                    <li><strong>Encryption</strong> – plaintext → ciphertext</li>
                    <li><strong>Hashing</strong> – one‑way (SHA‑256)</li>
                    <li><strong>Symmetric</strong> – AES (same key)</li>
                    <li><strong>Asymmetric</strong> – RSA (public/private)</li>
                </ul>
                """,
                "quiz": [
                    {"q": "Hashing is?", "options": ["Two‑way", "One‑way", "Compression", "Encoding"], "answer": 1},
                    {"q": "Asymmetric encryption example?", "options": ["AES", "DES", "RSA", "Blowfish"], "answer": 2},
                    {"q": "Encryption provides?", "options": ["Speed", "Confidentiality", "Compression", "Formatting"], "answer": 1}
                ]
            },
            {
                "id": "sec_network",
                "title": "Network Security",
                "xp": 75,
                "prerequisites": ["sec_crypto"],
                "lesson": """
                <h3>Network Security</h3>
                <p>Threats: DDoS, MITM, phishing, SQL injection.</p>
                <p>Defenses: firewalls, IDS/IPS, VPNs, input sanitization.</p>
                """,
                "quiz": [
                    {"q": "DDoS stands for?", "options": ["Distributed Denial of Service", "Direct Data of System", "Digital Denial of Security", "Distributed Data over Service"], "answer": 0},
                    {"q": "Firewall is?", "options": ["Physical barrier", "Network security device", "Antivirus", "Password manager"], "answer": 1},
                    {"q": "Phishing is?", "options": ["Network scan", "Social engineering", "Password cracking", "DDoS attack"], "answer": 1}
                ]
            }
        ]
    },
    "os": {
        "name": "Operating Systems",
        "icon": "💻",
        "description": "How operating systems work under the hood",
        "modules": [
            {
                "id": "os_processes",
                "title": "Processes & Threads",
                "xp": 75,
                "prerequisites": [],
                "lesson": """
                <h3>Processes & Threads</h3>
                <p>Process = program in execution. Thread = unit inside process.</p>
                <p><strong>States:</strong> New → Ready → Running → Waiting → Terminated</p>
                """,
                "quiz": [
                    {"q": "What is a process?", "options": ["A file", "Program in execution", "CPU core", "Memory address"], "answer": 1},
                    {"q": "Threads share?", "options": ["CPU", "Memory space", "Nothing", "I/O only"], "answer": 1},
                    {"q": "Which is NOT a state?", "options": ["Ready", "Running", "Sleeping permanently", "Waiting"], "answer": 2}
                ]
            },
            {
                "id": "os_memory",
                "title": "Memory Management",
                "xp": 75,
                "prerequisites": ["os_processes"],
                "lesson": """
                <h3>Memory Management</h3>
                <p>Virtual memory, paging, segmentation, fragmentation.</p>
                """,
                "quiz": [
                    {"q": "Virtual memory uses?", "options": ["Extra RAM", "Disk as extension", "Cache", "GPU memory"], "answer": 1},
                    {"q": "Paging divides memory into?", "options": ["Segments", "Fixed‑size pages", "Files", "Processes"], "answer": 1},
                    {"q": "Fragmentation is caused by?", "options": ["Fast CPU", "Allocation patterns", "Large files", "Network latency"], "answer": 1}
                ]
            }
        ]
    },
    "networks": {
        "name": "Networking",
        "icon": "🌍",
        "description": "Protocols, TCP/IP, DNS, HTTP",
        "modules": [
            {
                "id": "net_tcpip",
                "title": "TCP/IP Suite",
                "xp": 50,
                "prerequisites": [],
                "lesson": """
                <h3>TCP/IP Model</h3>
                <p>Layers: Application (HTTP, DNS), Transport (TCP/UDP), Internet (IP), Network Access (Ethernet).</p>
                """,
                "quiz": [
                    {"q": "TCP/IP layers?", "options": ["3", "4", "5", "7"], "answer": 1},
                    {"q": "Reliable protocol?", "options": ["UDP", "TCP", "IP", "ICMP"], "answer": 1},
                    {"q": "HTTP belongs to which layer?", "options": ["Transport", "Internet", "Application", "Network"], "answer": 2}
                ]
            },
            {
                "id": "net_dns",
                "title": "DNS & HTTP",
                "xp": 50,
                "prerequisites": ["net_tcpip"],
                "lesson": """
                <h3>DNS & HTTP</h3>
                <p>DNS translates names to IPs. HTTP methods: GET, POST, PUT, DELETE.</p>
                """,
                "quiz": [
                    {"q": "DNS does?", "options": ["Encrypts", "Translates names to IPs", "Routes packets", "Compresses"], "answer": 1},
                    {"q": "HTTP method to create?", "options": ["GET", "POST", "DELETE", "HEAD"], "answer": 1},
                    {"q": "Status code 404 means?", "options": ["OK", "Moved", "Not Found", "Server Error"], "answer": 2}
                ]
            }
        ]
    },
    "databases": {
        "name": "Databases",
        "icon": "🗄️",
        "description": "SQL, NoSQL, and data management",
        "modules": [
            {
                "id": "db_sql",
                "title": "SQL Fundamentals",
                "xp": 50,
                "prerequisites": [],
                "lesson": """
                <h3>SQL – Structured Query Language</h3>
                <pre><code>SELECT * FROM users WHERE age > 18;
INSERT INTO users (name, age) VALUES ('Alice', 25);
UPDATE users SET age = 26 WHERE name = 'Alice';
DELETE FROM users WHERE name = 'Alice';</code></pre>
                """,
                "quiz": [
                    {"q": "SQL command to retrieve data?", "options": ["INSERT", "SELECT", "UPDATE", "DELETE"], "answer": 1},
                    {"q": "Which is a valid SQL keyword?", "options": ["FOR", "WHERE", "EACH", "WHILE"], "answer": 1},
                    {"q": "What does CRUD stand for?", "options": ["Create, Read, Update, Delete", "Copy, Run, Undo, Drop", "Class, Return, Unit, Data", "None"], "answer": 0}
                ]
            },
            {
                "id": "db_nosql",
                "title": "NoSQL Databases",
                "xp": 50,
                "prerequisites": ["db_sql"],
                "lesson": """
                <h3>NoSQL Databases</h3>
                <p>Types: Document (MongoDB), Key‑Value (Redis), Column‑Family (Cassandra), Graph (Neo4j).</p>
                """,
                "quiz": [
                    {"q": "MongoDB is which type?", "options": ["Key‑Value", "Document", "Graph", "Column"], "answer": 1},
                    {"q": "Redis is?", "options": ["Document", "Key‑Value", "Graph", "Relational"], "answer": 1},
                    {"q": "NoSQL means?", "options": ["No SQL at all", "Not Only SQL", "Never SQL", "New SQL"], "answer": 1}
                ]
            }
        ]
    },
    "cloud": {
        "name": "Cloud Computing",
        "icon": "☁️",
        "description": "Containers, Kubernetes, serverless",
        "modules": [
            {
                "id": "cloud_containers",
                "title": "Containers & Docker",
                "xp": 50,
                "prerequisites": [],
                "lesson": """
                <h3>Containers</h3>
                <p>Lightweight, portable units that package code and dependencies.</p>
                <pre><code>docker run -d -p 80:80 nginx</code></pre>
                """,
                "quiz": [
                    {"q": "Docker is a?", "options": ["Container runtime", "Programming language", "Database", "OS"], "answer": 0},
                    {"q": "Command to run a container?", "options": ["docker start", "docker run", "docker execute", "docker launch"], "answer": 1},
                    {"q": "Containers share the host's?", "options": ["Kernel", "BIOS", "Hard drive only", "Nothing"], "answer": 0}
                ]
            },
            {
                "id": "cloud_k8s",
                "title": "Kubernetes",
                "xp": 75,
                "prerequisites": ["cloud_containers"],
                "lesson": """
                <h3>Kubernetes (K8s)</h3>
                <p>Orchestrates containers across clusters. Pods, Services, Deployments.</p>
                """,
                "quiz": [
                    {"q": "Kubernetes is for?", "options": ["Container orchestration", "Database management", "Code editing", "Testing"], "answer": 0},
                    {"q": "Smallest deployable unit?", "options": ["Node", "Pod", "Cluster", "Service"], "answer": 1},
                    {"q": "K8s stands for?", "options": ["Kubernetes", "K8s is short for Kubernetes", "Both", "Neither"], "answer": 2}
                ]
            }
        ]
    }
}

# ============================================================
# ACHIEVEMENTS / BADGES
# ============================================================
ACHIEVEMENTS = [
    {"id": "first_lesson", "name": "First Steps", "desc": "Complete your first lesson", "icon": "👶"},
    {"id": "first_branch", "name": "Branch Master", "desc": "Finish all modules in one branch", "icon": "🌿"},
    {"id": "streak_3", "name": "3‑Day Streak", "desc": "Maintain a 3‑day learning streak", "icon": "🔥"},
    {"id": "streak_7", "name": "Weekly Warrior", "desc": "7‑day streak", "icon": "⚔️"},
    {"id": "xp_500", "name": "500 XP", "desc": "Earn 500 XP", "icon": "⭐"},
    {"id": "xp_2000", "name": "Knowledge Seeker", "desc": "Earn 2000 XP", "icon": "📚"},
    {"id": "hero", "name": "CS Hero", "desc": "Reach Hero rank", "icon": "🏆"},
]

# ============================================================
# PROGRESS FILE HANDLING
# ============================================================
PROGRESS_FILE = "progress.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {
        "xp": 0,
        "completed_modules": [],
        "streak": 0,
        "last_login": None,
        "achievements": [],
        "coding_history": []
    }

def save_progress(p):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(p, f, indent=2)

# ============================================================
# HELPER: check streak update
# ============================================================
def update_streak(p):
    today = str(date.today())
    last = p.get("last_login")
    if last == today:
        return
    if last is None:
        p["streak"] = 1
    else:
        last_date = datetime.strptime(last, "%Y-%m-%d").date()
        diff = (date.today() - last_date).days
        if diff == 1:
            p["streak"] += 1
        elif diff > 1:
            p["streak"] = 1
        else:
            return
    p["last_login"] = today
    # Check streak achievements
    if p["streak"] >= 3 and "streak_3" not in p["achievements"]:
        p["achievements"].append("streak_3")
    if p["streak"] >= 7 and "streak_7" not in p["achievements"]:
        p["achievements"].append("streak_7")

# ============================================================
# ROUTES
# ============================================================
@app.route("/")
def home():
    # No Jinja2 variables needed; frontend uses API for everything
    return render_template("index.html")

@app.route("/api/branches")
def get_branches():
    result = {}
    for bid, bdata in BRANCHES.items():
        result[bid] = {
            "name": bdata["name"],
            "icon": bdata["icon"],
            "description": bdata["description"],
            "modules": [
                {"id": m["id"], "title": m["title"], "xp": m["xp"], "prerequisites": m["prerequisites"]}
                for m in bdata["modules"]
            ]
        }
    return jsonify(result)

@app.route("/api/lesson/<module_id>")
def get_lesson(module_id):
    for bdata in BRANCHES.values():
        for m in bdata["modules"]:
            if m["id"] == module_id:
                return jsonify({
                    "id": m["id"],
                    "title": m["title"],
                    "lesson": m["lesson"],
                    "quiz": m["quiz"],
                    "xp": m["xp"],
                    "prerequisites": m["prerequisites"]
                })
    return jsonify({"error": "Module not found"}), 404

@app.route("/api/progress")
def get_progress():
    p = load_progress()
    update_streak(p)
    save_progress(p)
    return jsonify(p)

@app.route("/api/complete/<module_id>", methods=["POST"])
def complete_module(module_id):
    p = load_progress()
    if module_id in p["completed_modules"]:
        return jsonify({"message": "Already completed", "progress": p})
    
    xp = 0
    for bdata in BRANCHES.values():
        for m in bdata["modules"]:
            if m["id"] == module_id:
                if not all(pr in p["completed_modules"] for pr in m["prerequisites"]):
                    return jsonify({"error": "Prerequisites not met"}), 400
                xp = m["xp"]
                break
    
    p["completed_modules"].append(module_id)
    p["xp"] += xp
    
    if "first_lesson" not in p["achievements"]:
        p["achievements"].append("first_lesson")
    if p["xp"] >= 500 and "xp_500" not in p["achievements"]:
        p["achievements"].append("xp_500")
    if p["xp"] >= 2000 and "xp_2000" not in p["achievements"]:
        p["achievements"].append("xp_2000")
    
    for bid, bdata in BRANCHES.items():
        branch_module_ids = [m["id"] for m in bdata["modules"]]
        if all(mid in p["completed_modules"] for mid in branch_module_ids):
            if "first_branch" not in p["achievements"]:
                p["achievements"].append("first_branch")
    
    if p["xp"] >= 5000 and "hero" not in p["achievements"]:
        p["achievements"].append("hero")
    
    update_streak(p)
    save_progress(p)
    return jsonify({"message": "Module completed", "progress": p})

@app.route("/api/quiz/<module_id>", methods=["POST"])
def submit_quiz(module_id):
    data = request.get_json()
    answers = data.get("answers", [])
    for bdata in BRANCHES.values():
        for m in bdata["modules"]:
            if m["id"] == module_id:
                quiz = m["quiz"]
                score = sum(1 for i, q in enumerate(quiz) if i < len(answers) and answers[i] == q["answer"])
                total = len(quiz)
                xp_earned = int(score / total * m["xp"]) if total > 0 else 0
                
                p = load_progress()
                p["xp"] += xp_earned
                update_streak(p)
                save_progress(p)
                
                return jsonify({
                    "score": score,
                    "total": total,
                    "xp_earned": xp_earned,
                    "progress": p
                })
    return jsonify({"error": "Module not found"}), 404

@app.route("/api/execute", methods=["POST"])
def execute_code():
    """Simple Python code execution sandbox (USE ONLY LOCALLY)"""
    code = request.get_json().get("code", "")
    p = load_progress()
    p["coding_history"].append({"code": code, "timestamp": datetime.now().isoformat()})
    save_progress(p)
    try:
        import io, sys
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        exec(code, {"__builtins__": __builtins__}, {})
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        return jsonify({"output": output})
    except Exception as e:
        return jsonify({"output": f"Error: {str(e)}"})

@app.route("/api/rank")
def get_rank():
    p = load_progress()
    xp = p["xp"]
    if xp >= 5000: rank = "Hero"
    elif xp >= 4000: rank = "Specialist"
    elif xp >= 3000: rank = "Master"
    elif xp >= 2000: rank = "Architect"
    elif xp >= 1500: rank = "Engineer"
    elif xp >= 1000: rank = "Builder"
    elif xp >= 500: rank = "Explorer"
    else: rank = "Novice"
    return jsonify({"rank": rank, "xp": xp})

@app.route("/api/achievements")
def get_achievements():
    return jsonify(ACHIEVEMENTS)

if __name__ == "__main__":
    app.run(debug=True, port=3000)