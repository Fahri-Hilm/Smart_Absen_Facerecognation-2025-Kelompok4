# 🎨 UI/UX Guide - ABSENN

## 📋 **Overview**

ABSENN menggunakan **Modern Glass Morphism Design System** dengan coffee-themed color palette yang memberikan pengalaman user yang elegan, professional, dan user-friendly untuk sistem absensi enterprise.

---

## 🎨 **Design System**

### 🌈 **Color Palette**

#### Primary Colors (Coffee Theme)
```css
:root {
  /* Coffee-inspired primary colors */
  --coffee-dark: #2C1810;       /* Dark roast */
  --coffee-medium: #8B4513;     /* Medium roast */
  --coffee-light: #D2B48C;      /* Latte */
  --coffee-cream: #F5F5DC;      /* Cream */
  
  /* Glass morphism colors */
  --glass-primary: rgba(139, 69, 19, 0.1);
  --glass-secondary: rgba(44, 24, 16, 0.05);
  --glass-border: rgba(255, 255, 255, 0.2);
  
  /* Status colors */
  --success: #27AE60;           /* Green */
  --warning: #F39C12;           /* Orange */
  --error: #E74C3C;             /* Red */
  --info: #3498DB;              /* Blue */
  
  /* Neutral colors */
  --white: #FFFFFF;
  --gray-100: #F8F9FA;
  --gray-200: #E9ECEF;
  --gray-300: #DEE2E6;
  --gray-400: #CED4DA;
  --gray-500: #ADB5BD;
  --gray-600: #6C757D;
  --gray-700: #495057;
  --gray-800: #343A40;
  --gray-900: #212529;
}
```

#### Semantic Colors
```css
/* Attendance status colors */
.status-hadir { color: var(--success); }
.status-izin { color: var(--info); }
.status-sakit { color: var(--warning); }
.status-alpha { color: var(--error); }
.status-cuti { color: var(--gray-600); }

/* Recognition confidence colors */
.confidence-high { color: var(--success); }    /* > 0.9 */
.confidence-medium { color: var(--warning); }  /* 0.7-0.9 */
.confidence-low { color: var(--error); }       /* < 0.7 */
```

---

### 🎭 **Typography**

#### Font Families
```css
:root {
  /* Primary font - Modern & clean */
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 
                  Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  
  /* Secondary font - Elegant headers */
  --font-secondary: 'Playfair Display', Georgia, serif;
  
  /* Monospace - Code & data */
  --font-mono: 'JetBrains Mono', 'Fira Code', Monaco, 'Cascadia Code', 
               'Roboto Mono', Consolas, monospace;
}
```

#### Typography Scale
```css
/* Typography scale - Perfect fifth (1.5) */
.text-xs { font-size: 0.75rem; line-height: 1rem; }      /* 12px */
.text-sm { font-size: 0.875rem; line-height: 1.25rem; }  /* 14px */
.text-base { font-size: 1rem; line-height: 1.5rem; }     /* 16px */
.text-lg { font-size: 1.125rem; line-height: 1.75rem; }  /* 18px */
.text-xl { font-size: 1.25rem; line-height: 1.75rem; }   /* 20px */
.text-2xl { font-size: 1.5rem; line-height: 2rem; }      /* 24px */
.text-3xl { font-size: 1.875rem; line-height: 2.25rem; } /* 30px */
.text-4xl { font-size: 2.25rem; line-height: 2.5rem; }   /* 36px */
.text-5xl { font-size: 3rem; line-height: 1; }           /* 48px */

/* Font weights */
.font-thin { font-weight: 100; }
.font-light { font-weight: 300; }
.font-normal { font-weight: 400; }
.font-medium { font-weight: 500; }
.font-semibold { font-weight: 600; }
.font-bold { font-weight: 700; }
.font-extrabold { font-weight: 800; }
.font-black { font-weight: 900; }
```

---

### 🌊 **Glass Morphism Components**

