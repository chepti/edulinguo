// אדולינגו - קוד JavaScript ראשי

document.addEventListener('DOMContentLoaded', function() {
    // אתחול טולטיפים של Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // אתחול פופוברים של Bootstrap
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // אנימציה לכפתורי השלמת אתגר
    const challengeButtons = document.querySelectorAll('.complete-challenge-btn');
    challengeButtons.forEach(button => {
        button.addEventListener('click', function() {
            // הוספת אנימציה לפני שליחת הטופס
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> מעבד...';
            this.disabled = true;
        });
    });
    
    // אנימציה לכפתורי השלמת אטום למידה
    const completeAtomButtons = document.querySelectorAll('.complete-atom-btn');
    completeAtomButtons.forEach(button => {
        button.addEventListener('click', function() {
            // הוספת אנימציה לפני שליחת הטופס
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> מעבד...';
            this.disabled = true;
        });
    });
    
    // אנימציה לכרטיסי הישגים
    const achievementCards = document.querySelectorAll('.achievement-card');
    achievementCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('pulse');
        });
        card.addEventListener('mouseleave', function() {
            this.classList.remove('pulse');
        });
    });
    
    // טיימר לאתגר יומי
    const dailyChallengeTimer = document.getElementById('daily-challenge-timer');
    if (dailyChallengeTimer) {
        updateDailyChallengeTimer();
        setInterval(updateDailyChallengeTimer, 1000);
    }
    
    // פונקציה לעדכון טיימר האתגר היומי
    function updateDailyChallengeTimer() {
        const now = new Date();
        const endOfDay = new Date();
        endOfDay.setHours(23, 59, 59, 999);
        
        const timeLeft = endOfDay - now;
        
        const hours = Math.floor(timeLeft / (1000 * 60 * 60));
        const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
        
        dailyChallengeTimer.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
    
    // אפקט הבזק לנקודות חדשות
    const pointsBadge = document.querySelector('.points-badge');
    if (pointsBadge && pointsBadge.dataset.newPoints === 'true') {
        pointsBadge.classList.add('flash');
        setTimeout(() => {
            pointsBadge.classList.remove('flash');
        }, 3000);
    }
}); 