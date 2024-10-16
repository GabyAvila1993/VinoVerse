document.addEventListener("DOMContentLoaded", () => {
    const videoOverlay = document.getElementById("videoOverlay");
    const transitionVideo = document.getElementById("transitionVideo");
    const navLinks = document.querySelectorAll(".nav-link");

    // Función para reproducir el video y luego navegar
    const playVideoAndNavigate = (href) => {
        videoOverlay.style.visibility = "visible";  // Muestra el overlay
        transitionVideo.play();  // Reproduce el video

        // Espera hasta que termine el video para navegar
        transitionVideo.onended = () => {
            window.location.href = href;  // Navega a la nueva página
        };
    };

    // Reproduce el video cuando se hace clic en un enlace
    navLinks.forEach(link => {
        link.addEventListener("click", function(event) {
            event.preventDefault();  // Previene la navegación inmediata
            playVideoAndNavigate(this.href);  // Reproduce el video y luego navega
        });
    });

    // Reproduce el video nuevamente cuando el usuario presiona "Atrás"
    window.addEventListener("pageshow", (event) => {
        if (event.persisted) {  // Detecta si la página fue cargada desde la caché (lo que suele suceder al presionar "Atrás")
            playVideoAndNavigate(window.location.href);  // Reproduce el video nuevamente antes de recargar la página
        }
    });
});