#### Base Glass Component
```css
.glass-component {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  box-shadow: 
    0 8px 32px rgba(31, 38, 135, 0.37),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.glass-card {
  @extend .glass-component;
  padding: 2rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-card:hover {
  transform: translateY(-4px);
  box-shadow: 
    0 20px 64px rgba(31, 38, 135, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
}

.glass-button {
  @extend .glass-component;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  color: var(--white);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.glass-button:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
}

.glass-input {
  @extend .glass-component;
  padding: 1rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  color: var(--white);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.glass-input:focus {
  outline: none;
  border-color: rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.1);
}
```

#### Specialized Glass Components
```css
/* QR Code Container */
.qr-glass-container {
  @extend .glass-card;
  text-align: center;
  max-width: 400px;
  margin: 2rem auto;
  position: relative;
  overflow: hidden;
}

.qr-glass-container::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
  transform: rotate(45deg);
  animation: shimmer 3s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
  100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
}

/* Face Recognition Container */
.camera-glass-container {
  @extend .glass-card;
  position: relative;
  border-radius: 20px;
  overflow: hidden;
}

.camera-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 200px;
  height: 200px;
  border: 3px solid var(--success);
  border-radius: 50%;
  box-shadow: 
    0 0 20px rgba(39, 174, 96, 0.5),
    inset 0 0 20px rgba(39, 174, 96, 0.1);
  animation: pulse-recognition 2s infinite;
}

@keyframes pulse-recognition {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.1); }
}

/* Status Cards */
.status-card {
  @extend .glass-card;
  padding: 1.5rem;
  text-align: center;
  border-radius: 16px;
  position: relative;
}

.status-card-success {
  background: linear-gradient(135deg, 
    rgba(39, 174, 96, 0.1), 
    rgba(39, 174, 96, 0.05)
  );
  border-color: rgba(39, 174, 96, 0.3);
}

.status-card-warning {
  background: linear-gradient(135deg, 
    rgba(243, 156, 18, 0.1), 
    rgba(243, 156, 18, 0.05)
  );
  border-color: rgba(243, 156, 18, 0.3);
}

.status-card-error {
  background: linear-gradient(135deg, 
    rgba(231, 76, 60, 0.1), 
    rgba(231, 76, 60, 0.05)
  );
  border-color: rgba(231, 76, 60, 0.3);
}
```

---

## 📱 **Responsive Design**

### 📐 **Breakpoints**
```css
:root {
  /* Responsive breakpoints */
  --breakpoint-xs: 475px;
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
}

/* Mobile First Approach */
/* Extra Small Devices (Phones) */
@media (min-width: 475px) {
  .container { max-width: 475px; }
}

/* Small Devices (Large Phones) */
@media (min-width: 640px) {
  .container { max-width: 640px; }
  .glass-card { padding: 2.5rem; }
}

/* Medium Devices (Tablets) */
@media (min-width: 768px) {
  .container { max-width: 768px; }
  .qr-glass-container { max-width: 500px; }
}

/* Large Devices (Laptops) */
@media (min-width: 1024px) {
  .container { max-width: 1024px; }
  .dashboard-grid { display: grid; grid-template-columns: repeat(3, 1fr); }
}

/* Extra Large Devices (Desktops) */
@media (min-width: 1280px) {
  .container { max-width: 1280px; }
  .dashboard-grid { grid-template-columns: repeat(4, 1fr); }
}
```

### 📱 **Mobile Optimizations**
```css
/* Mobile-specific components */
.mobile-nav {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  @extend .glass-component;
  backdrop-filter: blur(20px);
  border-radius: 20px 20px 0 0;
  padding: 1rem;
}

@media (max-width: 768px) {
  .mobile-nav { display: flex; }
  .desktop-nav { display: none; }
  
  .qr-glass-container {
    margin: 1rem;
    padding: 1.5rem;
  }
  
  .camera-glass-container {
    margin: 1rem;
    border-radius: 16px;
  }
  
  .glass-card {
    margin: 1rem;
    padding: 1.5rem;
  }
}

/* Touch-friendly buttons */
.touch-button {
  min-height: 44px;
  min-width: 44px;
  touch-action: manipulation;
}

/* Swipe gestures */
.swipeable {
  touch-action: pan-y;
  user-select: none;
}
```

