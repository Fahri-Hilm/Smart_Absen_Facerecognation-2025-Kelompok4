/**
 * Training Loader - Real-time loading indicator untuk training model
 */

class TrainingLoader {
    constructor() {
        this.isChecking = false;
        this.checkInterval = null;
        this.loadingElement = null;
        this.init();
    }

    init() {
        // Buat loading element
        this.createLoadingElement();
        
        // Start checking training status
        this.startChecking();
    }

    createLoadingElement() {
        // Cek apakah sudah ada
        if (document.getElementById('training-loader')) return;

        const loader = document.createElement('div');
        loader.id = 'training-loader';
        loader.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 9999;
            min-width: 300px;
            display: none;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        `;

        loader.innerHTML = `
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div class="spinner" style="
                    width: 20px; 
                    height: 20px; 
                    border: 2px solid rgba(255,255,255,0.3);
                    border-top: 2px solid white;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                    margin-right: 10px;
                "></div>
                <strong>🤖 Training Model</strong>
            </div>
            <div id="training-employee" style="font-size: 14px; margin-bottom: 8px;"></div>
            <div id="training-message" style="font-size: 13px; opacity: 0.9; margin-bottom: 10px;"></div>
            <div style="background: rgba(255,255,255,0.2); border-radius: 10px; height: 6px; overflow: hidden;">
                <div id="training-progress" style="
                    background: white;
                    height: 100%;
                    width: 0%;
                    transition: width 0.3s ease;
                    border-radius: 10px;
                "></div>
            </div>
            <div id="training-percent" style="font-size: 12px; text-align: right; margin-top: 5px;">0%</div>
        `;

        // Add CSS animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);

        document.body.appendChild(loader);
        this.loadingElement = loader;
    }

    startChecking() {
        if (this.isChecking) return;
        
        this.isChecking = true;
        this.checkInterval = setInterval(() => {
            this.checkTrainingStatus();
        }, 1000); // Check every second
    }

    stopChecking() {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
            this.checkInterval = null;
        }
        this.isChecking = false;
    }

    async checkTrainingStatus() {
        try {
            const response = await fetch('/api/training_status');
            const status = await response.json();

            if (status.is_training) {
                this.showLoading(status);
            } else {
                this.hideLoading();
                
                // Jika baru selesai training, refresh stats
                if (status.message && status.message.includes('selesai')) {
                    this.refreshDashboardStats();
                }
            }
        } catch (error) {
            console.error('Error checking training status:', error);
        }
    }

    showLoading(status) {
        if (!this.loadingElement) return;

        const employeeEl = document.getElementById('training-employee');
        const messageEl = document.getElementById('training-message');
        const progressEl = document.getElementById('training-progress');
        const percentEl = document.getElementById('training-percent');

        if (employeeEl) employeeEl.textContent = `Karyawan: ${status.employee_name}`;
        if (messageEl) messageEl.textContent = status.message;
        if (progressEl) progressEl.style.width = `${status.progress}%`;
        if (percentEl) percentEl.textContent = `${status.progress}%`;

        this.loadingElement.style.display = 'block';
    }

    hideLoading() {
        if (this.loadingElement) {
            this.loadingElement.style.display = 'none';
        }
    }

    refreshDashboardStats() {
        // Refresh stats di dashboard
        if (typeof updateDashboardStats === 'function') {
            updateDashboardStats();
        }
        
        // Refresh employee list jika ada
        if (typeof refreshEmployeeList === 'function') {
            refreshEmployeeList();
        }
    }

    destroy() {
        this.stopChecking();
        if (this.loadingElement) {
            this.loadingElement.remove();
        }
    }
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize on admin pages
    if (window.location.pathname.includes('/admin') || 
        window.location.pathname.includes('/capture') ||
        window.location.pathname.includes('/test')) {
        
        window.trainingLoader = new TrainingLoader();
        
        // Cleanup on page unload
        window.addEventListener('beforeunload', () => {
            if (window.trainingLoader) {
                window.trainingLoader.destroy();
            }
        });
    }
});

// Helper function untuk manual trigger
function showTrainingLoader(employeeName, message, progress = 0) {
    if (window.trainingLoader) {
        window.trainingLoader.showLoading({
            employee_name: employeeName,
            message: message,
            progress: progress,
            is_training: true
        });
    }
}

function hideTrainingLoader() {
    if (window.trainingLoader) {
        window.trainingLoader.hideLoading();
    }
}
