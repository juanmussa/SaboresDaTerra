/**
 * Script Principal - Sabores da Serra
 * Implementa funcionalidades de menu mobile, carrossel de imagens e validação de formulários.
 */

document.addEventListener('DOMContentLoaded', () => {
    // ---------------------------------------------------------
    // 1. MENU RESPONSIVO MOBILE
    // ---------------------------------------------------------
    const menuToggle = document.getElementById('menuToggle');
    const navMenu = document.getElementById('navMenu');

    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            
            // Altera o ícone do botão (bars <-> xmark)
            const icon = menuToggle.querySelector('i');
            if (icon) {
                if (navMenu.classList.contains('active')) {
                    icon.className = 'fa-solid fa-xmark';
                } else {
                    icon.className = 'fa-solid fa-bars';
                }
            }
        });

        // Fecha o menu ao clicar fora dele
        document.addEventListener('click', (e) => {
            if (!menuToggle.contains(e.target) && !navMenu.contains(e.target)) {
                navMenu.classList.remove('active');
                const icon = menuToggle.querySelector('i');
                if (icon) {
                    icon.className = 'fa-solid fa-bars';
                }
            }
        });
    }

    // ---------------------------------------------------------
    // 2. CARROSSEL DA PÁGINA INICIAL
    // ---------------------------------------------------------
    const slides = document.querySelectorAll('.carousel-slide');
    const dots = document.querySelectorAll('.indicator-dot');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    if (slides.length > 0) {
        let currentSlide = 0;
        let slideInterval;
        const intervalTime = 6000; // 6 segundos por imagem

        const showSlide = (index) => {
            // Remove classes ativas de todos
            slides.forEach(slide => slide.classList.remove('active'));
            dots.forEach(dot => dot.classList.remove('active'));

            // Trata limites circulares
            currentSlide = (index + slides.length) % slides.length;

            // Ativa o slide e indicador atual
            slides[currentSlide].classList.add('active');
            if (dots[currentSlide]) {
                dots[currentSlide].classList.add('active');
            }
        };

        const nextSlide = () => {
            showSlide(currentSlide + 1);
        };

        const prevSlide = () => {
            showSlide(currentSlide - 1);
        };

        const startSlideShow = () => {
            stopSlideShow();
            slideInterval = setInterval(nextSlide, intervalTime);
        };

        const stopSlideShow = () => {
            if (slideInterval) {
                clearInterval(slideInterval);
            }
        };

        // Eventos dos botões de controle
        if (prevBtn && nextBtn) {
            prevBtn.addEventListener('click', () => {
                prevSlide();
                startSlideShow(); // Reinicia o timer ao interagir
            });

            nextBtn.addEventListener('click', () => {
                nextSlide();
                startSlideShow();
            });
        }

        // Eventos dos indicadores (dots)
        dots.forEach(dot => {
            dot.addEventListener('click', (e) => {
                const targetIndex = parseInt(e.target.getAttribute('data-slide-to'), 10);
                showSlide(targetIndex);
                startSlideShow();
            });
        });

        // Pausa o slideshow quando o mouse está sobre o carrossel
        const carouselContainer = document.querySelector('.hero-carousel');
        if (carouselContainer) {
            carouselContainer.addEventListener('mouseenter', stopSlideShow);
            carouselContainer.addEventListener('mouseleave', startSlideShow);
        }

        // Inicializa o slideshow automático
        startSlideShow();
    }

    // ---------------------------------------------------------
    // 3. VALIDAÇÃO DO FORMULÁRIO DE CONTATO
    // ---------------------------------------------------------
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        const nomeInput = document.getElementById('nome');
        const emailInput = document.getElementById('email');
        const telefoneInput = document.getElementById('telefone');
        const assuntoSelect = document.getElementById('assunto');
        const mensagemInput = document.getElementById('mensagem');

        const validateField = (input, validatorFn, parentGroup) => {
            const isValid = validatorFn(input.value);
            if (isValid) {
                parentGroup.classList.remove('invalid');
            } else {
                parentGroup.classList.add('invalid');
            }
            return isValid;
        };

        // Regras de validação
        const validators = {
            nome: (val) => val.trim().length >= 3,
            email: (val) => {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                return emailRegex.test(val.trim());
            },
            telefone: (val) => {
                if (!val.trim()) return true; // Telefone é opcional
                const digits = val.replace(/\D/g, '');
                return digits.length >= 10 && digits.length <= 11;
            },
            assunto: (val) => val !== "" && val !== null,
            mensagem: (val) => val.trim().length > 0
        };

        // Adiciona listeners para feedback em tempo real no blur e input
        nomeInput.addEventListener('blur', () => validateField(nomeInput, validators.nome, nomeInput.parentElement));
        emailInput.addEventListener('blur', () => validateField(emailInput, validators.email, emailInput.parentElement));
        telefoneInput.addEventListener('input', () => {
            // Máscara básica para telefone ex: (24) 99999-9999
            let value = telefoneInput.value.replace(/\D/g, '');
            if (value.length > 11) value = value.substring(0, 11);
            
            if (value.length > 6) {
                telefoneInput.value = `(${value.substring(0, 2)}) ${value.substring(2, 7)}-${value.substring(7)}`;
            } else if (value.length > 2) {
                telefoneInput.value = `(${value.substring(0, 2)}) ${value.substring(2)}`;
            } else if (value.length > 0) {
                telefoneInput.value = `(${value}`;
            }
        });
        telefoneInput.addEventListener('blur', () => validateField(telefoneInput, validators.telefone, telefoneInput.parentElement));
        assuntoSelect.addEventListener('change', () => validateField(assuntoSelect, validators.assunto, assuntoSelect.parentElement));
        mensagemInput.addEventListener('blur', () => validateField(mensagemInput, validators.mensagem, mensagemInput.parentElement));

        // Validação no Envio
        contactForm.addEventListener('submit', (e) => {
            const isNomeValid = validateField(nomeInput, validators.nome, nomeInput.parentElement);
            const isEmailValid = validateField(emailInput, validators.email, emailInput.parentElement);
            const isTelefoneValid = validateField(telefoneInput, validators.telefone, telefoneInput.parentElement);
            const isAssuntoValid = validateField(assuntoSelect, validators.assunto, assuntoSelect.parentElement);
            const isMensagemValid = validateField(mensagemInput, validators.mensagem, mensagemInput.parentElement);

            const isFormValid = isNomeValid && isEmailValid && isTelefoneValid && isAssuntoValid && isMensagemValid;

            if (!isFormValid) {
                e.preventDefault(); // Impede o envio do formulário
                
                // Rola para o primeiro campo inválido
                const firstInvalid = contactForm.querySelector('.form-group.invalid');
                if (firstInvalid) {
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    }

    // ---------------------------------------------------------
    // 4. ANIMAÇÕES DE MENSAGENS FLASH (AUTO-FECHAR)
    // ---------------------------------------------------------
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
        // Auto-remove a mensagem após 5 segundos
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateX(100px)';
            msg.style.transition = 'all 0.5s ease';
            setTimeout(() => msg.remove(), 500);
        }, 5000);
    });
});