---

## 🎯 **UI Components**

### 🔲 **Buttons**

#### Primary Button
```html
<button class="btn btn-primary">
  <i class="fas fa-sign-in-alt"></i>
  Absen Masuk
</button>
```

```css
.btn {
  @extend .glass-button;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-primary {
  background: linear-gradient(135deg, 
    rgba(139, 69, 19, 0.2), 
    rgba(139, 69, 19, 0.1)
  );
  border-color: rgba(139, 69, 19, 0.3);
  color: var(--white);
}

.btn-primary:hover {
  background: linear-gradient(135deg, 
    rgba(139, 69, 19, 0.3), 
    rgba(139, 69, 19, 0.2)
  );
  transform: translateY(-2px) scale(1.05);
}

.btn-success {
  background: linear-gradient(135deg, 
    rgba(39, 174, 96, 0.2), 
    rgba(39, 174, 96, 0.1)
  );
  border-color: rgba(39, 174, 96, 0.3);
}

.btn-warning {
  background: linear-gradient(135deg, 
    rgba(243, 156, 18, 0.2), 
    rgba(243, 156, 18, 0.1)
  );
  border-color: rgba(243, 156, 18, 0.3);
}

.btn-danger {
  background: linear-gradient(135deg, 
    rgba(231, 76, 60, 0.2), 
    rgba(231, 76, 60, 0.1)
  );
  border-color: rgba(231, 76, 60, 0.3);
}
```

#### Floating Action Button
```html
<button class="fab fab-primary" id="refreshQR">
  <i class="fas fa-refresh"></i>
</button>
```

```css
.fab {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  @extend .glass-component;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 
    0 8px 32px rgba(31, 38, 135, 0.37),
    0 4px 16px rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1000;
}

.fab:hover {
  transform: scale(1.1) rotate(180deg);
}

.fab-primary {
  background: linear-gradient(135deg, 
    rgba(139, 69, 19, 0.3), 
    rgba(139, 69, 19, 0.1)
  );
}
```

---

### 📊 **Cards & Containers**

#### Attendance Status Card
```html
<div class="attendance-status-card">
  <div class="status-icon">
    <i class="fas fa-check-circle"></i>
  </div>
  <div class="status-content">
    <h3>Sudah Absen Masuk</h3>
    <p>08:30 WIB</p>
    <div class="confidence-badge">
      Confidence: 98.5%
    </div>
  </div>
</div>
```

```css
.attendance-status-card {
  @extend .glass-card;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 2rem;
  margin: 1rem 0;
}

.status-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  @extend .glass-component;
}

.status-icon.success {
  background: linear-gradient(135deg, 
    rgba(39, 174, 96, 0.2), 
    rgba(39, 174, 96, 0.1)
  );
  color: var(--success);
}

.status-content h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--white);
}

.status-content p {
  margin: 0 0 1rem 0;
  color: var(--gray-300);
}

.confidence-badge {
  @extend .glass-component;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  display: inline-block;
  background: rgba(39, 174, 96, 0.1);
  color: var(--success);
  border: 1px solid rgba(39, 174, 96, 0.2);
}
```

#### Statistics Dashboard
```html
<div class="stats-dashboard">
  <div class="stat-card">
    <div class="stat-icon">
      <i class="fas fa-users"></i>
    </div>
    <div class="stat-content">
      <div class="stat-number">127</div>
      <div class="stat-label">Total Karyawan</div>
    </div>
  </div>
  
  <div class="stat-card">
    <div class="stat-icon success">
      <i class="fas fa-user-check"></i>
    </div>
    <div class="stat-content">
      <div class="stat-number">98</div>
      <div class="stat-label">Hadir Hari Ini</div>
    </div>
  </div>
  
  <div class="stat-card">
    <div class="stat-icon warning">
      <i class="fas fa-clock"></i>
    </div>
    <div class="stat-content">
      <div class="stat-number">15</div>
      <div class="stat-label">Terlambat</div>
    </div>
  </div>
</div>
```

