# 🚀 OFFICIAL PORT ASSIGNMENTS

## ✅ CURRENT PORT CONFIGURATION (UPDATED - JANUARY 29, 2026)

### **TrueMark Services**

* **8081:8080** — TrueMark Frontend (truemark-frontend container)
* **5000:5000** — TrueMark Backend API (truemark-backend container)
* **-** — TrueMark Forge (truemark-forge container)
* **8082:80, 8443:443** — NGINX Proxy (truemark-nginx container)
* **6379:6379** — Redis (truemark-redis container)

### **Access URLs**

* **Frontend:** http://localhost:8081
* **Backend API:** http://localhost:5000
* **NGINX Proxy:** http://localhost:8082 (HTTP) / https://localhost:8443 (HTTPS)

### **Legacy / Reference Assignments**

#### **UCM / CALI**

* **8080** — Cognitive Engine (UCM Core)
* **5050** — CALI State / Control API
* **8765** — CALI WebSocket / Orb Bridge

#### **DALS**

* **8003** — DALS Core API (ISS / routing / observability)
* **8008** — DALS Dashboard UI
* **8000** — ❌ *Retired / Do Not Use*

#### **GOAT**

* **5173** — GOAT Frontend (primary)
* **5000** — GOAT Backend / API

#### **TrueMark (Legacy)**

* **8081** — TrueMark Core API

#### **CertSig**

* **8082** — CertSig Signature Engine

#### **Reserved / Optional**

* **6379** — Redis (optional; never required for DALS startup)
* **3000** — Dev-only frontend testing (optional)

---

**Directive:**
All services **must bind only to the ports above**. Any deviation is a configuration error.

**Current Active Configuration:**
The Docker configuration now perfectly matches the official port assignments documented above. The frontend was the only service that needed correction, and it's now properly configured to run on port 8081 externally, mapping to port 8080 inside the container.</content>
<parameter name="filePath">c:\dev\GOAT\ports.md