```css
.stats-dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.stat-card {
  @extend .glass-card;
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  @extend .glass-component;
  background: rgba(255, 255, 255, 0.1);
  color: var(--white);
}

.stat-icon.success {
  background: linear-gradient(135deg, 
    rgba(39, 174, 96, 0.2), 
    rgba(39, 174, 96, 0.1)
  );
  color: var(--success);
}

.stat-icon.warning {
  background: linear-gradient(135deg, 
    rgba(243, 156, 18, 0.2), 
    rgba(243, 156, 18, 0.1)
  );
  color: var(--warning);
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: var(--white);
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--gray-300);
  margin-top: 0.25rem;
}
```

---

### 🎥 **Camera Interface**

#### Face Recognition UI
```html
<div class="face-recognition-container">
  <div class="camera-container">
    <video id="camera" autoplay></video>
    <canvas id="overlay" class="camera-overlay-canvas"></canvas>
    <div class="face-detection-overlay">
      <div class="face-frame"></div>
      <div class="scanning-line"></div>
    </div>
  </div>
  
  <div class="recognition-controls">
    <button class="btn btn-success" id="captureBtn">
      <i class="fas fa-camera"></i>
      Capture Face
    </button>
    <button class="btn btn-secondary" id="retryBtn">
      <i class="fas fa-redo"></i>
      Retry
    </button>
  </div>
  
  <div class="recognition-status">
    <div class="status-indicator" id="statusIndicator">
      <i class="fas fa-search"></i>
      <span>Scanning for face...</span>
    </div>
    <div class="confidence-meter">
      <div class="confidence-bar" id="confidenceBar"></div>
      <span id="confidenceText">--</span>
    </div>
  </div>
</div>
```

```css
.face-recognition-container {
  @extend .glass-card;
  max-width: 600px;
  margin: 2rem auto;
  text-align: center;
}

.camera-container {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 2rem;
  @extend .glass-component;
}

#camera {
  width: 100%;
  height: auto;
  border-radius: 16px;
}

.camera-overlay-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.face-detection-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 200px;
  height: 200px;
}

.face-frame {
  width: 100%;
  height: 100%;
  border: 3px solid var(--success);
  border-radius: 50%;
  position: relative;
  animation: pulse-frame 2s infinite;
}

.scanning-line {
  position: absolute;
  top: 0;
  left: 50%;
  width: 2px;
  height: 100%;
  background: linear-gradient(
    to bottom,
    transparent,
    var(--success),
    transparent
  );
  transform: translateX(-50%);
  animation: scanning 2s infinite;
}

@keyframes pulse-frame {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.05); opacity: 0.8; }
}

@keyframes scanning {
  0% { transform: translateX(-50%) rotate(0deg); }
  100% { transform: translateX(-50%) rotate(360deg); }
}

.recognition-controls {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.recognition-status {
  @extend .glass-component;
  padding: 1rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
}

.status-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  color: var(--white);
}

.status-indicator i {
  animation: spin 2s linear infinite;
}

.confidence-meter {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.confidence-bar {
  flex: 1;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}

.confidence-bar::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: var(--confidence-width, 0%);
  background: linear-gradient(90deg, var(--error), var(--warning), var(--success));
  border-radius: 4px;
  transition: width 0.3s ease;
}

#confidenceText {
  font-weight: 600;
  color: var(--white);
  min-width: 60px;
}
```

---

## 🎭 **Animations & Transitions**

### ⚡ **Loading Animations**

#### Spinner
```css
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-top: 4px solid var(--coffee-medium);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.spinner-dots {
  display: flex;
  gap: 0.5rem;
}

.spinner-dot {
  width: 8px;
  height: 8px;
  background: var(--coffee-medium);
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out;
}

.spinner-dot:nth-child(1) { animation-delay: -0.32s; }
.spinner-dot:nth-child(2) { animation-delay: -0.16s; }
.spinner-dot:nth-child(3) { animation-delay: 0s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}
```

#### Progress Bar
```css
.progress-container {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
  @extend .glass-component;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, var(--coffee-medium), var(--success));
  border-radius: 4px;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.progress-bar::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.4),
    transparent
  );
  animation: shimmer 2s infinite;
}
```

### 🎨 **Micro-interactions**

#### Button Hover Effects
```css
.interactive-button {
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.interactive-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: left 0.5s ease;
}

.interactive-button:hover::before {
  left: 100%;
}

.interactive-button:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 12px 24px rgba(31, 38, 135, 0.5),
    0 4px 8px rgba(0, 0, 0, 0.1);
}

.interactive-button:active {
  transform: translateY(0);
  transition: transform 0.1s ease;
}
```

#### Card Hover Effects
```css
.hover-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.hover-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    135deg,
    rgba(255, 255, 255, 0.1),
    rgba(255, 255, 255, 0.05)
  );
  border-radius: inherit;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.hover-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 
    0 20px 40px rgba(31, 38, 135, 0.6),
    0 8px 16px rgba(0, 0, 0, 0.1);
}

.hover-card:hover::before {
  opacity: 1;
}
```

---

## 🔔 **Notifications & Alerts**

### 📢 **Toast Notifications**
```html
<div class="toast toast-success" id="successToast">
  <div class="toast-icon">
    <i class="fas fa-check-circle"></i>
  </div>
  <div class="toast-content">
    <div class="toast-title">Berhasil!</div>
    <div class="toast-message">Absensi berhasil dicatat</div>
  </div>
  <button class="toast-close">
    <i class="fas fa-times"></i>
  </button>
</div>
```

```css
.toast {
  @extend .glass-component;
  position: fixed;
  top: 2rem;
  right: 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  max-width: 400px;
  transform: translateX(100%);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1000;
}

.toast.show {
  transform: translateX(0);
}

.toast-success {
  background: linear-gradient(135deg, 
    rgba(39, 174, 96, 0.2), 
    rgba(39, 174, 96, 0.1)
  );
  border-left: 4px solid var(--success);
}

.toast-error {
  background: linear-gradient(135deg, 
    rgba(231, 76, 60, 0.2), 
    rgba(231, 76, 60, 0.1)
  );
  border-left: 4px solid var(--error);
}

.toast-warning {
  background: linear-gradient(135deg, 
    rgba(243, 156, 18, 0.2), 
    rgba(243, 156, 18, 0.1)
  );
  border-left: 4px solid var(--warning);
}

.toast-icon {
  font-size: 1.5rem;
  color: inherit;
}

.toast-title {
  font-weight: 600;
  color: var(--white);
  margin-bottom: 0.25rem;
}

.toast-message {
  color: var(--gray-300);
  font-size: 0.875rem;
}

.toast-close {
  background: none;
  border: none;
  color: var(--gray-400);
  font-size: 1rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: color 0.3s ease;
}

.toast-close:hover {
  color: var(--white);
}
```

### 🚨 **Modal Dialogs**
```html
<div class="modal-overlay" id="confirmModal">
  <div class="modal-container">
    <div class="modal-header">
      <h3>Konfirmasi Absensi</h3>
      <button class="modal-close">
        <i class="fas fa-times"></i>
      </button>
    </div>
    <div class="modal-body">
      <p>Apakah Anda yakin ingin mencatat absensi keluar?</p>
      <div class="employee-info">
        <img src="employee-photo.jpg" alt="Photo" class="employee-photo">
        <div class="employee-details">
          <div class="employee-name">John Doe</div>
          <div class="employee-department">IT Development</div>
          <div class="confidence-display">Confidence: 98.5%</div>
        </div>
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal()">Batal</button>
      <button class="btn btn-primary" onclick="confirmAttendance()">Ya, Catat</button>
    </div>
  </div>
</div>
```

```css
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}

.modal-overlay.show {
  opacity: 1;
  visibility: visible;
}

.modal-container {
  @extend .glass-card;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  transform: scale(0.8);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-overlay.show .modal-container {
  transform: scale(1);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h3 {
  margin: 0;
  color: var(--white);
  font-size: 1.25rem;
  font-weight: 600;
}

.modal-close {
  background: none;
  border: none;
  color: var(--gray-400);
  font-size: 1.25rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.modal-close:hover {
  color: var(--white);
  background: rgba(255, 255, 255, 0.1);
}

.modal-body {
  margin-bottom: 2rem;
  color: var(--gray-300);
}

.employee-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
  padding: 1rem;
  @extend .glass-component;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
}

.employee-photo {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
}

.employee-name {
  font-weight: 600;
  color: var(--white);
  margin-bottom: 0.25rem;
}

.employee-department {
  color: var(--gray-400);
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
}

.confidence-display {
  @extend .confidence-badge;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}
```

---

## 📱 **PWA Enhancements**

### 🔧 **Install Prompt**
```html
<div class="install-prompt" id="installPrompt">
  <div class="install-content">
    <div class="install-icon">
      <i class="fas fa-download"></i>
    </div>
    <div class="install-text">
      <div class="install-title">Install ABSENN</div>
      <div class="install-description">
        Install aplikasi untuk akses cepat dan notifikasi
      </div>
    </div>
    <div class="install-actions">
      <button class="btn btn-secondary btn-sm" onclick="dismissInstall()">
        Nanti
      </button>
      <button class="btn btn-primary btn-sm" onclick="installApp()">
        Install
      </button>
    </div>
  </div>
</div>
```

```css
.install-prompt {
  position: fixed;
  bottom: 2rem;
  left: 2rem;
  right: 2rem;
  @extend .glass-card;
  padding: 1.5rem;
  transform: translateY(100%);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1000;
}

.install-prompt.show {
  transform: translateY(0);
}

.install-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.install-icon {
  width: 48px;
  height: 48px;
  @extend .glass-component;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  color: var(--coffee-medium);
  background: linear-gradient(135deg, 
    rgba(139, 69, 19, 0.2), 
    rgba(139, 69, 19, 0.1)
  );
}

.install-text {
  flex: 1;
}

.install-title {
  font-weight: 600;
  color: var(--white);
  margin-bottom: 0.25rem;
}

.install-description {
  color: var(--gray-300);
  font-size: 0.875rem;
}

.install-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}
```

---

## 🎯 **Accessibility Features**

### ♿ **WCAG Compliance**
```css
/* Focus indicators */
.focus-visible {
  outline: 2px solid var(--coffee-medium);
  outline-offset: 2px;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .glass-component {
    background: rgba(255, 255, 255, 0.9);
    color: var(--gray-900);
    border: 2px solid var(--gray-900);
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Dark mode preference */
@media (prefers-color-scheme: light) {
  :root {
    --glass-primary: rgba(0, 0, 0, 0.1);
    --glass-secondary: rgba(0, 0, 0, 0.05);
  }
}

/* Screen reader only text */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

### 🔊 **Screen Reader Support**
```html
<!-- Semantic HTML with ARIA labels -->
<main role="main" aria-label="Attendance System">
  <section aria-labelledby="qr-section-title">
    <h2 id="qr-section-title" class="sr-only">QR Code Scanner</h2>
    <div class="qr-container" role="img" aria-label="QR Code for attendance">
      <!-- QR Code content -->
    </div>
  </section>
  
  <section aria-labelledby="camera-section-title">
    <h2 id="camera-section-title" class="sr-only">Face Recognition</h2>
    <div class="camera-container" role="region" aria-label="Camera feed for face recognition">
      <video aria-label="Camera feed"></video>
    </div>
  </section>
  
  <div role="status" aria-live="polite" id="statusAnnouncer" class="sr-only">
    <!-- Dynamic status updates -->
  </div>
</main>
```

---

## 🔗 **Related Documentation**

- [📚 API Documentation](API_DOCUMENTATION.md)
- [🚀 Deployment Guide](DEPLOYMENT_GUIDE.md)
- [🗄️ Database Schema](README_DATABASE.md)
- [📋 Implementation Guide](IMPLEMENTASI_LENGKAP.md)
- [🔧 Troubleshooting](../README.md#troubleshooting)

---

**Last Updated**: October 5, 2025  
**UI Framework**: Glass Morphism + Bootstrap 5  
**Design Version**: 2.0.1